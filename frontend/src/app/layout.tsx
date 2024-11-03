"use client";
import { Inter } from "next/font/google";
import "@/styles/globals.scss";
import { PageProvider } from "@/context/pageContext";
import React from "react";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    const bodyClassName = inter.className;

    return (
        <html lang="pt-br">
            <body className={bodyClassName}>
                <PageProvider>{children}</PageProvider>
            </body>
        </html>
    );
}
