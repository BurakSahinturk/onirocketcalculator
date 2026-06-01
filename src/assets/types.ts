export interface RocketPart {
  key: string;
  display_name: string;
  mass: number;
}

export interface EngineDesc {
  key: string;
  display_name: string;
  mass: number;
  capacity: number | null;
  uses_internal_fuel: boolean;
}

export interface TankDesc {
  key: string;
  display_name: string;
  mass: number;
  resource_type: string;
  capacity: number;
}

export interface EngineRecipe {
  engine: string | null;
  thrusters: number;
  internal_fuel: number;
}

export interface TankRecipe {
  tank_count: number;
  fuel_amount: number;
}

export type TankKey = keyof RocketRecipe["fuel_system"];
export type ModuleKey = keyof RocketRecipe["modules"];

export interface RocketRecipe {
  engine_system: EngineRecipe;
  fuel_system: Record<string, TankRecipe>;
  modules: Record<string, number>;
}

export interface GameConstants {
  MAX_THRUSTERS: number;
  MAX_FUEL_TANKS: number;
  MAX_MODULE_COUNT: number;
  MAX_OXI_TANKS: number;
}

export interface GameReferenceDataResponse {
  constants: GameConstants;
  commands: RocketPart[];
  engines: EngineDesc[];
  fuel_tanks: TankDesc[];
  oxidizer_tanks: TankDesc[];
  extra_modules: RocketPart[];
  thrusters: RocketPart[];
}

export const OXIDIZER_TYPES = {
  OXYLITE: {
    En: "Solid Oxylite",
    Tr: "Katı Oksilit",
  },
  LOX: {
    En: "Liquid Oxygen",
    Tr: "Sıvı Oksijen",
  },
} as const;

export interface ConfigurationRequest {
  rocket_recipe: RocketRecipe;
  desired_range: number;
  oxidizer: typeof OXIDIZER_TYPES;
}

export const languages = ["En", "Tr"] as const;
export type languageType = (typeof languages)[number];
