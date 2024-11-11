import { createContext, useState, useEffect, PropsWithChildren, useCallback } from "react";
import { UUID } from "crypto";
import { Login } from "@/api/login";
import type { UserRecord } from "@/api/types/login";
import { userAgent } from "next/server";

export interface PageContextType {
    user_uuid?: UUID;
}

export const PageContext = createContext<PageContextType | null>(null);

export const PageProvider = ({ children }: PropsWithChildren) => {
    const [value, setValue] = useState<PageContextType | null>(null);
    const [user, setUser] = useState<UserRecord|undefined>(undefined);

    const get_user = useCallback(async () => {
        const rep = new Login()
        const login = await rep.get_test()
        setUser(login);
    }, []);

    useEffect(() =>{
        // on client side mount, set starting value
        if (user == undefined){
            get_user();
        }

        setValue({
            user_uuid: user?.uuid
        });
    }, [user]);
    useEffect(() => {
        console.log({value})
    }, [value])

    return <PageContext.Provider value={value}>{children}</PageContext.Provider>;
};
