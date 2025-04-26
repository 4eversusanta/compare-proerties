import uuid
from typing import Any

from sqlalchemy.orm import selectinload
from fastapi import APIRouter
from sqlmodel import func, select, Session, select


from app.api.deps import CurrentUser, SessionDep
from app.models import Project, ProjectPublic, ProjectsPublic

from app.core.config import settings
from app.core.openai_client import OpenAIClient

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

    # Query to fetch paginated projects with developer, SWOT, amenities and images
    statement = (
        select(Project)
        .options(
            selectinload(Project.developer),
            selectinload(Project.swots),
            selectinload(Project.amenities),
            selectinload(Project.images),
        )
        .offset(skip)
        .limit(limit)
    )
    projects = session.exec(statement).all()

    # Transform projects to include developer name
    projects_public = [
        ProjectPublic(
            id=project.id,
            developer_id=project.developer_id,
            developer_name=project.developer.name if project.developer else None,
            min_price=project.min_price,
            max_price=project.max_price,
            name=project.name,
            location=project.location,
            latitude=project.latitude,
            longitude=project.longitude,
            possession_date=project.possession_date,
            project_type=project.project_type,
            website=project.website,
            reraId=project.reraId,
            description=project.description,
            area=project.area,
            key_amenities=project.key_amenities,
            swots=project.swots,
            amenities=project.amenities,
            images=project.images,
        )
        for project in projects
    ]

    # openai_client = OpenAIClient(api_key=settings.OPENAI_API_KEY)
    # projects_public_json = [project.json() for project in projects_public]
    # prompt = "You are a real estate expert. Please generate three recommendations for a buyer comparing the following projects: " + \
    #     ", ".join(projects_public_json)
    # try:
    #     response = openai_client.generate_summary(prompt)
    #     print(response)
    # except Exception as e:
    #     return {
    #         "data": [],
    #         "count": count,
    #         "error": f"Failed to generate summary: {str(e)}"
    #     }

    return ProjectsPublic(data=projects_public, count=count)
