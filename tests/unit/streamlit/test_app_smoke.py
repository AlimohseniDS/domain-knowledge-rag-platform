from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
APP_FILES = [
    REPOSITORY_ROOT / "apps/streamlit/app.py",
    REPOSITORY_ROOT / "apps/streamlit/pages/01_Documents.py",
    REPOSITORY_ROOT / "apps/streamlit/pages/02_Chat.py",
    REPOSITORY_ROOT / "apps/streamlit/pages/03_Retrieval_Debug.py",
    REPOSITORY_ROOT / "apps/streamlit/pages/04_System_Status.py",
]


@pytest.mark.parametrize("app_file", APP_FILES, ids=lambda path: path.stem)
def test_page_loads_when_api_is_unavailable(app_file: Path, monkeypatch) -> None:
    monkeypatch.setenv("RAG_API_BASE_URL", "http://127.0.0.1:1")
    app = AppTest.from_file(str(app_file), default_timeout=5).run()
    assert not app.exception
