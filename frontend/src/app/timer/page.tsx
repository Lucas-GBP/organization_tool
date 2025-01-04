"use client";
import Head from "next/head";
import Link from "next/link";
import { useCallback, useContext, useEffect, useMemo, useState } from "react";
import { DatePicker } from "antd";
import dayjs from "dayjs";
//import { CategorySelector, SelectedCategoryObject } from "@/components/categorySelector";
import style from "@/styles/pages/timer.module.scss";
import { PageContext, type PageContextType } from "@/context/pageContext";
import { TimeRangeEventNotDeleted } from "@/api/types/timerEvent";
import { CategotyCompletedRecord } from "@/api/types/category";
import { CategorySelector, type SelectedCategoryObject } from "@/components";
import { findCategory } from "@/utils";
import { Repository } from "@/api";

const { RangePicker } = DatePicker;

export default function Home() {
    const context = useContext(PageContext);

    return (
        <>
            <Head>
                <title>Timer</title>
                <meta name="description" content="Descrição da minha página" />
            </Head>
            {context && <Main context={context} />}
            <footer>
                <Link href="/">Home</Link>
            </footer>
        </>
    );
}

type MainProps = {
    context: PageContextType;
};
function Main(props: MainProps) {
    const { repository } = props.context;
    const [list, setList] = useState<undefined | TimeRangeEventNotDeleted[]>(undefined);

    const get_list = useCallback(async () => {
        const _list = await repository.timerEvent.get_by_range(new Date("2023"), new Date());
        setList(_list);
    }, [repository, setList]);

    useEffect(() => {
        // get_list();
    }, []);

    return (
        <main>
            <h1>Timer</h1>
            <section>
                <RunningTimer 
                    repository={repository}
                    categories={props.context.categories ? props.context.categories : []}
                />
                <br />
            </section>
            <section>
                <button onClick={get_list}>Get List</button>
            </section>
            <section>
                {list &&
                    list.map((item) => (
                        <TimerEvent
                            key={item.uuid}
                            repository={repository}
                            timerEvent={item}
                            categories={props.context.categories ? props.context.categories : []}
                            updateTimerEvent={(item) => console.log({item})}
                        />
                    ))}
            </section>
        </main>
    );
}

type RunningTimerProps = {
    repository: Repository;
    categories: CategotyCompletedRecord[];
};
function RunningTimer(props: RunningTimerProps) {
    const { repository } = props;
    const [running, setRunning] = useState<TimeRangeEventNotDeleted | undefined>(undefined);
    const [deltaTime, setDeltaTime] = useState<number | undefined>(undefined);

    const formatTime = useMemo(() => {
        if (!deltaTime) {
            return "";
        }
        const seconds = deltaTime / 100;

        const deci = Math.floor(deltaTime % 100);
        const secs = Math.floor(seconds % 60);
        const minutes = Math.floor((seconds % 3600) / 60);
        const hours = Math.floor(seconds / 3600);

        return `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${secs
            .toString()
            .padStart(2, "0")}.${deci.toString().padStart(2, "0")}`;
    }, [deltaTime]);
    const selectedCategory = useMemo(() => {
        if (!running){
            return undefined;
        }
        return findCategory(props.categories, running.category_uuid, running.sub_category_uuid);
    }, [props.categories, running]);

    const get_running = useCallback(async () => {
        const _runnig = await repository.timerEvent.get_running();
        console.log({_runnig});
        setRunning(_runnig);
    }, [repository]);
    const start_timer = useCallback(async () => {
        const running = await repository.timerEvent.post({
            start_time: new Date(),
        });
        setRunning(running);
    }, [repository]);
    const stop_timer = useCallback(async () => {
        if (!running) {
            return;
        }
        const stoped = await repository.timerEvent.patch({
            ...running,
            end_time: new Date(),
        });
        if (stoped) {
            get_running();
        }
    }, [repository, running, get_running]);
    const update_categories = useCallback(
        async (item: SelectedCategoryObject) => {
            if (!running){
                return;
            }
            const updated = await repository.timerEvent.patch({
                ...running,
                category_uuid: item.category.uuid,
                sub_category_uuid: item.subCategory?.uuid,
            });
            if (updated.category_uuid !== item.category.uuid) {
                console.error("category uuid not updated.");
                return;
            }
            if (!item.subCategory) {
                if (updated.sub_category_uuid) {
                    console.error("sub category uuid not updated. A");
                    return;
                }
            } else if (item.subCategory.uuid !== updated.sub_category_uuid) {
                console.error("sub category uuid not updated. B");
                return;
            }

            setRunning(updated);
        },
        [repository.timerEvent, running, setRunning]
    );

    useEffect(() => {
        if (!running) {
            setDeltaTime(undefined);
            return;
        }
        // Atualiza o tempo decorrido a cada segundo
        const interval = setInterval(() => {
            const now = new Date();
            const miliseconds = now.getTime() - running.start_time.getTime();
            const delta_t = Math.floor(miliseconds / 10);
            setDeltaTime(delta_t);
        }, 10);

        return () => clearInterval(interval);
    }, [running]);

    useEffect(() => {
        get_running();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <>
            {running ? (
                <>
                    <button onClick={stop_timer}>Stop Timer</button>
                    {/*TODO: <CategorySelector categories={props.categories} setItem={update_categories} selected={selectedCategory} />*/}
                    {deltaTime && <div>{formatTime}</div>}
                </>
            ) : (
                <button onClick={start_timer}>Start Timer</button>
            )}
        </>
    );
}

type TimerEventProps = {
    repository: Repository;
    categories: CategotyCompletedRecord[];
    timerEvent: TimeRangeEventNotDeleted;
    updateTimerEvent: (data: TimeRangeEventNotDeleted|undefined) => void;
};
function TimerEvent(props: TimerEventProps) {
    const { repository } = props;
    const [timerEvent, setTimerEvent] = useState(props.timerEvent);

    const selectedCategory = useMemo(() => {
        return findCategory(props.categories, timerEvent.category_uuid, timerEvent.sub_category_uuid);
    }, [props.categories, timerEvent]);

    const update_categories = useCallback(
        async (item: SelectedCategoryObject) => {
            const updated = await repository.timerEvent.patch({
                ...timerEvent,
                category_uuid: item.category.uuid,
                sub_category_uuid: item.subCategory?.uuid,
            });
            if (updated.category_uuid !== item.category.uuid) {
                console.error("category uuid not updated.");
                return;
            }
            if (!item.subCategory) {
                if (updated.sub_category_uuid) {
                    console.error("sub category uuid not updated. A");
                    return;
                }
            } else if (item.subCategory.uuid !== updated.sub_category_uuid) {
                console.error("sub category uuid not updated. B");
                return;
            }

            setTimerEvent(updated);
        },
        [repository.timerEvent, timerEvent, setTimerEvent]
    );

    useEffect(() => {
        setTimerEvent(props.timerEvent);
    }, [props.timerEvent]);

    return (
        <div className={style.timerEvent}>
            <CategorySelector categories={props.categories} setItem={update_categories} selected={selectedCategory} />
            <RangePicker showTime defaultValue={[dayjs(timerEvent.start_time), dayjs(timerEvent.end_time)]} />
        </div>
    );
}
