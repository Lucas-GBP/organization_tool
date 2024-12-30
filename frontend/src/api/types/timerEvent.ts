import type { UUID } from "crypto";
import type { ApiDateTime } from "@/types/date";

/**
 * Backend
 */

/**
 * Backend Arguments Types
 */
export type TimeRangeEventPostAPI = {
    user_uuid:UUID
    start_time:ApiDateTime
    // Optional arguments
    category_id?:number
    sub_category_id?:number
    title?:number
    description?:string
    end_time?:ApiDateTime
}
export type TimeRangeEventPatchAPI = {
    uuid:UUID
    start_time:ApiDateTime
    // Optional arguments
    category_id?:number
    sub_category_id?:number
    title?:string
    description?:string
    end_time?:ApiDateTime
}
export type TimeRangeEventGetByRangeAPI = {
    user_uuid:UUID
    start: ApiDateTime
    end?: ApiDateTime
}
/**
 * Backend Responses Types
 */
export type TimeRangeEventNotDeletedAPI = {
    uuid:UUID;

    category_id?:number;
    sub_category_id?:number;
    title?:string;
    description?:string;
    start_time:ApiDateTime;
    end_time?:ApiDateTime;
}


/**
 * Repository
 */

/**
 * Repository Arguments
 */
export type TimeRangeEventPost = {
    start_time:Date
    // Optional arguments
    category_id?:number
    sub_category_id?:number
    title?:number
    description?:string
    end_time?:Date
}
export type TimeRangeEventPatch = {
    uuid:UUID
    start_time:Date
    // Optional arguments
    category_id?:number
    sub_category_id?:number
    title?:string
    description?:string
    end_time?:Date
}
/**
 * Repository Responses
 */
export type TimeRangeEventNotDeleted = {
    uuid:UUID;

    category_id?:number;
    sub_category_id?:number;
    title?:string;
    description?:string;
    start_time:Date
    end_time?:Date
}