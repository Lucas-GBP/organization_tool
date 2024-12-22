import style from "@/styles/components/fragments/input.module.scss";
import { DetailedHTMLProps, InputHTMLAttributes } from "react";
//import AntInput from "antd/es/input/Input";
//import { InputProps as AntInputProps } from "antd/es/input/Input";

/*
export interface InputProps extends AntInputProps {
}*/
export interface InputProps extends DetailedHTMLProps<InputHTMLAttributes<HTMLInputElement>, HTMLInputElement> {}
export function Input(props: InputProps) {
    return <input {...props} className={`${style.inputFragment} ${props.className}`} />;
}
