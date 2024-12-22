import style from "@/styles/components/categoryItem.module.scss";
import { ChangeEvent, useCallback, useEffect, useRef } from "react";

import type {
    SubCategoryRecord,
    CategotyCompletedRecord,
    CategoryPatch,
    SubCategoryPatch,
    SubCategoryPost,
} from "@/api/types/category";
import type { Category } from "@/api/category";
import { Repository } from "@/api";
import { Input } from "@/components/fragments";
import { ColorPicker } from "antd";
import { AggregationColor } from "antd/es/color-picker/color";
import { type Color, isValidColor } from "@/types/color";

const standart_sub_category_post = (category: CategotyCompletedRecord) => {
    return {
        category_uuid: category.uuid,
        color: category.color,
        title: "New Sub Category",
    } as SubCategoryPost;
};

export interface CategoryItemProps {
    category: CategotyCompletedRecord;
    setCategory: (arg?: CategotyCompletedRecord) => void;
    repository: Repository;
}
export function CategoryItem(props: CategoryItemProps) {
    const { category, setCategory, repository } = props;
    const category_post = useRef<SubCategoryPost>(standart_sub_category_post(category));

    const getSubCategories = useCallback(async () => {
        const sub_categories = await repository.category.get_sub_all(category.uuid);

        setCategory({
            ...category,
            sub_categories: sub_categories,
        });
    }, [repository, category, setCategory]);
    const deleteItem = useCallback(async () => {
        const deleted = await repository.category.delete(category.uuid);

        setCategory(deleted);
    }, [category, repository, setCategory]);
    const updateItem = useCallback(
        async (data: CategoryPatch) => {
            const updated = await repository.category.update(data);
            setCategory({
                ...updated,
                sub_categories: category.sub_categories,
            });
        },
        [repository, category, setCategory]
    );
    const newSubCategory = useCallback(async () => {
        const new_sub = await repository.category.post_sub(category_post.current);
        const category_copy = category;
        if (!category_copy.sub_categories) {
            category_copy.sub_categories = [];
        }
        category_copy.sub_categories.push(new_sub);

        setCategory(category_copy);
    }, [repository, category, category_post, setCategory]);

    const updateSubCategory = useCallback(
        (index: number, new_sub?: SubCategoryRecord) => {
            if (!category.sub_categories) {
                return;
            }
            const new_sub_category = category.sub_categories;

            //Se o new_sub for undefine significa que ele foi deletado
            if (new_sub == undefined) {
                new_sub_category.splice(index, 1);
            } else {
                new_sub_category[index] = new_sub;
            }
            setCategory({
                ...category,
                sub_categories: new_sub_category,
            });
        },
        [category, setCategory]
    );
    const updateTitle = useCallback(
        (e: ChangeEvent<HTMLInputElement>) => {
            updateItem({
                ...category,
                title: e.target.value,
            });
        },
        [updateItem, category]
    );
    const updateColor = useCallback(
        (value: AggregationColor) => {
            const color = value.toHexString();
            if (!isValidColor(color)) {
                return;
            }

            updateItem({
                ...category,
                color: color as Color,
            });
        },
        [updateItem, category]
    );

    useEffect(() => {
        category_post.current = standart_sub_category_post(category);
    }, [category]);
    useEffect(() => {
        if (category.sub_categories == undefined) {
            getSubCategories();
        }
    }, [category, getSubCategories]);

    return (
        <div className={style.categoryItem} key={"category:" + category.uuid}>
            Title: <Input className={style.titleInput} defaultValue={category.title} onBlur={updateTitle} />
            Color: <ColorPicker defaultValue={category.color} onChangeComplete={updateColor} />
            <button onClick={deleteItem}>Delete</button>
            <button onClick={newSubCategory}>New Sub Category</button>
            {category.sub_categories && category.sub_categories.length > 0 ? (
                <div className={style.subCategorySection}>
                    {category.sub_categories.map((sub_item, index) => {
                        return (
                            <SubCategoryItem
                                key={sub_item.uuid}
                                item={sub_item}
                                updateList={(new_sub) => {
                                    updateSubCategory(index, new_sub);
                                }}
                                api={repository.category}
                            />
                        );
                    })}
                </div>
            ) : null}
        </div>
    );
}

export interface SubCategoryItemProps {
    item: SubCategoryRecord;
    api: Category;
    updateList: (arg?: SubCategoryRecord) => void;
}
export function SubCategoryItem(props: SubCategoryItemProps) {
    const { updateList, api, item } = props;

    const deleteSubItem = useCallback(async () => {
        const deleted = await api.delete_sub(item.uuid);
        updateList(deleted);
    }, [item, updateList, api]);
    const updateSubItem = useCallback(
        async (data: SubCategoryPatch) => {
            const updated = await api.update_sub(data);
            updateList(updated);
        },
        [api, updateList]
    );

    const updateTitle = useCallback(
        (e: ChangeEvent<HTMLInputElement>) => {
            updateSubItem({
                ...item,
                title: e.target.value,
            });
        },
        [updateSubItem, item]
    );
    const updateColor = useCallback(
        (value: AggregationColor) => {
            const color = value.toHexString();
            if (!isValidColor(color)) {
                return;
            }

            updateSubItem({
                ...item,
                color: color as Color,
            });
        },
        [updateSubItem, item]
    );

    return (
        <div key={"sub_category:" + item.uuid}>
            Title: <Input defaultValue={item.title} className={style.titleInput} onBlur={updateTitle} />
            Color: <ColorPicker defaultValue={item.color} onChangeComplete={updateColor} />
            <button onClick={deleteSubItem}> Delete </button>
        </div>
    );
}
