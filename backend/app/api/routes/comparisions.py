import uuid
from typing import Any, List

from sqlalchemy.orm import selectinload
from fastapi import APIRouter, HTTPException
from sqlmodel import func, select, Session, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Project, ProjectPublic, ProjectsPublic, ProjectIdsRequest

from app.core.config import settings
from app.core.openai_client import OpenAIClient

router = APIRouter(prefix="/comparisions", tags=["comparisions"])


@router.post("/", response_model=ProjectsPublic)
def read_projects_by_ids(
    session: SessionDep, request: ProjectIdsRequest
) -> Any:
    """
    Retrieve projects by a list of IDs.
    - **ids**: List of project IDs to retrieve.
    """
    ids = list(set(request.ids))
    # Check if the number of IDs exceeds 5
    if len(ids) > 5:
        raise HTTPException(
            status_code=400, 
            detail="Invalid input: Too many IDs provided. Maximum allowed is 5."
        )

    count_statement = select(func.count()).select_from(Project).where(Project.id.in_(ids))
    count = session.exec(count_statement).one()

    statement = (
        select(Project)
        .where(Project.id.in_(ids))
        .options(
            selectinload(Project.developer),
            selectinload(Project.swots),
            selectinload(Project.amenities),
            selectinload(Project.images),
        )
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

    return ProjectsPublic(data=projects_public, count=count)