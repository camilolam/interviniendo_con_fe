from fastapi import APIRouter
from models.models import Service

router =  APIRouter(
    prefix="/services",
    tags=["services"],
)

@router.get('/')
async def get_all_services():
    return [{"user":"user1"},{"user":"user2"},{"user":"user3"},{"user":"user4"},{"user":"user5"}]