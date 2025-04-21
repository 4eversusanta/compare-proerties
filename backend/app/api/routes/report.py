import uuid
from typing import Any, List

from sqlalchemy.orm import selectinload
from fastapi import APIRouter, HTTPException
from sqlmodel import func, select, Session, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Project, ProjectPublic, SWOTPublic, AmenityPublic, ReportResponse, ProjectIdsRequest

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
            selectinload(Project.amenities),
        )
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
    print(prompt)
    try:
        # response = openai_client.generate_summary(prompt)
        response = "This is a mock response for the prompt: {}".format(prompt)
        # print(response)

        return ReportResponse(summary=response)
    except Exception as e:
        return ReportResponse(summary=f"Failed to generate summary: {str(e)}")
    
