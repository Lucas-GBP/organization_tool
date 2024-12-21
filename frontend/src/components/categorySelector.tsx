import style from "@/styles/components/categorySelector.module.scss";

import { useCallback, useEffect, useRef, useState } from "react";
import type { CategotyCompletedRecord, CategoryRecord, SubCategoryRecord } from "@/api/types/category";

export type SelectedCategoryObject = {
    category: CategoryRecord;
    subCategory?: SubCategoryRecord;
};

export interface CategorySelectorProps {
    categories: CategotyCompletedRecord[];
    selected?: SelectedCategoryObject;
    setItem: (arg: SelectedCategoryObject) => void;
}
export function CategorySelector(props: CategorySelectorProps) {
    const { setItem } = props;
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const [label, setLabel] = useState<string>("");

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

    useEffect(() => {
        if (props.selected?.subCategory?.title) {
            setLabel(props.selected?.subCategory?.title);
            return;
        }
        if (props.selected?.category.title) {
            setLabel(props.selected?.category.title);
            return;
        }
        setLabel("Select Category");
        return;
    }, [props.selected]);

    return (
        <span className={style.selector} onMouseLeave={() => setIsOpen(false)}>
            <button onClick={openAction}>{label}</button>
            {isOpen && (
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
