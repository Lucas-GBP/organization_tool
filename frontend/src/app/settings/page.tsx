"use client";
import { useContext, useEffect } from "react";
import Link from "next/link";
import { PageContext } from "@/context/pageContext";
import { CategoriesList } from "@/components/categoriesList";

export default function Page() {
    const context = useContext(PageContext);

    useEffect(() => {
        context?.get_categories();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <main>
            <h1>Settings</h1>
            {context?.repository && context.categories ? (
                <CategoriesList repository={context.repository} categorires={context.categories} />
            ) : (
                <span>Loading Context...</span>
            )}
            <Link href="/">Home</Link>
        </main>
    );
}
