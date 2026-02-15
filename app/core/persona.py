from typing import Dict


_PERSONA_MAP: Dict[str, str] = {
    "user_new": "NEW",
    "user_power": "POWER",
}


def get_persona(user_id: str) -> str:
    return _PERSONA_MAP.get(user_id, "RETURNING")