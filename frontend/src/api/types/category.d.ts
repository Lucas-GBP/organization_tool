export interface SubCategoryAPI {
    uuid: UUID;
    title: string;
    color: string;
}

export interface CategoryAPI {
    uuid: UUID;
    title: string;
    description: string;
    color: string;
    sub_categories: SubCategoryAPI[];
}

export interface CategoryRecord extends CategoryAPI {
}

export interface SubCategoryIntegratedPost {
    title:string;
    color:string;

}

export interface CategoryPost {
    user_uuid: UUID;
    title:string
    color?:string;
    description?:string;
    sub_categories?:SubCategoryIntegratedPost[];
}