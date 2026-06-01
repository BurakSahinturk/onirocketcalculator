import { Button, HStack, Menu, Portal, Spacer, Text } from "@chakra-ui/react";
import { ColorModeButton, useColorMode } from "@/components/ui/color-mode";
import { languages, type languageType } from "@/assets/types";

// ─── Types & Interfaces ────────────────────────────────────────────────────────
interface NavbarProps {
  lisan: languageType;
  setLisan: (lisan: languageType) => void;
}

const langFlag = {
  En: "🇬🇧",
  Tr: "🇹🇷",
};

const headerText = {
  En: "Tuygun's ONI Rocket 🚀 Calculator",
  Tr: "ONI Roket Hesaplama by Tuygun 🚀 Roket Hesaplama San. Tic. Turizm Ltd. Şti.",
};

const Navbar = ({ lisan, setLisan }: NavbarProps) => {
  const { toggleColorMode } = useColorMode();
  return (
    <HStack py="10px" px="30px">
      <Text>{headerText[lisan]}</Text>
      <Spacer />
      <ColorModeButton onClick={toggleColorMode} />
      <Menu.Root onSelect={(e) => setLisan(e.value as languageType)}>
        <Menu.Trigger asChild>
          <Button paddingRight={"30px"}>{lisan + " " + langFlag[lisan]}</Button>
        </Menu.Trigger>
        <Portal>
          <Menu.Positioner>
            <Menu.Content>
              {languages.map((lang) => (
                <Menu.Item value={lang} key={lang}>
                  {lang + " " + langFlag[lang]}
                </Menu.Item>
              ))}
            </Menu.Content>
          </Menu.Positioner>
        </Portal>
      </Menu.Root>
    </HStack>
  );
};

export default Navbar;
