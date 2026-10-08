from io import BytesIO
from importlib.metadata import version

from app import app


def test_required_packages_are_installed():
    assert version("Flask")
    assert version("pypdf")


def test_home_page_is_available():
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert b"PDF to Text" in response.data


def test_non_pdf_upload_is_rejected():
    response = app.test_client().post(
        "/",
        data={"pdf": (BytesIO(b"not a PDF"), "document.txt")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    assert b"Only PDF files are supported." in response.data
