"use client";
import Head from "next/head";
import { PageContext, type PageContextType } from "@/context/pageContext";
import Link from "next/link";
import { useContext, useState } from "react";
import { CategorySelector, SelectedCategoryObject } from "@/components/categorySelector";

export default function Home() {
    const context = useContext(PageContext);

    return (
        <>
            <Head>
                <title>Timer</title>
                <meta name="description" content="Descrição da minha página" />
            </Head>
            {context && <Main context={context} />}
            <footer>
                <Link href="/">Home</Link>
            </footer>
        </>
    );
}

type MainProps = {
    context: PageContextType;
};
function Main(props: MainProps) {
    const [selected, setSelected] = useState<SelectedCategoryObject | undefined>(undefined);

    return (
        <main>
            <h1>Timer</h1>
            <section>
                sdkjnfoidwsniofndsof{" "}
                <CategorySelector categories={props.context.categories} selected={selected} setItem={setSelected} />{" "}
                sakodnsoiandiusandknsa <br />
                iodsnbfiujonsdiufndsuijn
            </section>
        </main>
    );
}
