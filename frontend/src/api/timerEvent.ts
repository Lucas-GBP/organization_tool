import { Base } from "./helpers/base";
import { apiDateToDate, dateToApiDate } from "@/types/date";
import type { UUID } from "crypto";
import type {
    TimeRangeEventNotDeletedAPI,
    TimeRangeEventNotDeleted,
    TimeRangeEventGetByRangeAPI,
    TimeRangeEventPatchAPI,
    TimeRangeEventPatch,
    TimeRangeEventPostAPI,
    TimeRangeEventPost,
} from "./types/timerEvent";

export class TimerEvent extends Base {
    public constructor(user_uuid: UUID) {
        super("timer_event/", user_uuid);
    }
    private parseObject(apiObject: TimeRangeEventNotDeletedAPI): TimeRangeEventNotDeleted {
        return {
            ...apiObject,
            start_time: apiDateToDate(apiObject.start_time),
            end_time: apiObject.end_time ? apiDateToDate(apiObject.end_time) : undefined,
        };
    }
    private parsePostObject(postObject: TimeRangeEventPost): TimeRangeEventPostAPI {
        return {
            ...postObject,
            user_uuid: this.user_uuid,
            start_time: dateToApiDate(postObject.start_time),
            end_time: postObject.end_time ? dateToApiDate(postObject.end_time) : undefined,
        };
    }
    private parsePatchObject(patchObject: TimeRangeEventPatch): TimeRangeEventPatchAPI {
        return {
            ...patchObject,
            start_time: dateToApiDate(patchObject.start_time),
            end_time: patchObject.end_time ? dateToApiDate(patchObject.end_time) : undefined,
        };
    }
    public async get(uuid: UUID): Promise<TimeRangeEventNotDeleted> {
        const response = await this.fetch(uuid, {
            method: "GET",
        });
        if (response.ok) {
            const respose_json = (await response.json()) as TimeRangeEventNotDeletedAPI;

            return this.parseObject(respose_json);
        } else {
            throw new Error("error trying to get TimerEvent.");
        }
    }
    public async post(obj: TimeRangeEventPost): Promise<TimeRangeEventNotDeleted> {
        const response = await this.fetch("", {
            method: "POST",
            body: JSON.stringify(this.parsePostObject(obj)),
        });
        if (response.ok) {
            const respose_json = (await response.json()) as TimeRangeEventNotDeletedAPI;

            return this.parseObject(respose_json);
        }
        throw new Error("error trying to post TimerEvent.");
    }
    public async patch(obj: TimeRangeEventPatch): Promise<TimeRangeEventNotDeleted> {
        console.warn({ obj });
        const response = await this.fetch("", {
            method: "PATCH",
            body: JSON.stringify(this.parsePatchObject(obj))
        });
        if (response.ok) {
            const respose_json = (await response.json()) as TimeRangeEventNotDeletedAPI;

            return this.parseObject(respose_json);
        }
        throw new Error("error trying to patch TimerEvent.");
    }
    public async delete(uuid: UUID): Promise<UUID> {
        const response = await this.fetch(uuid, {
            method: "DELETE",
        });
        if (response.ok) {
            const respose_json = (await response.json()) as UUID;

            return respose_json;
        } else {
            throw new Error("error trying to delete.");
        }
    }
    public async get_by_range(start: Date, end?: Date): Promise<TimeRangeEventNotDeleted[]> {
        const data = {
            user_uuid: this.user_uuid,
            start: dateToApiDate(start),
            end: end ? dateToApiDate(end) : undefined,
        } as TimeRangeEventGetByRangeAPI;
        const params = new URLSearchParams(data).toString();

        const response = await this.fetch(`range?${params}`, {
            method: "GET",
        });
        if (response.ok) {
            const response_json = (await response.json()) as TimeRangeEventNotDeletedAPI[];

            return response_json.map((item) => {
                return this.parseObject(item);
            });
        }
        console.error({ response });
        throw new Error("error trying to get TimerEvent with Range.");
    }
    public async get_running(): Promise<TimeRangeEventNotDeleted | undefined> {
        const response = await this.fetch("running/" + this.user_uuid, {
            method: "GET",
        });
        const respose_json = (await response.json()) as TimeRangeEventNotDeletedAPI | undefined;

        return respose_json ? this.parseObject(respose_json) : undefined;
    }
}
