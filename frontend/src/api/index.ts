import { Category } from "./category";
import { UUID } from "crypto";

export class Repository {
    protected user_uuid:UUID;
    public category:Category;

    public constructor(user_uuid: UUID) {
        this.user_uuid = user_uuid;
        this.category = new Category(user_uuid);
    }
}