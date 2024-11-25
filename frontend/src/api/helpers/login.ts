import { Base } from "./base";
import type { UUID } from "crypto";
import type { UserRecord } from "../types/login";
import { base_URL } from "./base";

export class Login {
    protected http:string;
    public constructor() {
        this.http = base_URL + "login/"
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
        console.warn(response)

        return response.json();
    }
}