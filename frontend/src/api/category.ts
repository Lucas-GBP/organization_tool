import { Base } from "./_base";
import { UUID } from "crypto";
import type { CategoryRecord, CategoryPost } from "./types/category";

export class Category extends Base {
    public constructor(){
        super();
        this.http = this.http+"category/";
    }

    public async get(uuid:UUID): Promise<CategoryRecord> {
        const response = await this.fetch(uuid, {
            method:"GET"
        });

        return response.json()
    }

    public async get_all(user_uuid:UUID): Promise<CategoryRecord[]> {
        const response = await this.fetch("all/"+user_uuid, {
            method:"GET"
        });
        
        return response.json();
    }

    public async post(post_data:CategoryPost): Promise<CategoryRecord>{
        const data = JSON.stringify(post_data);
        const response = await this.fetch("", {
            method:"POST",
            body: data
        });

        return response.json();
    }

    public async delete(uuid:UUID): Promise<CategoryRecord>{
        const response = await this.fetch(`${uuid}`,{
            method:"DELETE"
        });

        return response.json()
    }
}