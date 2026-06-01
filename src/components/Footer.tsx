import type { languageType } from "@/assets/types";
import { ScrollArea, Text } from "@chakra-ui/react";

interface FooterProps {
  lisan: languageType;
}

const disclaimerText = {
  En: "Unofficial fan-made tool for Oxygen Not Included. Rocket images, logos, and all other game assets belong to Klei Entertainment and/or the Oxygen Not Included Wiki contributors. This project is a fan-made unofficial calculator and is not affiliated with Klei Entertainment. Browser Local Storage is used for theme and language settings. No cookies are used. 2026",
  Tr: "Gayrı-resmi fan-made 'Oxygen Not Included' Roket Menzil Hesap Aracı. Tüm roket görselleri, logolar ve tüm diğer oyun materyali Klei Entertainment ve/veya Oxygen Not Included Wiki sayfası ve/veya katılımcılarına aittir. Bu site bir fan projesidir ve Klei Entertainment ile herhangi bir ilişkisi yoktur. Renk teması ve dil seçenekleri için local storage kullanılmaktadır. Site hiçbir cookie kullanmamaktadır. 2026",
};

const Footer = ({ lisan }: FooterProps) => {
  return (
    <footer>
      <ScrollArea.Root size={"xs"} variant={"hover"}>
        <ScrollArea.Viewport>
          <ScrollArea.Content>
            <Text fontSize={"10px"}>{disclaimerText[lisan]}</Text>
          </ScrollArea.Content>
        </ScrollArea.Viewport>
      </ScrollArea.Root>
    </footer>
  );
};

export default Footer;
