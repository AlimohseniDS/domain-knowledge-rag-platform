from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ConsoleSettings:
    api_base_url: str
    request_timeout_seconds: float

    @classmethod
    def from_environment(cls) -> ConsoleSettings:
        return cls(
            api_base_url=os.getenv("RAG_API_BASE_URL", "http://localhost:8000").rstrip("/"),
            request_timeout_seconds=float(os.getenv("RAG_API_TIMEOUT_SECONDS", "30")),
        )
