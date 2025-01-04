import type { UUID } from "crypto";
import type { CategotyCompletedRecord } from "@/api/types/category";
import type { SelectedCategoryObject } from "@/components";

export function findCategory(
    categories: CategotyCompletedRecord[],
    category?: UUID,
    sub_category?: UUID
): SelectedCategoryObject | undefined {
    if (!category) {
        return undefined;
    }

    const foundCategory = categories.find((item) => item.uuid === category);
    if (!foundCategory) {
        return undefined;
    }

    if (!foundCategory.sub_categories || !sub_category) {
        return {
            category: foundCategory,
        };
    }

    const foudedSubCategory = foundCategory.sub_categories.find((item) => item.uuid === sub_category);
    if (!foudedSubCategory) {
        return undefined;
    }

    return {
        category: foundCategory,
        subCategory: foudedSubCategory,
    };
}
