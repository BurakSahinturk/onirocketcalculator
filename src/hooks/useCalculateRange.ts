import type { RocketRecipe } from "@/assets/types";
import apiClient from "@/services/api-client";
import { isAxiosError } from "axios";
import { useEffect, useState } from "react";

const useCalculateRange = (recipe: RocketRecipe) => {
  const [debouncedRecipe, setDebouncedRecipe] = useState(recipe);
  const [calculatedRange, setCalculatedRange] = useState<number | null>(null);
  const [rangeError, setRangeError] = useState<string | null>(null);

  useEffect(() => {
    if (recipe.engine_system.engine === null) return;
    const timeout = setTimeout(() => setDebouncedRecipe(recipe), 250);
    return () => clearTimeout(timeout);
  }, [recipe]);
  useEffect(() => {
    apiClient
      .post<number>("/range", debouncedRecipe)
      .then((res: { data: number }) => setCalculatedRange(res.data))
      .catch((err: unknown) => {
        if (isAxiosError(err))
          setRangeError(`Failed to calculate range - ${err.message}`);
      });
  }, [debouncedRecipe]);
  return { calculatedRange, rangeError };
};

export default useCalculateRange;
