import type { UUID } from "crypto";

export interface UserAPI {
    uuid: UUID,
    nickname: string
};

export interface UserRecord extends UserAPI {};
