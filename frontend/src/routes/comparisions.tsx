import React from "react";
import {
  Container,
  EmptyState,
  Flex,
  Heading,
  Table,
  VStack,
  HStack,
  Text,
} from "@chakra-ui/react";
import { useQuery } from "@tanstack/react-query";
import { createFileRoute, Link as RouterLink } from "@tanstack/react-router";
import { FiSearch } from "react-icons/fi";
import { z } from "zod";

import { ComparisionsService, ReportService } from "@/client";
import PendingComparisions from "@/components/Pending/PendingComparisions";
import PendingMap from "@/components/Pending/PendingMap";

import PendingRecomendations from "@/components/Pending/PendingRecomendations";

import { useEffect } from "react";
import type { ProjectPublic } from "@/client/types.gen";

import L from "leaflet";
import "leaflet/dist/leaflet.css";

import { Icon } from "@chakra-ui/react"
import { MdBackspace } from "react-icons/md";


const projectsSearchSchema = z.object({
  ids: z
    .string()
    .refine(
      (ids) => {
        if (!ids) return false;
        const idArray = ids.split(",");
        return idArray.every((id) => z.string().uuid().safeParse(id).success);
      },
      { message: "All ids must be valid UUIDs" }
    ),
});

function getProjectssQueryOptions({ ids }: { ids: string[] }) {
  return {
    queryFn: () =>
      ComparisionsService.readProjectsByIds({
        requestBody: { ids: ids || [] },
      }),
    queryKey: ["items", { ids }],
  };
}
function getProjectsReportOptions({ ids }: { ids: string[] }) {
  return {
    queryFn: () =>
      ReportService.readProjectsReportByIds({
        requestBody: { ids: ids || [] },
      }),
    queryKey: ["report", { ids }],
  };
}

export const Route = createFileRoute("/comparisions")({
  component: Comparisions,
  validateSearch: (search) => {
    const parsedSearch = projectsSearchSchema.parse(search);
    return {
      ...parsedSearch,
      ids: parsedSearch.ids ? parsedSearch.ids.split(",") : [], // Convert comma-separated string to array
    };
  },
});
function Map({ projects }: { projects: ProjectPublic[] }) {
  const isLoading = !projects || projects.length === 0; // Example condition

  useEffect(() => {
    if (!isLoading) {
      const map = L.map("map").setView([18.598778, 73.7271182], 13);

      const customIcon = L.icon({
        iconUrl: "/assets/images/marker-icon.png", // Path to your copied marker-icon.png
        shadowUrl: "/assets/images/marker-shadow.png", // Path to your copied marker-shadow.png
      });

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(map);

      projects.forEach((project) => {
        if (project.latitude && project.longitude) {
            L.marker([project.latitude, project.longitude], { icon: customIcon })
            .addTo(map)
            .bindPopup(`
                <div>
                  <b style="font-size: 16px;">${project.name}</b><br/>
                  <span style="font-size: 12px; color: gray;">${project.developer_name}</span><br/>
                  <span style="font-size: 12px; color: gray;">${project.area}</span><br/>
                  <span style="font-size: 12px; color: gray;">${project.min_price} - ${project.max_price}</span>
                </div>
              `);
        }
      });

      setTimeout(() => {
        map.invalidateSize();
      }, 0);

      return () => {
        map.remove();
      };
    }
  }, [projects, isLoading]);

  if (isLoading) {
    console.log("isLoading:", isLoading, "projects:", projects);
    return <PendingMap />;
  }

  return (
    <Container
      id="map"
      style={{
        height: "300px",
        width: "100%",
        border: "1px solid #ccc",
        borderRadius: "8px",
        overflow: "hidden",
      }}
    />
  );
}

function ReportTable() {
  const { ids } = Route.useSearch();
  console.log("ids", ids);
  const { data, isLoading } = useQuery({
    ...getProjectsReportOptions({ ids }),
    placeholderData: (prevData) => prevData,
  });

  const summery = data?.summary;

  if (isLoading) {
    return <PendingRecomendations />;
  }
  if (!data || !data.summary) {
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
    )
  }
  return (
    <>
      <Text textStyle="lg" fontWeight="bold">
        AI generated Recommendations
      </Text>
      <Text
        as="span"
        textStyle="md"
        fontWeight="normal"
        dangerouslySetInnerHTML={{ __html: summery || "" }} // Ensure summery is a string
      />
    </>
  );
}
function ProjectsTable() {
  const { ids } = Route.useSearch();

  const { data, isLoading, isPlaceholderData } = useQuery({
    ...getProjectssQueryOptions({ ids }),
    placeholderData: (prevData) => prevData,
  });


  const items = data?.data ?? [];

  if (isLoading) {
    return <PendingComparisions />;
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
      <VStack align="center" pt={2}>
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
            {items?.map((item, index) => (
              <Table.Row key={index} opacity={isPlaceholderData ? 0.5 : 1}>
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
                  color={!item.min_price ? "gray" : "inherit"}
                  truncate
                  maxW="30%"
                >
                  {item.min_price || "N/A"} - {item.max_price || "N/A"}
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
        {items?.map((item, index) => (
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
                    key={index}
                    opacity={isPlaceholderData ? 0.5 : 1}
                  >
                    <Table.Cell maxW="sm">
                      <Text fontWeight="bold">{swot.category}</Text>
                      <br />
                      {swot.description.split(/\r\n/).map((line, index) => (
                        <React.Fragment key={index}>
                          {line}
                          <br />
                        </React.Fragment>
                      ))}
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
                src={item.images && item.images[0]?.image_url ? item.images[0].image_url : ""}
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
    </>
  );
}

function Comparisions() {
  return (
    <Container maxW="full">
      <VStack pt={12}>
        <HStack w="100%">
          <RouterLink to="/projects" className="main-link">
            <Icon size="lg">
              <MdBackspace />
            </Icon>
          </RouterLink>
          <Flex flex="1">
            <Heading size="lg">Comparisions</Heading>
          </Flex>
        </HStack>
      </VStack>
      <VStack align="stretch" pt={4}>
        <ProjectsTable />
      </VStack>
      <VStack align="stretch" pt={4}>
        <ReportTable />
      </VStack>
    </Container>
  );
}
