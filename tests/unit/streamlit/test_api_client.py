import json

import httpx
import pytest
from rag_console.client import APIClient, APIError
from rag_console.config import ConsoleSettings


def build_client(handler) -> APIClient:
    return APIClient(
        ConsoleSettings(api_base_url="http://test-api", request_timeout_seconds=1),
        transport=httpx.MockTransport(handler),
    )


def test_list_documents_accepts_paginated_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/documents"
        return httpx.Response(200, json={"items": [{"id": "doc-1"}]})

    client = build_client(handler)
    assert client.list_documents() == [{"id": "doc-1"}]


def test_upload_uses_multipart_file_field() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/documents"
        assert request.method == "POST"
        assert "multipart/form-data" in request.headers["content-type"]
        return httpx.Response(202, json={"document_id": "doc-1", "job_id": "job-1"})

    client = build_client(handler)
    result = client.upload_document("guide.txt", b"domain knowledge", "text/plain")
    assert result["job_id"] == "job-1"


def test_chat_sends_question_and_optional_model() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert body == {"question": "What is RAG?", "model": "local-model"}
        return httpx.Response(200, json={"answer": "Grounded answer", "citations": []})

    client = build_client(handler)
    result = client.chat("What is RAG?", model="local-model")
    assert result["answer"] == "Grounded answer"


def test_http_error_exposes_api_detail() -> None:
    client = build_client(
        lambda request: httpx.Response(422, json={"detail": "Unsupported document"})
    )

    with pytest.raises(APIError, match="Unsupported document") as captured:
        client.list_documents()

    assert captured.value.status_code == 422
