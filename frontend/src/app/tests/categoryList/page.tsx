"use client";
import { useContext, useState } from "react";
import { PageContext } from "@/context/pageContext";
import { CategorySelector } from "@/components/categorySelector";
import type { SelectedCategoryObject } from "@/components/categorySelector";

export default function Page() {
    const context = useContext(PageContext);
    const [selected, setSelected] = useState<SelectedCategoryObject | undefined>(undefined);

    return (
        <main>
            <div>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam efficitur congue mi a porta. Donec
                egestas diam eu porta aliquam. Pellentesque imperdiet justo pretium condimentum porttitor. Nam
                vestibulum interdum commodo. Sed in tortor pellentesque, placerat nibh ac, efficitur nulla. Sed in diam
                ut eros varius interdum. Donec malesuada elit id ipsum egestas lacinia. Morbi mattis convallis sapien,
                at elementum metus. Sed in augue quis enim dictum pharetra. Pellentesque lacus nisl, consectetur id
                elementum id, tristique ut dolor.
            </div>
            <button>AAAAA</button>
            {context?.categories ? (
                <CategorySelector
                    categories={context.categories}
                    selected={selected}
                    setItem={(item) => {
                        console.log(item);
                        setSelected(item);
                    }}
                />
            ) : null}
            <button>BBBBB</button>
            <div>
                Curabitur eu felis in purus laoreet consectetur. Ut malesuada rhoncus quam, eu fringilla odio tincidunt
                vel. Quisque commodo eget nibh feugiat facilisis. Vestibulum ante ipsum primis in faucibus orci luctus
                et ultrices posuere cubilia curae; Mauris scelerisque justo lectus, sed ullamcorper nibh convallis quis.
                Sed vulputate auctor lectus, eleifend vulputate tortor sodales non. Nam at purus euismod, blandit nisi
                et, rhoncus ipsum. Phasellus eu bibendum mi, non semper est. Cras consectetur libero ut rhoncus sodales.
                Sed quis luctus mauris. Etiam ornare, mauris nec laoreet mollis, metus est porttitor lacus, et auctor
                libero mi nec ex. Nulla lacinia leo in vulputate condimentum. Suspendisse dignissim quam et magna
                eleifend lobortis. Nam sed nibh facilisis, eleifend metus eu, blandit magna. Morbi eu mollis erat, sed
                porta nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae;
            </div>
            <div>
                Praesent nec quam turpis. Nullam maximus dictum sapien. Vivamus placerat id nunc sit amet porta.
                Praesent dui arcu, tincidunt sed auctor et, fringilla at ipsum. Mauris tortor neque, aliquam quis
                aliquet quis, sodales at leo. Donec placerat convallis tristique. Donec vehicula magna et tellus
                consequat consectetur. Pellentesque ac viverra justo. Sed semper leo vel lacinia viverra. Praesent
                aliquet velit odio, sit amet consequat tortor ultrices nec.
            </div>
            <div>
                Aliquam ut nisl convallis, fringilla mi vitae, lobortis turpis. Maecenas pulvinar malesuada aliquam.
                Vestibulum urna nibh, finibus sit amet bibendum vel, pulvinar id ligula. In euismod dapibus tortor eget
                suscipit. In non arcu scelerisque, malesuada magna quis, euismod mauris. Curabitur faucibus metus sed
                ante cursus, a maximus libero malesuada. Morbi egestas pharetra nisl eu porta. Nullam bibendum purus sed
                leo pharetra vulputate. Cras a lobortis leo. Mauris ultrices est vitae lectus rhoncus, at facilisis
                felis lobortis. In hac habitasse platea dictumst. Vestibulum condimentum elit sit amet arcu lobortis
                dignissim. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque gravida lorem nec lectus
                pharetra hendrerit.
            </div>
            <div>
                Phasellus ligula elit, vestibulum in quam mattis, sodales volutpat ante. Pellentesque elit erat,
                tincidunt vel metus ac, malesuada ultricies dui. Nullam quam nulla, fermentum a risus nec, convallis
                sagittis augue. Cras varius viverra nibh, et molestie ante imperdiet at. Ut euismod, tellus ut ornare
                lobortis, sapien velit consectetur ante, a congue ipsum ante ut odio. Morbi id pellentesque nibh, quis
                blandit nunc. Etiam non nibh magna. In lobortis tellus sed viverra egestas. Sed consequat leo eget mi
                consectetur, a convallis turpis aliquam. In hac habitasse platea dictumst. Suspendisse pretium nulla
                nisi, id suscipit nibh lacinia sit amet. Curabitur semper consequat est eu consectetur. Phasellus eu
                ante efficitur, aliquet odio ullamcorper, sodales massa.
            </div>
        </main>
    );
}
