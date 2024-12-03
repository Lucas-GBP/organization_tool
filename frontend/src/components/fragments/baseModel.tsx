import style from "@/styles/components/fragments/baseModel.module.scss";

import { useEffect, useRef, useCallback, type ReactNode } from "react";

export interface BaseModalProps {
    isOpen: boolean; // Controla se o modal está visível
    onClose: () => void; // Função chamada ao fechar o modal
    children: ReactNode; // Conteúdo do modal
}
export function BaseModal(props: BaseModalProps) {
    const { isOpen, onClose, children } = props;
    const modalRef = useRef<HTMLDivElement>(null);

    // Fechar modal ao clicar fora do conteúdo
    const handleClickOutside = useCallback(
        (event: MouseEvent) => {
            if (modalRef.current && !modalRef.current.contains(event.target as Node)) {
                onClose();
            }
        },
        [modalRef, onClose]
    );

    // Adicionar/remover listener para cliques fora do modal
    useEffect(() => {
        if (isOpen) {
            document.addEventListener("mousedown", handleClickOutside);
        } else {
            document.removeEventListener("mousedown", handleClickOutside);
        }
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [isOpen, handleClickOutside]);

    return (
        isOpen && (
            <div className={style.modalOverlay}>
                <div className={style.modalContainer} ref={modalRef}>
                    <button className={style.modalCloseButton} onClick={onClose}>
                        &times; {/* Símbolo de "fechar" */}
                    </button>
                    <div className={style.modalContent}>{children}</div>
                </div>
            </div>
        )
    );
}
