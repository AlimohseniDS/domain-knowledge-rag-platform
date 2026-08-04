from __future__ import annotations

from typing import Any

import httpx

from .config import ConsoleSettings


class APIError(RuntimeError):
    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class APIClient:
    """Small typed boundary between Streamlit and the future FastAPI service."""

    def __init__(
        self,
        settings: ConsoleSettings,
        *,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.settings = settings
        self._client = httpx.Client(
            base_url=settings.api_base_url,
            timeout=settings.request_timeout_seconds,
            transport=transport,
        )

    def close(self) -> None:
        self._client.close()

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        try:
            response = self._client.request(method, path, **kwargs)
            response.raise_for_status()
        except httpx.ConnectError as exc:
            raise APIError(
                f"Cannot connect to the RAG API at {self.settings.api_base_url}."
            ) from exc
        except httpx.TimeoutException as exc:
            raise APIError("The RAG API request timed out.") from exc
        except httpx.HTTPStatusError as exc:
            detail = self._error_detail(exc.response)
            raise APIError(detail, status_code=exc.response.status_code) from exc

        if response.status_code == 204 or not response.content:
            return None
        try:
            return response.json()
        except ValueError as exc:
            raise APIError("The RAG API returned an invalid JSON response.") from exc

    @staticmethod
    def _error_detail(response: httpx.Response) -> str:
        try:
            payload = response.json()
        except ValueError:
            return f"RAG API request failed with status {response.status_code}."
        if isinstance(payload, dict):
            detail = payload.get("detail") or payload.get("message")
            if isinstance(detail, str):
                return detail
        return f"RAG API request failed with status {response.status_code}."

    def list_documents(self) -> list[dict[str, Any]]:
        payload = self._request("GET", "/documents")
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict) and isinstance(payload.get("items"), list):
            return payload["items"]
        raise APIError("The documents endpoint returned an unexpected response.")

    def upload_document(self, name: str, content: bytes, content_type: str) -> dict[str, Any]:
        payload = self._request(
            "POST",
            "/documents",
            files={"file": (name, content, content_type)},
        )
        if not isinstance(payload, dict):
            raise APIError("The upload endpoint returned an unexpected response.")
        return payload

    def delete_document(self, document_id: str) -> None:
        self._request("DELETE", f"/documents/{document_id}")

    def get_ingestion_job(self, job_id: str) -> dict[str, Any]:
        payload = self._request("GET", f"/ingestion-jobs/{job_id}")
        if not isinstance(payload, dict):
            raise APIError("The ingestion endpoint returned an unexpected response.")
        return payload

    def chat(
        self,
        question: str,
        *,
        conversation_id: str | None = None,
        model: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"question": question}
        if conversation_id:
            body["conversation_id"] = conversation_id
        if model:
            body["model"] = model
        payload = self._request("POST", "/chat", json=body)
        if not isinstance(payload, dict):
            raise APIError("The chat endpoint returned an unexpected response.")
        return payload

    def debug_retrieval(self, query: str, *, top_k: int = 8) -> dict[str, Any]:
        payload = self._request(
            "POST",
            "/retrieval/debug",
            json={"query": query, "top_k": top_k},
        )
        if not isinstance(payload, dict):
            raise APIError("The retrieval endpoint returned an unexpected response.")
        return payload

    def health(self) -> dict[str, Any]:
        payload = self._request("GET", "/health")
        return payload if isinstance(payload, dict) else {"status": "ok"}

    def readiness(self) -> dict[str, Any]:
        payload = self._request("GET", "/ready")
        return payload if isinstance(payload, dict) else {"status": "ready"}
