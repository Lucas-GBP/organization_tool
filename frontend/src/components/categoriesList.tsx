import { useEffect, useState, useCallback } from "react";
import { CategoryItem } from "@/components";
import type { CategoryPost, CategotyCompletedRecord } from "@/api/types/category";
import { arrayToMap } from "@/utils/arrayToMap";
import { UUID } from "crypto";
import { Repository } from "@/api";

const standart_post_data:CategoryPost = {
    title: "New Category",
    color: "#ffffff",
    description: undefined,
};

export interface CategoriesListProps {
    repository: Repository;
    user_uuid: UUID;
}
export default function CategoriesList(props: CategoriesListProps) {
    const { repository, user_uuid } = props;
    const [categories, setCategories] = useState<Map<UUID, CategotyCompletedRecord>>(new Map());

    const getData = useCallback(async () => {
        const category_list = await repository.category.get_all_completed();
        setCategories(arrayToMap(category_list));
    }, [repository]);
    const newCategory = useCallback(async () => {
        const result = await repository.category.post_completed(standart_post_data);
        
        const new_map = new Map(categories)
        new_map.set(result.uuid, result)
        setCategories(new_map)
    }, [repository, user_uuid, categories]);
    const updateCategory = useCallback(
        (uuid: UUID, new_category?: CategotyCompletedRecord) => {
            const new_map = new Map(categories);
            if (new_category == undefined) {
                new_map.delete(uuid);
            } else {
                new_map.set(uuid, new_category);
            }

            setCategories(new_map);
        },
        [categories, setCategories]
    );

    useEffect(() => {
        getData();
    }, [getData]);

    return (
        <section>
            <h2>Categories</h2>
            <button onClick={newCategory}>New Category</button>
            {Array.from(categories.keys()).map((uuid) => {
                return (<CategoryItem
                    key={uuid}
                    category={categories.get(uuid)!}
                    setCategory={(new_category) => {
                        updateCategory(uuid, new_category);
                    }}
                    repository={repository!}
                />);
            })}
        </section>
    );
}