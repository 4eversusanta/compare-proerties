import { Flex, Image, useBreakpointValue, Container } from "@chakra-ui/react"
import { Link } from "@tanstack/react-router"

import Logo from "/assets/images/fastapi-logo.png"
import UserMenu from "./UserMenu"

function Navbar() {

  return (
    <Container maxW="full">
      <Flex
        justify="space-between"
        alignItems="center"
        pt={2}
      >
        <Link to="/">
          <Image height="50px" src={Logo} alt="Logo" maxW="3xs" />
        </Link>
        <Flex alignItems="center">
          <UserMenu />
        </Flex>
      </Flex>
    </Container>
  )
}

export default Navbar
