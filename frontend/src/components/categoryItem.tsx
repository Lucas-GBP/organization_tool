import style from "@/styles/components/categoryItem.module.scss";

import { useContext, useCallback } from "react";

import type { CategoryRecord, SubCategoryRecord } from "@/api/types/category";
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
    item.color = "#aa";

    const deleteItem = useCallback(async () => {
        const deleted = await api.delete(item.uuid);
        updateList();
    }, [item, api])
    const updateItem = useCallback(async () => {
        const updated = await api.update();
        updateList();
    }, []);

    return <div className={style.categoryItem}>
        Title: <input defaultValue={item.title}/> Color: <input defaultValue={item.color}/>
        <button onClick={deleteItem}>Delete</button>
        {item.sub_categories.length > 0 ? <div className={style.subCategorySection}>
            {item.sub_categories.map((sub_item) => {
                return <SubCategoryItem
                    key={sub_item.uuid}
                    item={sub_item}
                    api={api}
                    updateList={updateList}
                />
            })}
        </div>:null}
    </div>
}

export interface SubCategoryItemProps {
    item:SubCategoryRecord,
    api:Category,
    updateList: () => void,
};
export function SubCategoryItem(props:SubCategoryItemProps){
    const {item, api, updateList} = props;
    
    const deleteSubItem = useCallback(async () => {
        const deleted = await api.delete_sub(item.uuid);
        updateList();
    }, [item, api]);
    const updateSubItem = useCallback(async () => {
        const updated = await api.update_sub();
        updateList();
    }, []);

    return (<div key={item.uuid}>
        Title: <input 
            defaultValue={item.title}
        /> 
        Color: <input
            defaultValue={item.color}
        />
        <button 
            onClick={deleteSubItem}
        > Delete </button>
    </div>)
}