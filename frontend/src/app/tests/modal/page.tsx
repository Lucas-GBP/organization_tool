"use client";
import { useState } from "react";
import { BaseModal } from "@/components";

export default function Page() {
    const [isModalOpen, setModalOpen] = useState(false);

    return (
        <main>
            <h1>Modal Teste</h1>
            <div>
                <button onClick={() => setModalOpen(true)}>Open Modal</button>
                <BaseModal isOpen={isModalOpen} onClose={() => setModalOpen(false)}>
                    <h2>Modal Title</h2>
                    <p>This is the modal content.</p>
                </BaseModal>
            </div>
        </main>
    );
}
