import { Image } from "@chakra-ui/react";

interface RocketPartImageProps {
  fileName: string;
}

const RocketPartImage = ({ fileName }: RocketPartImageProps) => {
  return (
    <Image
      src={`/RocketParts/${fileName}.png`}
      alt={fileName}
      boxSize="50px"
      objectFit={"contain"}
      py={0}
      my={"-3px"}
    />
  );
};

export default RocketPartImage;
