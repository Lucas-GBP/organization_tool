"use client";
import Link from "next/link";
import { UUID } from "crypto";
import { useEffect, useState, useCallback, useContext, useRef } from "react";
import { CategoryItem } from "@/components";
import { PageContext } from "@/context/pageContext";
import type { CategoryPost, CategotyCompletedRecord } from "@/api/types/category";
import { arrayToMap } from "@/utils/arrayToMap";
import { Repository } from "@/api";
import { organizeCategories } from "@/utils/organizeCategories";


export default function Page() {
    const context = useContext(PageContext);

    useEffect(() => {
        context?.get_categories();
        return () => {
            context?.get_categories();
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <main>
            <h1>Settings</h1>
            {context?.repository && context.categories ? (
                <CategoriesList repository={context.repository} categorires={context.categories} />
            ) : (
                <span>Loading Context...</span>
            )}
            <Link href="/">Home</Link>
        </main>
    );
}

export interface CategoriesListProps {
    repository: Repository;
    categorires: CategotyCompletedRecord[];
}
export function CategoriesList(props: CategoriesListProps) {
    const { repository } = props;
    const [categories, setCategories] = useState<Map<UUID, CategotyCompletedRecord>>(arrayToMap(props.categorires));
    const standart_post_data = useRef<CategoryPost>({
        title: "New Category",
        color: "#ffffff",
        description: undefined,
    });

    const getData = useCallback(async () => {
        const category_list = await repository.category.get_all_completed();
        organizeCategories(category_list);
        setCategories(arrayToMap(category_list));
    }, [repository]);
    const newCategory = useCallback(async () => {
        const result = await repository.category.post_completed(standart_post_data.current);

        const new_map = new Map(categories);
        new_map.set(result.uuid, result);
        setCategories(new_map);
    }, [repository, categories]);
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
                return (
                    <CategoryItem
                        key={uuid}
                        category={categories.get(uuid)!}
                        setCategory={(new_category) => {
                            updateCategory(uuid, new_category);
                        }}
                        repository={repository!}
                    />
                );
            })}
        </section>
    );
}
