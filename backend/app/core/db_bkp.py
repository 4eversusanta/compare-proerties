from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models import User, UserCreate, Developer, Project, SWOT, Amenity

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # logger.info("Initializing ....")
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

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


    # Sample data for Developer
    developer = session.exec(
        select(Developer).where(Developer.name == "Kings Marque Group")
    ).first()
    if not developer:
        developer = Developer(
            name="Kings Marque Group",
            reputation="High",
            additional_info="A well-known developer in the industry."
        )
        session.add(developer)
        session.commit()
        session.refresh(developer)

    # Sample data-2 for Developer
    developer = session.exec(
        select(Developer).where(Developer.name == "ANP Corp")
    ).first()
    if not developer:
        developer = Developer(
            name="ANP Corp",
            reputation="High",
            additional_info="A well-known developer in the industry."
        )
        session.add(developer)
        session.commit()
        session.refresh(developer)

    # Sample data for Project
    project = session.exec(
        select(Project).where(Project.name == "Kings County")
    ).first()
    if not project:
        project = Project(
            name="Kings County",
            location="Wakad, Pune",
            latitude=18.598778,
            longitude=73.7271182,
            pricing_range="Rs 1.56cr - 1.68Cr",
            possession_date="Dec 2026",
            project_type="Apartments",
            website="https://kingscountywakad.in",
            reraId="P52100000154",
            description="""  Kings County is a luxurious residential project
            located in Wakad, Pune. The project offers a range of 2 and 3 BHK apartments with modern amenities
            """,
            area="1195 sq ft.",
            image_url="https://kingscountywakad.in/wp-content/uploads/al_opt_content/IMAGE/kingscountywakad.in//wp-content/uploads/2024/04/1.jpg.bv_resized_desktop.jpg.bv.webp?bv_host=kingscountywakad.in",
            key_amenities="Infinity Swimming Pool, Outdoor Fitness, Cricket pitch, Gym",
            developer_id=developer.id
        )
        session.add(project)
        session.commit()
        session.refresh(project)

        # Sample data for SWOT
        swot = session.exec(
            select(SWOT).where(SWOT.category == "Strength").where(SWOT.project_id == project.id)
        ).first()
        if not swot:
            swot = SWOT(
                category="Strength",
                description="""  Competitive pricing for the carpet area 
                offered.  <br> Includes essential amenities suitable for Pros. <br> Located in Wakad, offering good 
                connectivity and infrastructure.   
                """,
                project_id=project.id
            )
            session.add(swot)
            session.commit()

        # Sample data-2 for SWOT
        swot = session.exec(
            select(SWOT).where(SWOT.category == "Weakness").where(SWOT.project_id == project.id)
        ).first()
        if not swot:
            swot = SWOT(
                category="Weakness",
                description=""" Lacks some of the luxury amenities found in 
                    premium  projects.    
                    >br> Less  brand recognition compared to larger   
                    developers.    
                    """,
                project_id=project.id
            )
            session.add(swot)
            session.commit()
            
            # Sample data for Amenity
            amenity = session.exec(
                select(Amenity).where(Amenity.amenity_name == "Swimming Pool").where(Amenity.project_id == project.id)
            ).first()
            if not amenity:
                amenity = Amenity(
                    amenity_name="Swimming Pool",
                    description="Olympic-sized swimming pool with temperature control.",
                    project_id=project.id
                )
                session.add(amenity)
                session.commit()
   
    # Sample data-2 for Project
    project = session.exec(
        select(Project).where(Project.name == "ANP Ultimus")
    ).first()
    if not project:
        project = Project(
            name="ANP Ultimus",
            location="Wakad, Pune",
            latitude=18.5933421,
            longitude=73.7537458,
            pricing_range="Rs 1.5cr - 1.58Cr",
            possession_date="Dec 2026",
            project_type="Apartments",
            website="https://www.anpultimus.com",
            reraId="P52100000154",
            description="""
              ANP Ultimus is a premium residential project
            """,
            area="1148 sq ft.",
            image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStZikRuRgU618DmYWx4EkY-Pui8Km7bv4uVw&s",
            key_amenities="Infinity Swimming Pool, Landscaped Garden, Gym",
            developer_id=developer.id
        )
        session.add(project)
        session.commit()
        session.refresh(project)
    

        # Sample data-3 for SWOT
        swot = session.exec(
            select(SWOT).where(SWOT.category == "Strength").where(SWOT.project_id == project.id)
        ).first()
        if not swot:
            swot = SWOT(
                category="Strength",
                description="""Extensive range of premium amenities 
                    catering to all age  groups.    Strategic location with excellent  Pros:  
                    connectivity to major IT hubs and the Mumbai - Pune Highway.    
                    
                    Developed by ANP Corp, known for quality 
                    
                    construction and timely  delivery.    
                    """,
                project_id=project.id
            )
            session.add(swot)
            session.commit()

        # Sample data-4 for SWOT
        swot = session.exec(
            select(SWOT).where(SWOT.category == "Weakness").where(SWOT.project_id == project.id)
        ).first()
        if not swot:
            swot = SWOT(
                category="Weakness",
                description="""Higher price point compared to other 
                    Cons projects in the  vicinity.    
                    Premium pricing may limit flexibility in unit :  customization.      
                    """,
                project_id=project.id
            )
            session.add(swot)
            session.commit()

