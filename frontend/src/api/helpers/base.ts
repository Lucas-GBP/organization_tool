import { RequestInit } from "next/dist/server/web/spec-extension/request";
import { UUID } from "crypto";

export const base_URL = "http://127.0.0.1:8888/";

export class Base {
    protected base_URL = base_URL;
    protected http = this.base_URL;
    protected user_uuid: UUID;

    public constructor(endpoint: string, user_uuid: UUID) {
        this.http = this.http + endpoint;
        this.user_uuid = user_uuid;
    }

    protected fetch(input: string, init?: RequestInit): Promise<Response> {
        if (init) {
            init.headers = {
                "Content-Type": "application/json",
            };
        }

        return fetch(this.http + input, init);
    }
}
