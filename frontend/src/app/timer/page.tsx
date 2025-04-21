import Link from "next/link";
import { Main } from "@/templates/timer";
import type { Metadata } from "next";

export const metadata: Metadata = {
    title: 'Timer',
};

export default function Home() {
    return (
        <>
            <Main />
            <footer>
                <Link href="/">Home</Link>
            </footer>
        </>
    );
}