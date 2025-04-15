import {
    Container,
    EmptyState,
    Flex,
    Heading,
    Table,
    VStack,
    Text,
  } from "@chakra-ui/react";
  import { useQuery } from "@tanstack/react-query";
  import { createFileRoute, useNavigate } from "@tanstack/react-router";
  import { FiSearch } from "react-icons/fi";
  import { z } from "zod";
  
  import { ProjectsService } from "@/client";
  import PendingItems from "@/components/Pending/PendingItems";
  import {
    PaginationItems,
    PaginationNextTrigger,
    PaginationPrevTrigger,
    PaginationRoot,
  } from "@/components/ui/pagination.tsx";
  
  import { useEffect } from "react";
  import type { ProjectPublic } from "@/client/types.gen";
  
  import L from "leaflet";
  import "leaflet/dist/leaflet.css";
  
  const projectsSearchSchema = z.object({
    page: z.number().default(1),
  });
  
  const PER_PAGE = 5;
  
  function getProjectssQueryOptions({ page }: { page: number }) {
    return {
      queryFn: () =>
        ProjectsService.readProjects({
          skip: (page - 1) * PER_PAGE,
          limit: PER_PAGE,
        }),
      queryKey: ["items", { page }],
    };
  }
  export const Route = createFileRoute("/projects")({
    component: Projects,
    validateSearch: (search) => projectsSearchSchema.parse(search),
  });
  
  function Map({ projects }: { projects: ProjectPublic[] }) {
    useEffect(() => {
      const map = L.map("map").setView([18.598778, 73.7271182], 13);
  
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(map);
  
      projects.forEach((project) => {
        if (project.latitude && project.longitude) {
          L.marker([project.latitude, project.longitude]).addTo(map).bindPopup(`
                          <div>
                              <b style="font-size: 16px;">${project.name}</b><br/>
                              <span style="font-size: 12px; color: gray;">${project.developer_name}</span>
                          </div>
                          `);
        }
      });
  
      // Ensure the map resizes properly
      setTimeout(() => {
        map.invalidateSize();
      }, 0);
  
      return () => {
        map.remove(); // Clean up the map on component unmount
      };
    }, [projects]);
  
    return (
      <Container
        id="map"
        style={{
          height: "400px", // Set a fixed height
          width: "100%", // Ensure it takes full width
          border: "1px solid #ccc", // Optional: Add a border for better visibility
          borderRadius: "8px", // Optional: Add rounded corners
          overflow: "hidden", // Prevent overflow issues
        }}
      />
    );
  }
  
  function ProjectsTable() {
    const navigate = useNavigate({ from: Route.fullPath });
    const { page } = Route.useSearch();
  
    const { data, isLoading, isPlaceholderData } = useQuery({
      ...getProjectssQueryOptions({ page }),
      placeholderData: (prevData) => prevData,
    });
  
    const setPage = (page: number) =>
      navigate({
        search: (prev: { [key: string]: string }) => ({ ...prev, page }),
      });
  
    const items = data?.data.slice(0, PER_PAGE) ?? [];
    const count = data?.count ?? 0;
  
    if (isLoading) {
      return <PendingItems />;
    }
    if (items.length === 0) {
      return (
        <EmptyState.Root>
          <EmptyState.Content>
            <EmptyState.Indicator>
              <FiSearch />
            </EmptyState.Indicator>
            <VStack textAlign="center">
              <EmptyState.Title>You don't have any items yet</EmptyState.Title>
              <EmptyState.Description>
                Add a new item to get started
              </EmptyState.Description>
            </VStack>
          </EmptyState.Content>
        </EmptyState.Root>
      );
    }
  
    return (
      <>
        <VStack align="center" pt={4}>
          <Map projects={items} />
        </VStack>
        <Flex overflowX="auto">
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
              {items?.map((item) => (
                <Table.Row key={item.id} opacity={isPlaceholderData ? 0.5 : 1}>
                  <Table.Cell truncate maxW="sm">
                    {item.developer_name}
                  </Table.Cell>
                  <Table.Cell truncate maxW="sm">
                    {item.name}
                  </Table.Cell>
                  <Table.Cell truncate maxW="sm">
                    {item.project_type}
                  </Table.Cell>
                  <Table.Cell truncate maxW="sm">
                    {item.location}
                  </Table.Cell>
                  <Table.Cell
                    color={!item.pricing_range ? "gray" : "inherit"}
                    truncate
                    maxW="30%"
                  >
                    {item.pricing_range || "N/A"}
                  </Table.Cell>
                  <Table.Cell
                    color={!item.area ? "gray" : "inherit"}
                    truncate
                    maxW="30%"
                  >
                    {item.area || "N/A"}
                  </Table.Cell>
                  <Table.Cell
                    color={!item.possession_date ? "gray" : "inherit"}
                    truncate
                    maxW="30%"
                  >
                    {item.possession_date || "N/A"}
                  </Table.Cell>
                  <Table.Cell
                    color={!item.key_amenities ? "gray" : "inherit"}
                    truncate
                    maxW="30%"
                  >
                    {item.key_amenities || "N/A"}
                  </Table.Cell>
                  <Table.Cell
                    color={!item.website ? "gray" : "inherit"}
                    truncate
                    maxW="30%"
                  >
                    {item.website || "N/A"}
                  </Table.Cell>
                  <Table.Cell
                    color={!item.reraId ? "gray" : "inherit"}
                    truncate
                    maxW="30%"
                  >
                    {item.reraId || "N/A"}
                  </Table.Cell>
                </Table.Row>
              ))}
            </Table.Body>
          </Table.Root>
        </Flex>
        <Flex direction="column">
          {items?.map((item) => (
            <Flex
              direction={{ base: "column-reverse", md: "row" }} // Stack on small screens, side-by-side on larger screens
              justifyContent="space-between"
              alignItems="flex-start"
              mt={4}
              key={item.id}
            >
              <Table.Root size={{ base: "sm", md: "md" }}>
                <Text textStyle="md" fontWeight="bold">
                  {item.name}
                </Text>
                <Table.Body>
                  {item.swots?.map((swot) => (
                    <Table.Row
                      key={swot.id}
                      opacity={isPlaceholderData ? 0.5 : 1}
                    >
                      <Table.Cell maxW="sm">
                        <Text fontWeight="bold">{swot.category}</Text>
                        <br />
                        {swot.description}
                      </Table.Cell>
                    </Table.Row>
                  ))}
                </Table.Body>
              </Table.Root>
              <Flex
                alignItems="center"
                justifyContent="center"
                ml={{ base: 0, md: 4 }} // Add margin on larger screens
                mb={{ base: 4, md: 0 }} // Add margin on smaller screens
              >
                <img
                  src={item.image_url ?? ""}
                  alt="Description of the image"
                  style={{
                    maxWidth: "100%",
                    height: "auto",
                    borderRadius: "8px",
                    border: "1px solid #ccc",
                    objectFit: "contain",
                  }}
                />
              </Flex>
            </Flex>
          ))}
        </Flex>
        <Flex justifyContent="flex-end" mt={4}>
          <PaginationRoot
            count={count}
            pageSize={PER_PAGE}
            onPageChange={({ page }) => setPage(page)}
          >
            <Flex>
              <PaginationPrevTrigger />
              <PaginationItems />
              <PaginationNextTrigger />
            </Flex>
          </PaginationRoot>
        </Flex>
      </>
    );
  }
  
  function Projects() {
    return (
      <Container maxW="full">
        <Heading size="lg" pt={12}>
          Projects
        </Heading>
        <VStack align="stretch" pt={4}>
          <ProjectsTable />
        </VStack>
      </Container>
    );
  }
  