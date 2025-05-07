import uuid
from typing import Any, List

from sqlalchemy.orm import selectinload
from fastapi import APIRouter, HTTPException
from sqlmodel import func, select, Session, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Project, ProjectPublic, ReportResponse, ProjectIdsRequest

from app.core.config import settings
from app.core.openai_client import OpenAIClient
import os
import gdown
import requests
import shutil

router = APIRouter(prefix="/report", tags=["report"])

def load_prompt_from_gdrive(gdrive_url: str, prompt_file: str) -> None:
    """Load sample data from a Google Drive link."""
    
    output_folder = "/tmp/prompts"

    # Delete the folder if it exists
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    gdown.download_folder(gdrive_url, output=output_folder)
    
    # # Iterate over files in the folder and call load_sample_data_from_file
    for file_name in os.listdir(output_folder):
        file_path = os.path.join(output_folder, file_name)
        if os.path.isfile(file_path) and file_name == prompt_file: 
            with open(file_path, "r") as file:
                prompt = file.read()
                return prompt
    return None

@router.post("/", response_model=ReportResponse)
def read_projects_report_by_ids(
    session: SessionDep,request: ProjectIdsRequest
) -> Any:
    """
    Retrieve report by a list of IDs.
    - **ids**: List of project IDs to retrieve.
    """
    ids = list(set(request.ids))
     # Check if the number of IDs exceeds 5
    if len(ids) > 5:
        raise HTTPException(
            status_code=400, 
            detail="Invalid input: Too many IDs provided. Maximum allowed is 5."
        )
    
    # Query to fetch paginated projects with developer, SWOT, and amenities
    statement = (
        select(Project)
        .where(Project.id.in_(ids))
        .options(
            selectinload(Project.developer),
            selectinload(Project.swots),
            selectinload(Project.amenities)
        )
    )
    projects = session.exec(statement).all()

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
            images=[],
        )
        for project in projects
    ]

    openai_client = OpenAIClient(api_key=settings.OPENAI_API_KEY)
    projects_public_json = [project.json() for project in projects_public]
    
    if len(projects_public_json) > 10:  # Example limit
        projects_public_json = projects_public_json[:10]
    if not projects_public_json:
        return ReportResponse(summary="No projects found for the provided IDs.")
    
    # Load prompt from Google Drive
    gdrive_url = "https://drive.google.com/drive/folders/1qZUpu6d0RWPGqJ5CF0VkwhFZL0kMMlNZ"
    prompt_file = "prompt.txt"
    system_prompt = load_prompt_from_gdrive(gdrive_url, prompt_file)
    
    if system_prompt is None:
        return ReportResponse(summary=f"Failed to generate summary: Prompt file not found.")
    
    # prompt = """
    # You are a real estate expert. Please generate three recommendations 
    # for a buyer comparing the following projects: "{}"
    # """.format(", ".join(projects_public_json))
    prompt = system_prompt.format(", ".join(projects_public_json))
    try:
        response = openai_client.generate_summary(prompt)

        # print(completion.choices[0].message)
        response = response
        # print(response)

        return ReportResponse(summary=response)
    except Exception as e:
        return ReportResponse(summary=f"Failed to generate summary: {str(e)}")
    
