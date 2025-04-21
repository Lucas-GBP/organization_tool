import type { Metadata } from "next";
import { Main } from "@/templates/settings";

export const metadata: Metadata = {
    title: 'Settings',
};


export default function Page() {

    return (<>
        <Main />
    </>);
}