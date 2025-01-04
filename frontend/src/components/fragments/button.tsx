import style from "@/styles/components/fragments/button.module.scss";
import { DetailedHTMLProps, ButtonHTMLAttributes } from "react";

export interface ButtonProps extends DetailedHTMLProps<ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement> {}
export function Button(props: ButtonProps) {
    return <button {...props} className={`${style.buttonFragment} ${props.className}`} />;
}
