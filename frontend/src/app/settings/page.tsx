"use client"
import { useEffect, useRef, useState, useContext, useCallback } from "react"
import { Category } from "@/api/category";
import { CategoryItem } from "@/components";
import type { CategoryRecord, CategoryPost } from "@/api/types/category";
import { arrayToMap } from "@/utils/arrayToMap";
import { PageContext } from "@/context/pageContext";
import { UUID } from "crypto";

const standart_post_data:(uuid:UUID) => CategoryPost = (uuid:UUID) => { return {
    user_uuid: uuid,
    title: "A NICE title",
    color: "#ffffff",
    description: "A very good description",
    sub_categories: [{
        color: "#000000",
        title: "A NICE sub title"
    }, {
        color: "#cecece",
        title: "A NICE sub title"
    }]
}}

export default function Page(){
    const context = useContext(PageContext);
    const categoryRepository = useRef(new Category());
    const [data, setData] = useState<Map<UUID, CategoryRecord>>(new Map());

    const getData = useCallback(async () => {
        if (!context || !context?.user_uuid) {
            console.warn("Without context or user_uuid");
            return;
        };

        const category_list = await categoryRepository.current.get_all(context.user_uuid);
        setData(arrayToMap(category_list));
    }, [context, context?.user_uuid])

    const postData = useCallback(async () => {
        if (!context || !context?.user_uuid) {
            console.warn("Without context or user_uuid");
            return;
        };

        const post_data:CategoryPost = standart_post_data(context.user_uuid)
        const result = await categoryRepository.current.post(post_data);
        console.log({result});
        getData();
    }, [context, context?.user_uuid])

    useEffect(() => {
        if (!context || !context?.user_uuid) {
            console.warn("(useEffect) -> Without context or user_uuid");
            return;
        };

        try{
            getData()
        } catch (e){
            console.error(e);
            setData([]);
        }
    }, [context])

    return <>
        <main>
            <h1>Settings</h1>
            <section>
                <h2>Categories</h2>
                {data.map((item) => {
                    return <CategoryItem
                        key={item.uuid}
                        item={item}
                        api={categoryRepository.current}
                        updateList={getData}
                    />
                })}
            </section>
            <button onClick={postData}>Post Data</button>
        </main>
    </>
}