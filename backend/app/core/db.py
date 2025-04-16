import json
import os
import gdown
import requests
from sqlmodel import Session, create_engine, select
from app.models import User, UserCreate, Developer, Project, SWOT, Amenity
from app import crud
from app.core.config import settings
import shutil

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

def load_sample_data_from_gdrive(gdrive_url: str, session: Session) -> None:
    """Load sample data from a Google Drive link."""
    
    output_folder = "/tmp/public"

    # Delete the folder if it exists
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    gdown.download_folder(gdrive_url, output=output_folder)
    
    # # Iterate over files in the folder and call load_sample_data_from_file
    for file_name in os.listdir(output_folder):
        file_path = os.path.join(output_folder, file_name)
        if os.path.isfile(file_path):  # Ensure it's a file
            load_sample_data_from_file(file_path, session)

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
                    pricing_range=project_data["pricing_range"],
                    possession_date=project_data["possession_date"],
                    project_type=project_data["project_type"],
                    website=project_data["website"],
                    reraId=project_data["reraId"],
                    description=project_data["description"],
                    area=project_data["area"],
                    image_url=project_data["image_url"],
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

def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)
    gdrive_url = 'https://drive.google.com/drive/folders/1ICvXyow6vmT9Jiy91vSsfBiCXq1uh5Op'
    load_sample_data_from_gdrive(gdrive_url, session)