import { createContext, useState, useEffect, PropsWithChildren } from "react";
import { UUID } from "crypto";

export interface PageContextType {
    user_uuid?: UUID;
}

export const PageContext = createContext<PageContextType | null>(null);

const standartValue: PageContextType = {
    user_uuid: "142c07aa-2759-4433-a753-65795e747af1",
};

export const PageProvider = ({ children }: PropsWithChildren) => {
    const [value, setValue] = useState<PageContextType | null>(null);

    useEffect(() => {
        // on client side mount, set starting value
        setValue(standartValue);
    }, []);

    return <PageContext.Provider value={value}>{children}</PageContext.Provider>;
};
