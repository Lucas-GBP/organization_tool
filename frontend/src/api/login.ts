import { Base } from "./_base";
import type { UUID } from "crypto";
import type { UserRecord } from "./types/login";

export class Login extends Base {
    public constructor() {
        super("login/");
    }

    public async get_test(): Promise<UserRecord> {
        const response = await this.fetch("test/", {
            method: "GET",
        });
        console.warn(response)

        return response.json();
    }
}