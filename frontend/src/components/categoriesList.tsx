import { useEffect, useState, useCallback } from "react";
import { CategoryItem } from "@/components";
import type { CategoryRecord, CategoryPost } from "@/api/types/category";
import { arrayToMap } from "@/utils/arrayToMap";
import { UUID } from "crypto";
import { Repository } from "@/api";

export interface CategoriesListProps {
    repository: Repository,
    user_uuid: UUID
}
export default function CategoriesList(props: CategoriesListProps) {
    const {repository, user_uuid} = props;
    const [categories, setCategories] = useState<Map<UUID, CategoryRecord>>(new Map());

    const getData = useCallback(async () => {
        const category_list = await repository.category.get_all();
        setCategories(arrayToMap(category_list));
    }, [repository]);

    const postData = useCallback(async () => {
        const post_data = standart_post_data(user_uuid);
        const result = await repository.category.post_completed(post_data);
        console.log({ result });
        getData();
    }, [repository, user_uuid, getData]);

    useEffect(() => {
        getData();
    }, [])
    useEffect(() => {
        console.warn(categories);
    }, [categories]);

    return <section>
        <h2>Categories</h2>
        {Array.from(categories.keys()).map((uuid) => {
            return (
                <CategoryItem
                    key={uuid}
                    item={categories.get(uuid)!}
                    updateList={getData}
                    repository={repository!}
                />
            );
        })}
        <button onClick={postData}>Post Data</button>
    </section>
}

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
