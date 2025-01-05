import Link from "next/link";
import { Main } from "@/pages/timer";
import { Metadata } from "next";

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