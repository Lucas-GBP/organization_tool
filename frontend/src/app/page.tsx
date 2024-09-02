"use client"
import styles from "../styles/page.module.scss";
import Link from "next/link";

export default function Home() {

  return (
      <main className={styles.main}>
        <div className={styles.center}>
          <Link href="/settings">Categories</Link>
        </div>
      </main>
  );
}
