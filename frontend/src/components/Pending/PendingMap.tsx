import { Box, Skeleton } from "@chakra-ui/react";

const PendingMap = () => (
  <Box
    height="300px"
    width="100%"
    border="1px solid #ccc"
    borderRadius="8px"
    overflow="hidden"
  >
    <Skeleton height="100%" width="100%" />
  </Box>
);

export default PendingMap;