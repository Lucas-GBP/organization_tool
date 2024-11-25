import { createContext, useState, useEffect, PropsWithChildren, useCallback } from "react";
import { UUID } from "crypto";
import { Login } from "@/api/helpers/login";
import type { UserRecord } from "@/api/types/login";
import { Repository } from "@/api";

export interface PageContextType {
    user_uuid: UUID;
    repository:Repository;
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
            return;
        }

        setValue({
            user_uuid: user.uuid,
            repository: new Repository(user.uuid)
        });
    }, [user]);
    useEffect(() => {

    })

    return <PageContext.Provider value={value}>{children}</PageContext.Provider>;
};
