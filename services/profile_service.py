from models.orm import Profile
from models.repository import ProfileRepository
from schemas.profile.request import CreateProfileRequest


class ProfileService:
    def __init__(self, repo: ProfileRepository, current_user: dict):
        self.repo = repo
        self.user = current_user

    def create_profile(self, request: CreateProfileRequest):
        repository = ProfileRepository(session=self.repo.session)
        profile: Profile = repository.create_profile(profile_data={
            "name": self.user.get("name"),
            "email": self.user.get("email"),
            "language": request.language
        })
        return {
            "name": profile.name,
            "email": profile.email,
            "language": profile.language,
        }

    def get_profile(self):
        repository = ProfileRepository(session=self.repo.session)
        profile: Profile =  repository.get_profile(email=self.user.get('email'))
        if profile is None:
            return None
        
        return {
            "name": profile.name,
            "email": profile.email,
            "language": profile.language,
        }

