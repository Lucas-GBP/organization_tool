"use client";
import { useState, useCallback } from "react";
//import { arrayToMap } from "@/utils/arrayToMap";
//import { UUID } from "crypto";

type taskType = {
    title: string;
    completed: boolean;
};
const emptyTask: taskType = {
    title: "",
    completed: false,
};

function Page() {
    const [task, setTask] = useState<taskType>(emptyTask);
    const [tasksMap, setTasksMap] = useState(new Map<number, taskType>());

    const addTask = useCallback(() => {
        const copyTasks = new Map(tasksMap);
        copyTasks.set(Date.now(), task);

        setTasksMap(copyTasks);
        setTask(emptyTask);
    }, [task, tasksMap]);

    const toggleComplete = useCallback(
        (id: number) => {
            const taskToUpdate = tasksMap.get(id);
            if (taskToUpdate) {
                const copyTasks = new Map(tasksMap);
                taskToUpdate.completed = !taskToUpdate.completed;
                copyTasks.set(id, taskToUpdate);

                setTasksMap(copyTasks);
            }
        },
        [tasksMap]
    );

    const removeTask = useCallback(
        (id: number) => {
            const copyTasks = new Map(tasksMap);
            copyTasks.delete(id);

            setTasksMap(copyTasks);
        },
        [tasksMap]
    );

    return (
        <>
            <h1>To-Do List</h1>
            <section>
                <input
                    type="text"
                    value={task.title}
                    onChange={(e) =>
                        setTask({
                            title: e.target.value,
                            completed: false,
                        })
                    }
                    placeholder="Add a new task"
                />
                <button onClick={addTask}>Add Task</button>
                <ul>
                    {[...tasksMap.entries()].map(([id, task]) => (
                        <li key={id} style={{ textDecoration: task.completed ? "line-through" : undefined }}>
                            {task.title}
                            <button onClick={() => toggleComplete(id)}>{task.completed ? "Undo" : "Complete"}</button>
                            <button onClick={() => removeTask(id)}>Remove</button>
                        </li>
                    ))}
                </ul>
            </section>
        </>
    );
}

export default Page;
