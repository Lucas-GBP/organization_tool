import type { UUID } from "crypto";
import type { ColorType } from "./color";

export interface SubCategoryAPI {
    uuid: UUID;
    title: string;
    color: ColorType;
}

export interface CategoryAPI {
    uuid: UUID;
    title: string;
    description: string;
    color: ColorType;
    sub_categories: SubCategoryAPI[];
}

export interface CategoryRecord extends CategoryAPI {
}

export interface SubCategoryIntegratedPost {
    title:string;
    color:ColorType;
}

export interface CategoryPost {
    user_uuid: UUID;
    title:string
    color?:ColorType;
    description?:string;
    sub_categories?:SubCategoryIntegratedPost[];
}

export interface SubCategoryPatch {
    uuid: UUID;
    title?: string;
    color?: ColorType;
}
export interface CategoryPatch {
    uuid: UUID;
    color?: ColorType;
    title?: string;
    description?: string;
}