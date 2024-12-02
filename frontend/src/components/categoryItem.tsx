import style from "@/styles/components/categoryItem.module.scss";
import { ChangeEvent, useCallback, useEffect, useState } from "react";

import type { 
    CategoryRecord, 
    SubCategoryRecord, 
    CategotyCompletedRecord,
    CategoryPatch
} from "@/api/types/category";
import type { Category } from "@/api/category";
import { Repository } from "@/api";
import { Input } from "@/components/fragments";
import { ColorPicker } from "antd";
import { AggregationColor } from "antd/es/color-picker/color";
import { type Color, isValidColor } from "@/types/color";

export interface CategoryItemProps {
    item: CategoryRecord;
    updateList: () => void;
    repository: Repository;
}
export function CategoryItem(props: CategoryItemProps) {
    const { updateList, repository } = props;
    const [category, setCategory] = useState<CategotyCompletedRecord>(props.item)

    const getSubCategories = useCallback(async () => {
        const sub_categories = await repository.category.get_sub_all(category.uuid)

        setCategory({
            ...category,
            sub_categories: sub_categories,
        });
    }, [category])
    const deleteItem = useCallback(async () => {
        const deleted = await repository.category.delete(category.uuid);

        updateList();
        getSubCategories();
    }, [category, updateList, repository]);
    const updateItem = useCallback(async (data:CategoryPatch) => {
        const updated = await repository.category.update(data);
        setCategory({
            ...updated,
            sub_categories:category.sub_categories
        })
    }, [repository, updateList]);

    const updateTitle = useCallback((e:ChangeEvent<HTMLInputElement>) => {
        updateItem({
            ...category,
            title:e.target.value,
        })
    }, [updateItem])
    const updateColor = useCallback((value: AggregationColor) => {
        const color = value.toHexString();
        console.log(color);
        if(!isValidColor(color)){
            return;
        }

        updateItem({
            ...category,
            color:color as Color,
        })
    }, [updateItem])

    useEffect(()=> {
        if(category.sub_categories == undefined){
            getSubCategories();
        }
    }, [category])


    return (
        <div className={style.categoryItem} key={"category:"+category.uuid}>
            Title: <Input 
                defaultValue={category.title}
                onBlur={updateTitle}
            /> 
            Color: <ColorPicker 
                defaultValue={category.color} 
                onChangeComplete={updateColor}
            />
            <button onClick={deleteItem}>Delete</button>
            {category.sub_categories !== undefined && category.sub_categories.length > 0 ? (
                <div className={style.subCategorySection}>
                    {category.sub_categories.map((sub_item) => {
                        return (
                            <SubCategoryItem
                                key={sub_item.uuid}
                                item={sub_item}
                                updateList={getSubCategories}
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
    updateList: () => void;
}
export function SubCategoryItem(props: SubCategoryItemProps) {
    const { item, updateList, api } = props;

    const deleteSubItem = useCallback(async () => {
        const deleted = await api.delete_sub(item.uuid);
        console.log(deleted);
        updateList();
    }, [item, updateList, api]);
    const updateSubItem = useCallback(async () => {
        const updated = await api.update_sub();
        updateList();
    }, [api, updateList]);

    return (
        <div key={"sub_category:"+item.uuid}>
            Title: <Input defaultValue={item.title} />
            Color: <ColorPicker defaultValue={item.color} />
            <button onClick={deleteSubItem}> Delete </button>
        </div>
    );
}
