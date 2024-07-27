import { useMemo, useContext, useCallback } from "react";

import type { CategoryRecord } from "@/api/types/category";
import type { Category } from "@/api/category";
import style from "@/styles/components/categoryItem.module.scss";
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
        console.log({deleted})
        updateList();
    }, [item, context?.user_uuid])

    return <div className={style.categoryItem}>
        {item.title}
        <button onClick={deleteItem}>Delete</button>
    </div>
}