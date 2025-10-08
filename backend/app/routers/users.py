from fastapi import APIRouter
from models.models import User

router =  APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get('/')
async def get_all_users():
    return [{"user":"user1"},{"user":"user2"},{"user":"user3"},{"user":"user4"},{"user":"user5"}]