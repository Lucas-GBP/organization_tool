import { Base } from "./helpers/base";
import { apiDateToDate, dateToApiDate } from "@/types/date";
import type { UUID } from "crypto";
import type {
    TimeRangeEventNotDeletedAPI, TimeRangeEventNotDeleted,
    TimeRangeEventGetByRangeAPI,
    TimeRangeEventPatchAPI, TimeRangeEventPatch,
    TimeRangeEventPostAPI, TimeRangeEventPost
} from "./types/timerEvent";

export class TimerEvent extends Base {
    public constructor(user_uuid: UUID) {
        super("timer_event/", user_uuid);
    }
    private parseObject(apiObject:TimeRangeEventNotDeletedAPI): TimeRangeEventNotDeleted{
        return {
            ...apiObject,
            start_time: apiDateToDate(apiObject.start_time),
            end_time: apiObject.end_time?apiDateToDate(apiObject.end_time):undefined
        };
    }
    private parsePostObject(postObject: TimeRangeEventPost): TimeRangeEventPostAPI {
        return {
            ...postObject,
            user_uuid: this.user_uuid,
            start_time: dateToApiDate(postObject.start_time),
            end_time:postObject.end_time? dateToApiDate(postObject.end_time):undefined
        };
    }
    private parsePatchObject(patchObject: TimeRangeEventPatch): TimeRangeEventPatchAPI{
        return {
            ...patchObject,
            start_time: dateToApiDate(patchObject.start_time),
            end_time: patchObject.end_time?dateToApiDate(patchObject.end_time):undefined
        };
    }
    public async get(uuid: UUID): Promise<TimeRangeEventNotDeleted>{
        const response = await this.fetch(uuid, {
            method: "GET",
        });
        const respose_json = await response.json() as TimeRangeEventNotDeletedAPI;

        return this.parseObject(respose_json);
    }
    public async post(obj: TimeRangeEventPost): Promise<TimeRangeEventNotDeleted>{
        const response = await (await this.fetch("", {
            method: "POST",
            body: JSON.stringify(this.parsePostObject(obj))
        })).json() as TimeRangeEventNotDeletedAPI

        return this.parseObject(response)
    }
    public async patch(obj: TimeRangeEventPatch): Promise<TimeRangeEventNotDeleted>{
        const response = await (await this.fetch("", {
            method: "PATCH",
            body: JSON.stringify(this.parsePatchObject(obj))
        })).json() as TimeRangeEventNotDeletedAPI

        return this.parseObject(response)
    }
    public async get_by_range(start: Date, end?:Date): Promise<TimeRangeEventNotDeleted[]>{
        const data = {
            user_uuid: this.user_uuid,
            start: start.toUTCString(),
            end: end?end.toUTCString():undefined
        } as TimeRangeEventGetByRangeAPI;
        const data_json = JSON.stringify(data);

        const response = await this.fetch("range", {
            method: "GET",
            body: data_json
        });
        const response_json = await response.json() as TimeRangeEventNotDeletedAPI[]

        return response_json.map((item) => this.parseObject(item));
    }
    public async get_running(): Promise<TimeRangeEventNotDeleted>{
        const response = await this.fetch("running/"+this.user_uuid, {
            method: "GET",
        });
        const respose_json = await response.json() as TimeRangeEventNotDeletedAPI;

        return this.parseObject(respose_json);
    }
    
}