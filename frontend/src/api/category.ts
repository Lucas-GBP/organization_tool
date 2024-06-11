import { Base } from "./_base";

interface CategoryAPI {
    id: number;
    user_id: number;
}

export interface CategoryRecord extends CategoryAPI {
}

export class Category extends Base {
    public constructor(){
        super();
        this.http = this.http+"category/";
    };
    public async get(user_id:number): Promise<CategoryRecord[]> {
        const response = await fetch(this.http+user_id, {
            method:"GET"
        });

        return response.json()
    }
}