"use client";
import { PageContext } from "@/context/pageContext";
import Link from "next/link";
import { useContext, useState } from "react";
import { SelectedCategoryObject } from "@/components/categorySelector";

export default function Home() {
    const context = useContext(PageContext)
    const [selected, setSelected] = useState<SelectedCategoryObject|undefined>(undefined);

    return (<>
        <main>
            <h1>Timer</h1>
        </main>
        <footer>
            <Link href="/">Home</Link>
        </footer>
    </>);
}
