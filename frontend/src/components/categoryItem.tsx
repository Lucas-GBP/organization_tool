import style from "@/styles/components/categoryItem.module.scss";

import { useContext, useCallback } from "react";
import { UUID } from "crypto";

import type { CategoryRecord } from "@/api/types/category";
import type { Category } from "@/api/category";
import { PageContext } from "@/context/pageContext";

export interface CategoryItemProps {
    item:CategoryRecord,
    api:Category,
    updateList: () => void,
};
export function CategoryItem(props:CategoryItemProps){
    const {item, api, updateList} = props;
    const context = useContext(PageContext);

    const deleteItem = useCallback(async () => {
        const deleted = await api.delete(item.uuid);
        updateList();
    }, [item, context?.user_uuid])
    const updateItem = useCallback(async () => {
    }, []);
    const deleteSubItem = useCallback(async (uuid: UUID) => {
        const deleted = await api.delete_sub(uuid);
        updateList();
    }, [context?.user_uuid])
    const updateSubItem = useCallback(async () => {
    }, []);

    return <div className={style.categoryItem}>
        Title: <input value={item.title}/> Color: <input value={item.color}/>
        <button onClick={deleteItem}>Delete</button>
        <div className={style.subCategorySection}>
            {item.sub_categories.map((sub) => {
                return <div key={sub.uuid}>
                    Title: <input value={sub.title}/> Color: <input value={sub.color}/>
                    <button onClick={() => deleteSubItem(sub.uuid)}>Delete</button>
                </div>
            })}
        </div>
    </div>
}