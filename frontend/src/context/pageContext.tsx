import { createContext, useState, useEffect, PropsWithChildren, useCallback } from "react";
import { UUID } from "crypto";
import { Login } from "@/api/login";
import type { UserRecord } from "@/api/types/login";

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
        if (user == undefined){
            get_user();
        }

        setValue({
            user_uuid: user?.uuid
        });
    }, [user]);

    return <PageContext.Provider value={value}>{children}</PageContext.Provider>;
};
