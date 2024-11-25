import style from "@/styles/components/categoryItem.module.scss";

import { useCallback } from "react";

import type { CategoryRecord, SubCategoryRecord } from "@/api/types/category";
import type { Category } from "@/api/category";

export interface CategoryItemProps {
    item: CategoryRecord;
    api: Category;
    updateList: () => void;
}
export function CategoryItem(props: CategoryItemProps) {
    const { item, api, updateList } = props;
    //const context = useContext(PageContext);

    const deleteItem = useCallback(async () => {
        const deleted = await api.delete(item.uuid);
        console.log(deleted);
        updateList();
    }, [item, api, updateList]);
    /*const updateItem = useCallback(async () => {
        const updated = await api.update();
        updateList();
    }, [api, updateList]);*/

    return (
        <div className={style.categoryItem}>
            Title: <input defaultValue={item.title} /> Color: <input defaultValue={item.color} />
            <button onClick={deleteItem}>Delete</button>
            {item.sub_categories !== undefined && item.sub_categories.length > 0 ? (
                <div className={style.subCategorySection}>
                    {item.sub_categories.map((sub_item) => {
                        return (
                            <SubCategoryItem key={sub_item.uuid} item={sub_item} api={api} updateList={updateList} />
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
    const { item, api, updateList } = props;

    const deleteSubItem = useCallback(async () => {
        const deleted = await api.delete_sub(item.uuid);
        console.log(deleted);
        updateList();
    }, [item, api, updateList]);
    /*const updateSubItem = useCallback(async () => {
        const updated = await api.update_sub();
        updateList();
    }, [api, updateList]);*/

    return (
        <div key={item.uuid}>
            Title: <input defaultValue={item.title} />
            Color: <input defaultValue={item.color} />
            <button onClick={deleteSubItem}> Delete </button>
        </div>
    );
}
