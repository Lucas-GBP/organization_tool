"use client";
import { useEffect, useState, useContext, useCallback } from "react";
import { CategoryItem } from "@/components";
import type { CategoryRecord, CategoryPost } from "@/api/types/category";
import { arrayToMap } from "@/utils/arrayToMap";
import { PageContext } from "@/context/pageContext";
import { UUID } from "crypto";

const standart_post_data = (uuid: UUID) => {
    return {
        user_uuid: uuid,
        title: "A NICE title",
        color: "#ffffff",
        description: "A very good description",
        sub_categories: [
            {
                color: "#000000",
                title: "A NICE sub title",
            },
            {
                color: "#cecece",
                title: "A NICE sub title",
            },
        ],
    } as CategoryPost;
};

export default function Page() {
    const context = useContext(PageContext);
    const [data, setData] = useState<Map<UUID, CategoryRecord>>(new Map());

    const getData = useCallback(async () => {
        if (!context) {
            return;
        }
        const { repository } = context;

        const category_list = await repository.category.get_all_completed();
        setData(arrayToMap(category_list));
    }, [context]);

    const postData = useCallback(async () => {
        if (!context) {
            console.warn("Without context or user_uuid");
            return;
        }
        const { repository } = context;

        const post_data = standart_post_data(context.user_uuid);
        const result = await repository.category.post_completed(post_data);
        console.log({ result });
        getData();
    }, [context, getData]);

    useEffect(() => {
        if (!context || !context?.user_uuid) {
            return;
        }

        try {
            getData();
        } catch (e) {
            console.error(e);
            setData(new Map());
        }
    }, [context, getData]);

    useEffect(() => {
        console.warn(data);
    }, [data]);

    return (
        <main>
            <h1>Settings</h1>
            <section>
                <h2>Categories</h2>
                {Array.from(data.keys()).map((uuid) => {
                    return (
                        <CategoryItem
                            key={uuid}
                            item={data.get(uuid)!}
                            updateList={getData}
                            repository={context?.repository!}
                        />
                    );
                })}
            </section>
            <button onClick={postData}>Post Data</button>
        </main>
    );
}
