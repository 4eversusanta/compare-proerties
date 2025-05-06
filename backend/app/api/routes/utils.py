from fastapi import APIRouter, Depends, HTTPException
from pydantic.networks import EmailStr

from app.api.deps import get_current_active_superuser
from app.models import Message
from app.utils import generate_test_email, send_email
import subprocess


router = APIRouter(prefix="/utils", tags=["utils"])


@router.post(
    "/test-email/",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
def test_email(email_to: EmailStr) -> Message:
    """
    Test emails.
    """
    email_data = generate_test_email(email_to=email_to)
    send_email(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Test email sent")


@router.get("/health-check/")
async def health_check() -> bool:
    return True

@router.post("/run-migrations/", dependencies=[Depends(get_current_active_superuser)])
def run_migrations_and_seed_data():
    """
    Run Alembic migrations and seed initial data.
    """
    try:
        # Run Alembic migrations
        alembic_result = subprocess.run(
            ["alembic", "upgrade", "head"], check=True, capture_output=True, text=True
        )
        # Run initial data script
        seed_result = subprocess.run(
            ["python", "app/initial_data.py"], check=True, capture_output=True, text=True
        )
        return {
            "message": "Migrations and initial data script executed successfully.",
            "alembic_output": alembic_result.stdout,
            "seed_output": seed_result.stdout,
        }
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error occurred: {e.stderr or str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}",
        )