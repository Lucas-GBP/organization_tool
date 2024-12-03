import type { UserRecord } from "../types/login";
import { base_URL } from "./base";
import { RequestInit } from "next/dist/server/web/spec-extension/request";

export class Login {
    protected http: string;
    public constructor() {
        this.http = base_URL + "login/";
    }

    protected fetch(input: string, init?: RequestInit): Promise<Response> {
        if (init) {
            init.headers = {
                "Content-Type": "application/json",
            };
        }

        return fetch(this.http + input, init);
    }

    public async get_test(): Promise<UserRecord> {
        const response = await this.fetch("test/", {
            method: "GET",
        });

        return response.json();
    }
}
