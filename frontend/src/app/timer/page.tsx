"use client";
import Head from "next/head";
import Link from "next/link";
import { useCallback, useContext, useEffect, useState } from "react";
import { DatePicker } from "antd";
import dayjs from "dayjs";
//import { CategorySelector, SelectedCategoryObject } from "@/components/categorySelector";
import style from "@/styles/pages/timer.module.scss";
import { PageContext, type PageContextType } from "@/context/pageContext";
import { TimeRangeEventNotDeleted } from "@/api/types/timerEvent";
import { CategotyCompletedRecord } from "@/api/types/category";
import { CategorySelector, type SelectedCategoryObject } from "@/components";
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
                <RunningTimer repository={repository} />
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
                        />
                    ))}
            </section>
        </main>
    );
}

type RunningTimerProps = {
    repository: Repository;
};
function RunningTimer(props: RunningTimerProps) {
    const { repository } = props;
    const [running, setRunning] = useState<TimeRangeEventNotDeleted | undefined>(undefined);
    const [deltaTime, setDeltaTime] = useState<number | undefined>(undefined);

    const get_running = useCallback(async () => {
        setRunning(await repository.timerEvent.get_running());
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
    const formatTime = useCallback((decisecond: number) => {
        const seconds = decisecond / 100;

        const deci = Math.floor(decisecond % 100);
        const secs = Math.floor(seconds % 60);
        const minutes = Math.floor((seconds % 3600) / 60);
        const hours = Math.floor(seconds / 3600);

        return `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${secs
            .toString()
            .padStart(2, "0")}.${deci.toString().padStart(2, "0")}`;
    }, []);

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
                    {deltaTime && <div>{formatTime(deltaTime)}</div>}
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
};
function TimerEvent(props: TimerEventProps) {
    const { repository } = props;
    const [timerEvent, setTimerEvent] = useState(props.timerEvent);
    const [selectedCategory, setSelectedCategory] = useState<SelectedCategoryObject | undefined>(undefined);

    useEffect(() => {
        setTimerEvent(props.timerEvent);
    }, [props.timerEvent]);
    useEffect(() => {
        console.log(selectedCategory);
    }, [selectedCategory]);

    return (
        <div className={style.timerEvent}>
            <CategorySelector
                categories={props.categories}
                setItem={(item) => {
                    setSelectedCategory(item);
                }}
                selected={selectedCategory}
            />
            <RangePicker showTime defaultValue={[dayjs(timerEvent.start_time), dayjs(timerEvent.end_time)]} />
        </div>
    );
}
