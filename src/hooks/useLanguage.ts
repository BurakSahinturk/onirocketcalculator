import type { languageType } from "@/assets/types";
import { useEffect, useState } from "react";

const useLanguage = () => {
  const getInitialLanguage = (): languageType => {
    const savedLang = localStorage.getItem("site-language");
    if (savedLang === "Tr" || savedLang === "En") return savedLang;
    const browserLang = navigator.languages?.[0] ?? navigator.language;
    if (browserLang?.toLowerCase().startsWith("tr")) return "Tr";
    else return "En";
  };

  const [lisan, setLisan] = useState<languageType>(getInitialLanguage);

  useEffect(() => {
    localStorage.setItem("site-language", lisan);
    document.documentElement.lang = lisan;
  }, [lisan]);

  return { lisan, setLisan };
};

export default useLanguage;
