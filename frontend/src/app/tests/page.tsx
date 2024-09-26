"use client"
import Link from "next/link"

export default function Page(){
    return <>
        <h1>Tests</h1>
        <Link href="/tests/todo">ToDo list</Link>
    </>
}