import type { UUID } from "crypto";
import type { Color } from "@/types/color";

export interface SubCategoryAPI {
    uuid: UUID;
    title: string;
    color: Color;
}

export interface CategoryAPI {
    uuid: UUID;
    title: string;
    description: string;
    color: Color;
}

export interface CategoryCompletedAPI extends CategoryAPI {
    sub_categories?: SubCategoryAPI[];
}

export interface CategoryRecord extends CategoryAPI {}

export interface CategotyCompletedRecord extends CategoryCompletedAPI {}

export interface SubCategoryRecord extends SubCategoryAPI {}

export interface SubCategoryIntegratedPost {
    title: string;
    color: Color;
}

export interface SubCategoryPost extends SubCategoryIntegratedPost {
    category_uuid: UUID;
}

export interface CategoryPost {
    title: string;
    color?: Color;
    description?: string;
}

export interface CategoryCompletedPost extends CategoryPost {
    sub_categories?: SubCategoryIntegratedPost[];
}

export interface CategoryPatch {
    uuid: UUID;
    color?: Color;
    title?: string;
    description?: string;
}

export interface SubCategoryPatch {
    uuid: UUID;
    title?: string;
    color?: Color;
}
