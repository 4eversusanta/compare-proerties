import { Table } from "@chakra-ui/react"
import { SkeletonText } from "../ui/skeleton"

const PendingProjects = () => (
  <Table.Root size={{ base: "sm", md: "md" }}>
    <Table.Header>
      <Table.Row>
        <Table.ColumnHeader w="sm">Developer</Table.ColumnHeader>
        <Table.ColumnHeader w="sm">Name</Table.ColumnHeader>
        <Table.ColumnHeader w="sm">Type</Table.ColumnHeader>
        <Table.ColumnHeader w="sm">Location</Table.ColumnHeader>
        <Table.ColumnHeader w="sm">Price</Table.ColumnHeader>
        <Table.ColumnHeader w="sm">Size</Table.ColumnHeader>
        <Table.ColumnHeader w="sm">Possesion</Table.ColumnHeader>
        <Table.ColumnHeader w="sm">Amenities</Table.ColumnHeader>
        <Table.ColumnHeader w="sm">Website</Table.ColumnHeader>
        <Table.ColumnHeader w="sm">Rera Id</Table.ColumnHeader>
      </Table.Row>
    </Table.Header>
    <Table.Body>
      {[...Array(3)].map((_, index) => (
        <Table.Row key={index}>
          <Table.Cell>
            <SkeletonText noOfLines={1} />
          </Table.Cell>
          <Table.Cell>
            <SkeletonText noOfLines={1} />
          </Table.Cell>
          <Table.Cell>
            <SkeletonText noOfLines={1} />
          </Table.Cell>
          <Table.Cell>
            <SkeletonText noOfLines={1} />
          </Table.Cell>
          <Table.Cell>
            <SkeletonText noOfLines={1} />
          </Table.Cell>
          <Table.Cell>
            <SkeletonText noOfLines={1} />
          </Table.Cell>
          <Table.Cell>
            <SkeletonText noOfLines={1} />
          </Table.Cell>
          <Table.Cell>
            <SkeletonText noOfLines={1} />
          </Table.Cell>
          <Table.Cell>
            <SkeletonText noOfLines={1} />
          </Table.Cell>
          <Table.Cell>
            <SkeletonText noOfLines={1} />
          </Table.Cell>
        </Table.Row>
      ))}
    </Table.Body>
  </Table.Root>
)
export default PendingProjects
