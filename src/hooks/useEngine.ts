import type { EngineDesc } from "@/assets/types";
import { useMemo } from "react";

const useEngine = (enginesList: EngineDesc[], engineName: string | null) => {
  const engineLookup = useMemo(
    () => Object.fromEntries(enginesList.map((item) => [item.key, item])),
    [enginesList],
  );

  const engine = engineName ? engineLookup[engineName] : null;

  return { engine };
};

export default useEngine;
