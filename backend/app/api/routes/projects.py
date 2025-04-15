import uuid
from typing import Any

from sqlalchemy.orm import selectinload
from fastapi import APIRouter
from sqlmodel import func, select, Session, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Project, ProjectPublic, ProjectsPublic, SWOTPublic, AmenityPublic, Message

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", response_model=ProjectsPublic)
def read_projects(
    session: SessionDep, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve projects with pagination.
    - **skip**: Number of records to skip (used for pagination offset).
    - **limit**: Maximum number of records to return.
    """

    # return ItemsPublic(data=items, count=count)

    # Query to count total projects
    count_statement = select(func.count()).select_from(Project)
    count = session.exec(count_statement).one()

    # Query to fetch paginated projects
    # statement = select(Project).offset(skip).limit(limit)
    # projects = session.exec(statement).all()

    # return ProjectsPublic(data=projects, count=count)

    # Query to fetch paginated projects with developer, SWOT, and amenities
    statement = (
        select(Project)
        .options(
            selectinload(Project.developer),
            selectinload(Project.swots),
            selectinload(Project.amenities),
        )
        .offset(skip)
        .limit(limit)
    )
    projects = session.exec(statement).all()

    # Transform projects to include developer name
    projects_public = [
        ProjectPublic(
            id=project.id,
            name=project.name,
            location=project.location,
            latitude=project.latitude,
            longitude=project.longitude,
            pricing_range=project.pricing_range,
            possession_date=project.possession_date,
            project_type=project.project_type,
            website=project.website,
            reraId=project.reraId,
            description=project.description,
            area=project.area,
            image_url=project.image_url,
            key_amenities=project.key_amenities,
            developer_name=project.developer.name if project.developer else None,
            swots=[
                SWOTPublic(category=swot.category, description=swot.description)
                for swot in project.swots
            ],
            amenities=[
                AmenityPublic(
                    amenity_name=amenity.amenity_name,
                    description=amenity.description,
                )
                for amenity in project.amenities
            ],
        )
        for project in projects
    ]

    return ProjectsPublic(data=projects_public, count=count)
