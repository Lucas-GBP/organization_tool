import { Base } from "./helpers/base";
import type { UUID } from "crypto";
import type {
    CategoryRecord,
    CategotyCompletedRecord,
    CategoryPost,
    CategoryCompletedPost,
    SubCategoryRecord,
    CategoryPatch,
    SubCategoryPost,
    SubCategoryPatch,
} from "./types/category";

export class Category extends Base {
    public constructor(user_uuid: UUID) {
        super("category/", user_uuid);
    }

    public async get(uuid: UUID): Promise<CategoryRecord> {
        const response = await this.fetch(uuid, {
            method: "GET",
        });

        return response.json();
    }

    public async post(data: CategoryPost): Promise<CategoryRecord> {
        const data_json = JSON.stringify({
            ...data,
            user_uuid: this.user_uuid
        });

        const response = await this.fetch("", {
            method: "POST",
            body: data_json,
        });

        return response.json();
    }

    public async update(data: CategoryPatch): Promise<CategoryRecord> {
        const data_json = JSON.stringify(data);

        const response = await this.fetch("", {
            method: "PATCH",
            body: data_json,
        });

        return response.json();
    }

    public async delete(uuid: UUID): Promise<CategoryRecord> {
        const response = await this.fetch(`${uuid}`, {
            method: "DELETE",
        });

        return response.json();
    }

    public async get_all(): Promise<CategoryRecord[]> {
        const response = await this.fetch("all/" + this.user_uuid, {
            method: "GET",
        });

        return response.json();
    }

    public async get_sub(subcategory_uuid: UUID): Promise<SubCategoryRecord> {
        const response = await this.fetch("subcategory/" + subcategory_uuid, {
            method: "GET",
        });

        return response.json();
    }

    public async post_sub(data: SubCategoryPost): Promise<SubCategoryRecord> {
        const data_json = JSON.stringify(data);

        const response = await this.fetch("subcategory/", {
            method: "POST",
            body: data_json,
        });

        return response.json();
    }

    public async update_sub(data: SubCategoryPatch): Promise<SubCategoryRecord> {
        const data_json = JSON.stringify(data);

        const response = await this.fetch("subcategory/", {
            method: "PATCH",
            body: data_json,
        });

        return response.json();
    }

    public async delete_sub(subcategory_uuid: UUID) {
        const response = await this.fetch(`subcategory/${subcategory_uuid}`, {
            method: "DELETE",
        });

        return response.json();
    }

    public async get_sub_all(uuid: UUID): Promise<SubCategoryRecord[]> {
        const response = await this.fetch("subcategory/all/" + uuid, {
            method: "GET",
        });

        return response.json();
    }

    public async get_completed(uuid: UUID): Promise<CategotyCompletedRecord> {
        const response = await this.fetch("complety/" + uuid, {
            method: "GET",
        });

        return response.json();
    }

    public async post_completed(post_data: CategoryCompletedPost): Promise<CategotyCompletedRecord> {
        const data = JSON.stringify({
            ...post_data,
            user_uuid: this.user_uuid
        });
        const response = await this.fetch("complety/", {
            method: "POST",
            body: data,
        });

        return response.json();
    }

    public async get_all_completed(): Promise<CategotyCompletedRecord[]> {
        const response = await this.fetch("complety/all/" + this.user_uuid, {
            method: "GET",
        });

        return response.json();
    }
}
