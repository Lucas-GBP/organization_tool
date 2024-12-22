import type { CategotyCompletedRecord } from "@/api/types/category";

export function organizeCategories(categories_buffer: CategotyCompletedRecord[]) {
    categories_buffer.sort((a, b) => a.title.localeCompare(b.title));
    categories_buffer.forEach((category) => {
        if (category.sub_categories) {
            category.sub_categories.sort((a, b) => a.title.localeCompare(b.title));
        }
    });

    return categories_buffer;
}
