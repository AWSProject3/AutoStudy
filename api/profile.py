from fastapi import APIRouter, Depends, status

from core.dependencies import get_current_user
from models.repository import ProfileRepository
from schemas.profile.request import CreateProfileRequest
from schemas.profile.response import GetProfile
from services.profile_service import ProfileService


router = APIRouter(prefix='/api/profile')

# get profile
@router.get('/me', status_code=status.HTTP_200_OK, tags=["Profile"])
async def get_profile(
    current_user: dict = Depends(get_current_user),
    profile_repo: ProfileRepository = Depends(),
) -> GetProfile | None:
    return ProfileService(profile_repo, current_user).get_profile()

# create profile
@router.post('/create', status_code=status.HTTP_201_CREATED, tags=["Profile"])
async def create_profile(
    profile_request: CreateProfileRequest,
    current_user: dict = Depends(get_current_user),
    profile_repo: ProfileRepository = Depends(),
):
    return ProfileService(profile_repo, current_user).create_profile(profile_request)