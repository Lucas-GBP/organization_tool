"use client"
import { useEffect, useState } from "react"
import { Category } from "@/api/category";
import type { CategoryRecord } from "@/api/category";

export default function Test(){
    const [data, setData] = useState<CategoryRecord[]>([]);

    const getData = async () => {
        const category = new Category();
        const _data = await category.get(1);
        console.log({_data})
        setData(_data)
    }

    useEffect(() => {
        try{
            getData()
        } catch (e){
            console.error(e)
            setData([])
        }
    }, [])

    return <>
        <main>
            <h1>Testes</h1>
            <section>
                {data.map((item, index) => {
                    return <div key={index}>
                        {item.user_id} {item.id}
                    </div>
                })}
            </section>
        </main>
    </>
}