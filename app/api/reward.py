from fastapi import APIRouter, Depends, status

from app.models.request import RewardRequest
from app.models.response import RewardResponse
from app.services.reward_service import RewardService

router = APIRouter(
    prefix="/reward",
    tags=["reward"],
)


def get_reward_service() -> RewardService:
    from app.main import reward_service
    return reward_service


@router.post(
    "/decide",
    response_model=RewardResponse,
    status_code=status.HTTP_200_OK,
)
async def decide_reward(
    request: RewardRequest,
    service: RewardService = Depends(get_reward_service),
) -> RewardResponse:
    return await service.decide(request)