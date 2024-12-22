import style from "@/styles/components/categorySelector.module.scss";

import { useCallback, useMemo, useRef, useState } from "react";
import type { CategotyCompletedRecord, CategoryRecord, SubCategoryRecord } from "@/api/types/category";

export type SelectedCategoryObject = {
    category: CategoryRecord;
    subCategory?: SubCategoryRecord;
};

export interface CategorySelectorProps {
    categories?: CategotyCompletedRecord[];
    selected?: SelectedCategoryObject;
    setItem: (arg: SelectedCategoryObject) => void;
}
export function CategorySelector(props: CategorySelectorProps) {
    const { setItem } = props;
    const [isOpen, setIsOpen] = useState<boolean>(false);

    const openAction = useCallback(() => {
        setIsOpen(!isOpen);
    }, [isOpen]);
    const setLocalItem = useCallback(
        (arg: SelectedCategoryObject) => {
            setItem(arg);
            setIsOpen(false);
        },
        [setItem, setIsOpen]
    );

    const button = useMemo(() => {
        if (props.selected?.subCategory?.title) {
            return (
                <span 
                    className={style.button} 
                    onClick={openAction}
                    style={{
                        borderColor: props.selected.subCategory.color
                    }}
                >
                    {props.selected?.subCategory?.title}
                </span>
            );
        }
        if (props.selected?.category.title) {
            return (
                <span 
                    className={style.button} 
                    onClick={openAction}
                    style={{
                        borderColor: props.selected.category.color
                    }}
                >
                    {props.selected?.category.title}
                </span>
            );
        }

        return (
            <span className={style.button} onClick={openAction}>
                Select Category
            </span>
        );
    }, [props.selected, openAction]);

    return (
        <span className={style.selector} onMouseLeave={() => setIsOpen(false)}>
            {button}
            {isOpen && props.categories && (
                <div className={style.list}>
                    {props.categories.map((value) => {
                        return <Item key={value.uuid} item={value} setItem={setLocalItem} />;
                    })}
                </div>
            )}
        </span>
    );
}

type ItemProps = {
    item: CategotyCompletedRecord;
    setItem: (arg: SelectedCategoryObject) => void;
};
function Item(props: ItemProps) {
    const { item } = props;
    const onSubList = useRef(false);
    const [isExtended, setIsExtended] = useState(false);

    const openSubList = useCallback(() => {
        if (item.sub_categories?.length && item.sub_categories?.length > 0) {
            setIsExtended(true);
        }
    }, [item, setIsExtended]);
    const closeSubList = useCallback(() => {
        setIsExtended(false);
    }, [setIsExtended]);

    return (
        <div
            className={style.item}
            style={{
                borderColor: item.color,
            }}
            onClick={() => {
                if (!onSubList.current) {
                    props.setItem({ category: item });
                }
            }}
            onMouseEnter={openSubList}
            onMouseLeave={closeSubList}
        >
            <span>{item.title}</span>
            {isExtended && item.sub_categories && (
                <span
                    className={style.subList}
                    onMouseEnter={() => {
                        onSubList.current = true;
                    }}
                    onMouseLeave={() => {
                        onSubList.current = false;
                    }}
                >
                    {item.sub_categories.map((subItem) => {
                        return (
                            <SubItem
                                key={subItem.uuid}
                                subItem={subItem}
                                setSubItem={() => {
                                    props.setItem({
                                        category: item,
                                        subCategory: subItem,
                                    });
                                }}
                            />
                        );
                    })}
                </span>
            )}
        </div>
    );
}

type SubItemProps = {
    subItem: SubCategoryRecord;
    setSubItem: () => void;
};
function SubItem(props: SubItemProps) {
    return (
        <div
            className={style.subItem}
            style={{
                borderColor: props.subItem.color,
            }}
            onClick={props.setSubItem}
        >
            {props.subItem.title}
        </div>
    );
}
