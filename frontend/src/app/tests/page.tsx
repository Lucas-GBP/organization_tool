"use client";
import Link from "next/link";

export default function Page() {
    return (<main>
        <h1>Tests</h1>
        <Link href="/tests/todo">ToDo list</Link><br/>
        <Link href="/tests/modal">Modal</Link><br/>
    </main>);
}
