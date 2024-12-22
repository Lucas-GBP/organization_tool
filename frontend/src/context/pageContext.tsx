import { createContext, useState, useEffect, PropsWithChildren, useCallback } from "react";
import { UUID } from "crypto";
import { Login } from "@/api/helpers/login";
import type { UserRecord } from "@/api/types/login";
import { Repository } from "@/api";
import type { CategotyCompletedRecord } from "@/api/types/category";
import { organizeCategories } from "@/utils/organizeCategories";

export interface PageContextType {
    user_uuid: UUID;
    repository: Repository;
    categories?: CategotyCompletedRecord[];
    get_categories: () => Promise<void>;
}

export const PageContext = createContext<PageContextType | null>(null);

export const PageProvider = ({ children }: PropsWithChildren) => {
    const [value, setValue] = useState<PageContextType | null>(null);
    const [user, setUser] = useState<UserRecord | undefined>(undefined);
    const [repository, setRepository] = useState<Repository | undefined>(undefined);
    const [categories, setCategories] = useState<CategotyCompletedRecord[] | undefined>(undefined);

    const get_repository = useCallback(async () => {
        if (!user) {
            return;
        }
        if (!repository) {
            setRepository(new Repository(user.uuid));
        }
    }, [user, repository, setRepository]);
    const get_user = useCallback(async () => {
        const rep = new Login();
        const login = await rep.get_test();
        setUser(login);
    }, [setUser]);
    const get_categories = useCallback(async () => {
        if (!repository) {
            return;
        }
        const categories_buffer = await repository.category.get_all_completed();
        // Organiza em ordem alfabetica as categorias e subcategorias
        organizeCategories(categories_buffer);
        setCategories(categories_buffer);
    }, [repository, setCategories]);

    useEffect(() => {
        if (user === undefined) {
            get_user();
            return;
        }
        if (repository === undefined) {
            get_repository();
            return;
        }
        if (categories === undefined) {
            get_categories();
        }

        setValue({
            user_uuid: user.uuid,
            repository: repository,
            categories: categories,
            get_categories: get_categories,
        });
    }, [user, get_user, repository, get_repository, categories, get_categories]);

    return <PageContext.Provider value={value}>{children}</PageContext.Provider>;
};
