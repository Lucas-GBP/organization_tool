import { RequestInit } from "next/dist/server/web/spec-extension/request";

export class Base {
    protected base_URL = "http://127.0.0.1:8888/";
    protected http = this.base_URL;

    public constructor(endpoint: string) {
        this.http = this.http + endpoint;
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
