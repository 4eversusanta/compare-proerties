import { Skeleton } from "@chakra-ui/react";

function PendingMap() {
  return (
    <Skeleton
      height="300px"
      width="100%"
      borderRadius="8px"
      border="1px solid #ccc"
    />
  );
}

export default PendingMap;