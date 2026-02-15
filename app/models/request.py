from pydantic import BaseModel, Field


class RewardRequest(BaseModel):
    txn_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    merchant_id: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    txn_type: str
    ts: int