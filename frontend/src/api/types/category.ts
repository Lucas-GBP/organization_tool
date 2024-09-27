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
    sub_categories: SubCategoryAPI[];
}

export interface CategoryRecord extends CategoryAPI {
}

export interface SubCategoryIntegratedPost {
    title:string;
    color:Color;

}

export interface CategoryPost {
    user_uuid: UUID;
    title:string
    color?:Color;
    description?:string;
    sub_categories?:SubCategoryIntegratedPost[];
}