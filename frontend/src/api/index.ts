import { Category } from "./category";
import { TimerEvent } from "./timerEvent";
import { UUID } from "crypto";

export class Repository {
    protected user_uuid: UUID;
    public category: Category;
    public timerEvent: TimerEvent;

    public constructor(user_uuid: UUID) {
        this.user_uuid = user_uuid;
        this.category = new Category(user_uuid);
        this.timerEvent = new TimerEvent(user_uuid);
    }
}
