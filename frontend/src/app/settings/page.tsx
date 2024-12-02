"use client";
import { useContext } from "react";
import { PageContext } from "@/context/pageContext";
import CategoriesList from "@/components/categoriesList";

export default function Page() {
    const context = useContext(PageContext);

    return (
        <main>
            <h1>Settings</h1>
            {context?.repository && context.user_uuid?
            <CategoriesList
                repository={context.repository}
                user_uuid={context.user_uuid}
            />:<span>Loading Context...</span>}
        </main>
    );
}
