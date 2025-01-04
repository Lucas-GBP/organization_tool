"use client";
import Head from "next/head";
import Link from "next/link";
import { useCallback, useContext, useEffect, useMemo, useState, type ChangeEvent } from "react";
import { DatePicker } from "antd";
import dayjs from "dayjs";
//import { CategorySelector, SelectedCategoryObject } from "@/components/categorySelector";
import style from "@/styles/pages/timer.module.scss";
import { PageContext, type PageContextType } from "@/context/pageContext";
import { TimeRangeEventNotDeleted } from "@/api/types/timerEvent";
import { CategotyCompletedRecord } from "@/api/types/category";
import { CategorySelector, type SelectedCategoryObject, Button, Input } from "@/components";
import { findCategory, calculateDeltaDate, type DeltaDateType } from "@/utils";
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
    const { repository, categories } = props.context;

    return (
        <main>
            <h1>Timer</h1>
            <section>
                <RunningTimer repository={repository} categories={categories ? categories : []} />
            </section>
            <TimerEventList repository={repository} categories={categories ? categories : []} />
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
    const [deltaTime, setDeltaTime] = useState<DeltaDateType | undefined>(undefined);

    const formatTime = useMemo(() => {
        if (!deltaTime) {
            return "";
        }

        return `${deltaTime.hours.toString().padStart(2, "0")}:${deltaTime.minutes.toString().padStart(2, "0")}:${deltaTime.seconds
            .toString()
            .padStart(2, "0")}.${deltaTime.centiseconds.toString().padStart(2, "0")}`;
    }, [deltaTime]);
    const selectedCategory = useMemo(() => {
        if (!running) {
            return undefined;
        }
        return findCategory(props.categories, running.category_uuid, running.sub_category_uuid);
    }, [props.categories, running]);

    const get_running = useCallback(async () => {
        const _runnig = await repository.timerEvent.get_running();
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
            if (!running) {
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
        [repository, running, setRunning]
    );

    useEffect(() => {
        if (!running) {
            setDeltaTime(undefined);
            return;
        }
        // Atualiza o tempo decorrido a cada segundo
        const interval = setInterval(() => {
            setDeltaTime(calculateDeltaDate(running.start_time));
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
                    <Button onClick={stop_timer}>Stop Timer</Button>
                    <CategorySelector
                        categories={props.categories}
                        setItem={update_categories}
                        selected={selectedCategory}
                    />
                    {deltaTime && <div>{formatTime}</div>}
                </>
            ) : (
                <Button onClick={start_timer}>Start Timer</Button>
            )}
        </>
    );
}

type TimerEventListProps = {
    repository: Repository;
    categories: CategotyCompletedRecord[];
};
function TimerEventList(props: TimerEventListProps) {
    const { repository } = props;
    const [list, setList] = useState<undefined | TimeRangeEventNotDeleted[]>(undefined);
    const [range, setRange] = useState<{ start: Date; end: Date }>({
        start: new Date("2023"),
        end: new Date(),
    });

    const get_list = useCallback(
        async (range: { start: Date; end: Date }) => {
            const _list = await repository.timerEvent.get_by_range(range.start, new Date());
            _list.sort((a, b) => a.start_time.getTime() - b.start_time.getTime())
            setList(_list);
        },
        [repository, setList]
    );
    const updateTimerEvent = useCallback(
        (index: number, event?: TimeRangeEventNotDeleted) => {
            if (!list) {
                return;
            }
            const list_copy = [...list];
            if (!event) {
                list_copy.splice(index, 1);
                setList(list_copy);
                return;
            }
            list_copy[index] = event;
            setList(list_copy);
            return;
        },
        [list, setList]
    );

    useEffect(() => {
        get_list(range);
    }, [get_list, range]);

    return (
        <section>
            <div>
                <Button onClick={() => get_list(range)}>Get List</Button>
            </div>
            <div>
                {list &&
                    list.map((item, index) => (
                        <TimerEvent
                            key={item.uuid}
                            repository={repository}
                            categories={props.categories ? props.categories : []}
                            timerEvent={item}
                            setTimerEvent={(update_item) => {
                                updateTimerEvent(index, update_item);
                            }}
                        />
                    ))}
            </div>
        </section>
    );
}

type TimerEventProps = {
    repository: Repository;
    categories: CategotyCompletedRecord[];
    timerEvent: TimeRangeEventNotDeleted;
    setTimerEvent: (data?: TimeRangeEventNotDeleted) => void;
};
function TimerEvent(props: TimerEventProps) {
    const { repository, timerEvent, setTimerEvent } = props;

    const deltaTime = useMemo(() => {
        return calculateDeltaDate(timerEvent.start_time, timerEvent.end_time);
    }, [timerEvent]);
    const formatedTime = useMemo(() => {
        if (!deltaTime) {
            return "";
        }

        return `${deltaTime.hours.toString().padStart(2, "0")}h ${deltaTime.minutes.toString().padStart(2, "0")}min ${deltaTime.seconds.toString().padStart(2, "0")}s`;
    }, [deltaTime]);
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
        [repository, timerEvent, setTimerEvent]
    );
    const update_title = useCallback(
        async (e: ChangeEvent<HTMLInputElement>) => {
            const updated = await repository.timerEvent.patch({
                ...timerEvent,
                title: e.target.value.length > 0 ? e.target.value : undefined,
            });
            setTimerEvent(updated);
        },
        [repository, timerEvent, setTimerEvent]
    );
    const update_description = useCallback(
        async (e: ChangeEvent<HTMLInputElement>) => {
            const updated = await repository.timerEvent.patch({
                ...timerEvent,
                description: e.target.value.length > 0 ? e.target.value : undefined,
            });
            setTimerEvent(updated);
        },
        [repository, timerEvent, setTimerEvent]
    );
    const delete_event = useCallback(async () => {
        const deleted = await repository.timerEvent.delete(timerEvent.uuid);
        if(deleted !== timerEvent.uuid){
            return;
        }

        setTimerEvent(undefined);
    }, [repository, timerEvent, setTimerEvent])

    useEffect(() => {
        setTimerEvent(props.timerEvent);
    }, [props.timerEvent]);

    return (
        <div className={style.timerEvent}>
            {formatedTime}{"\t"}
            <CategorySelector categories={props.categories} setItem={update_categories} selected={selectedCategory} />
            <RangePicker 
                showTime 
                defaultValue={[
                    dayjs(timerEvent.start_time), 
                    dayjs(timerEvent.end_time)
                ]}
                onChange={(item) => console.warn(item)} 
            />
            <Button onClick={delete_event}>Delete</Button> <br />
            title: <Input defaultValue={timerEvent.title} onBlur={update_title} />
            Description: <Input defaultValue={timerEvent.description} onBlur={update_description} />
        </div>
    );
}