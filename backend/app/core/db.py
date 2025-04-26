import json
import os
import gdown
from typing import Optional
from datetime import datetime, date
from sqlmodel import Session, create_engine, select
from app.models import User, UserCreate, Developer, Project, SWOT, Amenity, ProjectImage
from app import crud
from app.core.config import settings
import shutil

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

def extract_date(possession_date_str: str) -> Optional[date]:
    for date_format in ["%b %Y", "%B %Y"]:  # Try abbreviated and full month names
        try:
            possession_date = datetime.strptime(possession_date_str, date_format).date()
            return possession_date
        except ValueError:
            continue  # Try the next format
    return None  # Return None if no format matches

def load_sample_data_from_file(file_path: str, session: Session) -> None:
    """Load sample data from a local JSON file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r") as file:
        try:
            data_list = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {e}")

    for data in data_list:
        # Insert Users
        user = session.exec(
            select(User).where(User.email == settings.FIRST_SUPERUSER)
        ).first()
        if not user:
            user_in = UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            )
            user = crud.create_user(session=session, user_create=user_in)
        
        # Insert Developers
        for developer_data in data.get("developers", []):
            developer = session.exec(select(Developer).where(Developer.name == developer_data["name"])).first()
            if not developer:
                developer = Developer(
                    name=developer_data["name"],
                    reputation=developer_data["reputation"],
                    additional_info=developer_data["additional_info"]
                )
                session.add(developer)
                session.commit()
                session.refresh(developer)

        # Insert Projects
        for project_data in data.get("projects", []):
            developer = session.exec(select(Developer).where(Developer.name == project_data["developer_name"])).first()
            if not developer:
                continue  # Skip if developer does not exist

            project = session.exec(select(Project).where(Project.name == project_data["name"])).first()
            if not project:
                project = Project(
                    name=project_data["name"],
                    location=project_data["location"],
                    latitude=project_data["latitude"],
                    longitude=project_data["longitude"],
                    min_price=project_data["min_price"],
                    max_price=project_data["max_price"],
                    possession_date=extract_date(project_data["possession_date"]),
                    project_type=project_data["project_type"],
                    website=project_data["website"],
                    reraId=project_data["reraId"],
                    description=project_data["description"],
                    area=project_data["area"],
                    key_amenities=project_data["key_amenities"],
                    developer_id=developer.id
                )
                session.add(project)
                session.commit()
                session.refresh(project)

        # Insert SWOTs
        for swot_data in data.get("swots", []):
            project = session.exec(select(Project).where(Project.name == swot_data["project_name"])).first()
            if not project:
                continue  # Skip if project does not exist

            swot = session.exec(
                select(SWOT).where(SWOT.category == swot_data["category"]).where(SWOT.project_id == project.id)
            ).first()
            if not swot:
                swot = SWOT(
                    category=swot_data["category"],
                    description=swot_data["description"],
                    project_id=project.id
                )
                session.add(swot)
                session.commit()

        # Insert Amenities
        for amenity_data in data.get("amenities", []):
            project = session.exec(select(Project).where(Project.name == amenity_data["project_name"])).first()
            if not project:
                continue  # Skip if project does not exist

            amenity = session.exec(
                select(Amenity).where(Amenity.amenity_name == amenity_data["amenity_name"]).where(Amenity.project_id == project.id)
            ).first()
            if not amenity:
                amenity = Amenity(
                    amenity_name=amenity_data["amenity_name"],
                    description=amenity_data["description"],
                    project_id=project.id
                )
                session.add(amenity)
                session.commit()
        
        # Insert Image URLs
        for image_data in data.get("project_images", []):
            project = session.exec(select(Project).where(Project.name == image_data["project_name"])).first()
            if not project:
                continue  # Skip if project does not exist

            image = session.exec(
                select(ProjectImage).where(ProjectImage.image_url == image_data["image_url"]).where(ProjectImage.project_id == project.id)
            ).first()

            if not image:
                image = ProjectImage(
                    image_url=image_data["image_url"],
                    project_id=project.id
                )
                session.add(image)
                session.commit()

def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)
    
    # Delete the folder if it exists
    if os.path.exists(settings.TEMP_DATA_DIR):
        shutil.rmtree(settings.TEMP_DATA_DIR)

    gdown.download_folder(settings.GDRIVE_DATA_FOLDER_URL, output=settings.TEMP_DATA_DIR)
    
    # # Iterate over files in the folder and call load_sample_data_from_file
    for file_name in os.listdir(settings.TEMP_DATA_DIR):
        file_path = os.path.join(settings.TEMP_DATA_DIR, file_name)
        if os.path.isfile(file_path):  # Ensure it's a file
            load_sample_data_from_file(file_path, session)
    