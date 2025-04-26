import {
  Container,
  EmptyState,
  Flex,
  Heading,
  Button,
  VStack,
  Text,
} from "@chakra-ui/react";
import { useQuery } from "@tanstack/react-query";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { FiSearch } from "react-icons/fi";
import { z } from "zod";

import { ProjectsService, ProjectPublic } from "@/client";
import PendingProjects from "@/components/Pending/PendingProjects";
import PendingMap from "@/components/Pending/PendingMap";

import {
  PaginationItems,
  PaginationNextTrigger,
  PaginationPrevTrigger,
  PaginationRoot,
} from "@/components/ui/pagination.tsx";

import { useEffect } from "react";
// import type { ProjectPublic } from "@/client/types.gen";

import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { useState } from "react"; 

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
  const isLoading = !projects || projects.length === 0; // Example condition

  useEffect(() => {
    if (!isLoading) {
      const map = L.map("map").setView([18.598778, 73.7271182], 13);

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(map);

      projects.forEach((project) => {
        if (project.latitude && project.longitude) {
          L.marker([project.latitude, project.longitude])
            .addTo(map)
            .bindPopup(`
              <div>
                <b style="font-size: 16px;">${project.name}</b><br/>
                <span style="font-size: 12px; color: gray;">${project.developer_name}</span><br/>
                <span style="font-size: 12px; color: gray;">${project.area}</span><br/>
                <span style="font-size: 12px; color: gray;">${project.min_price} - ${project.max_price} </span>
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

function ProjectsTable() {
  const navigate = useNavigate({ from: Route.fullPath });
  const { page } = Route.useSearch();

  const { data, isLoading } = useQuery({
    ...getProjectssQueryOptions({ page }),
    placeholderData: (prevData) => prevData,
  });

  const setPage = (page: number) =>
    navigate({
      search: (prev: { [key: string]: string }) => ({ ...prev, page }),
    });

  const items = data?.data.slice(0, PER_PAGE) ?? [];
  const count = data?.count ?? 0;
  
  const [selectedItems, setSelectedItems] = useState<string[]>([]);
  
  const handleCheckboxChange = (id: string) => {
    setSelectedItems((prev) => {
      if (prev.includes(id)) {
        return prev.filter((itemId) => itemId !== id);
      } else if (prev.length < 5) {
        return [...prev, id];
      }
      return prev;
    });
  };

  const handleButtonClick = () => {
    console.log("Selected Items:", selectedItems);
    const selectedItemsString = selectedItems.join(",");
    navigate({
      to: `/comparisions?ids=${selectedItemsString}`,
    });
  };

  if (isLoading) {
    return <PendingProjects />;
  }
  if (items.length === 0) {
    return (
      <EmptyState.Root>
        <EmptyState.Content>
          <EmptyState.Indicator>
            <FiSearch />
          </EmptyState.Indicator>
          <VStack textAlign="center">
            <EmptyState.Title>No Projects to show</EmptyState.Title>
            <EmptyState.Description>
              Check your filters or try again later.
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
      <Flex justifyContent="end" mt={4}>
      <Button
        onClick={handleButtonClick}
        disabled={selectedItems.length < 2 || selectedItems.length > 5}
        style={{
          cursor:
            selectedItems.length >= 2 && selectedItems.length <= 5
              ? "pointer"
              : "not-allowed",
        }}
      >
        {selectedItems.length === 0
            ? "Compare"
            : selectedItems.length < 2
            ? "Add some more"
            : selectedItems.length > 5
            ? "Max 5"
            : "Compare"}
      </Button>
      </Flex>
      <Flex direction="column">
        {items?.map((item) => (
          <Flex
            direction={{ base: "column-reverse", md: "row" }} // Stack on small screens, side-by-side on larger screens
            justifyContent="space-between"
            alignItems="stretch"
            mt={4}
            key={item.id}
          >
            <Flex
              direction="row"
              justifyContent="start"
              alignItems="center"
              width="70%"
            >
              <Flex alignItems="start" mr={4}>
                <input
                  type="checkbox"
                  checked={selectedItems.includes(item.id)}
                  onChange={() => handleCheckboxChange(item.id)}
                  disabled={
                    !selectedItems.includes(item.id) && selectedItems.length >= 5
                  }
                />
              </Flex>
              <Flex direction="column" alignItems="start">
                <Text textStyle="lg" fontWeight="bold">
                  {item.name}
                </Text>
                <Text textStyle="sm" color="gray.600" fontWeight="bold">
                  {item.developer_name}
                </Text>
                <Text textStyle="sm" color="gray.600" fontWeight="medium">
                  {item.location}
                </Text>
                <Text textStyle="xs" color="gray.600" fontWeight="light">
                  {item.min_price} - {item.max_price}
                </Text>
                <Text textStyle="xs" color="gray.600" fontWeight="light">
                  {item.area}
                </Text>
                <br/>
                <Text textStyle="sm" color="gray.600" fontWeight="semibold" truncate>
                  {item.description}
                </Text>
              </Flex>
            </Flex>
            <Flex
              alignItems="end"
              justifyContent="end"
              ml={{ base: 0, md: 4 }} // Add margin on larger screens
              mb={{ base: 4, md: 0 }} // Add margin on smaller screens
              maxW="30%"
              width="30%"
              height="120px"
            >
              <img
                src={item.images && item.images[0]?.image_url ? item.images[0].image_url : ""}
                alt="Description of the image"
                style={{
                  width: "100%",
                  height: "100%",
                  borderRadius: "8px",
                  border: "1px solid #ccc",
                  objectFit: "cover",
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
