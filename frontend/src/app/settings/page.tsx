"use client"
import { useEffect, useRef, useState, useContext } from "react"
import { Category } from "@/api/category";
import { CategoryItem } from "@/components/categoryItem";
import type { CategoryRecord, CategoryPost } from "@/api/types/category";
import { PageContext } from "@/context/pageContext";

const standart_post_data = (uuid:string) => { return {
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

export default function Test(){
    const context = useContext(PageContext);
    const [data, setData] = useState<CategoryRecord[]>([]);
    const categoryRepository = useRef(new Category());

    const getData = async () => {
        if (!context || !context?.user_uuid) return;

        const category_list = await categoryRepository.current.get_all(context.user_uuid);
        console.log({category_list});
        setData(category_list);
    }
    const postData = async () => {
        if (!context || !context?.user_uuid) return;

        const post_data:CategoryPost = standart_post_data(context.user_uuid)
        const result = await categoryRepository.current.post(post_data);
        console.log({result});
        getData();
    }

    useEffect(() => {
        console.log({context})
        try{
            getData()
        } catch (e){
            console.error(e);
            setData([]);
        }
    }, [])

    return <>
        <main>
            <h1>Settings</h1>
            <section>
                <h2>Categories</h2>
                {data.map((item) => {
                    return <CategoryItem
                        key={"category_item_"+item.uuid}
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