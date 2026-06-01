import type {
  EngineDesc,
  GameConstants,
  GameReferenceDataResponse,
  RocketPart,
  TankDesc,
} from "@/assets/types";
import apiClient from "@/services/api-client";
import { useEffect, useState } from "react";

const useRocketModules = () => {
  const [loadingParts, setLoadingParts] = useState(true);
  const [commandsList, setCommandsList] = useState<RocketPart[]>([]);
  const [enginesList, setEnginesList] = useState<EngineDesc[]>([]);
  const [fuelTanksList, setFuelTanksList] = useState<TankDesc[]>([]);
  const [oxidizerTanksList, setOxidizerTanksList] = useState<TankDesc[]>([]);
  const [extraModulesList, setExtraModulesList] = useState<RocketPart[]>([]);
  const [thrustersList, setThrustersList] = useState<RocketPart[]>([]);
  const [loadingError, setLoadingError] = useState<string | null>(null);
  const [gameConstants, setGameConstants] = useState<GameConstants>({
    MAX_THRUSTERS: 0,
    MAX_FUEL_TANKS: 0,
    MAX_MODULE_COUNT: 0,
    MAX_OXI_TANKS: 0,
  });

  useEffect(() => {
    apiClient
      .get<GameReferenceDataResponse>("/reference-data")
      .then((res: { data: GameReferenceDataResponse }) => {
        setGameConstants(res.data.constants);
        setCommandsList(res.data.commands);
        setEnginesList(res.data.engines);
        setFuelTanksList(res.data.fuel_tanks);
        setOxidizerTanksList(res.data.oxidizer_tanks);
        setExtraModulesList(res.data.extra_modules);
        setThrustersList(res.data.thrusters);
      })
      .catch((err) =>
        setLoadingError(`Failed to load rocket parts - ${err.message}`),
      )
      .finally(() => {
        setLoadingParts(false);
      });
  }, []);

  return {
    loadingParts,
    commandsList,
    enginesList,
    fuelTanksList,
    oxidizerTanksList,
    extraModulesList,
    thrustersList,
    gameConstants,
    loadingError,
  };
};

export default useRocketModules;
