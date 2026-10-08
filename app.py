import tempfile
from pathlib import Path
from uuid import uuid4

from flask import Flask, render_template_string, request, send_from_directory
from werkzeug.utils import secure_filename
from pypdf import PdfReader
from pypdf.errors import PdfReadError


app = Flask(__name__)
PROCESSED_FOLDER = Path(__file__).parent / "processed"

PAGE = """\
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>PDF to Text</title>
    <style>
        :root { color-scheme: light; font-family: Arial, sans-serif; }
        body { background: #f4f6f8; margin: 0; padding: 2rem; color: #17202a; }
        main { background: white; border-radius: 10px; box-shadow: 0 2px 12px #0001;
               margin: auto; max-width: 800px; padding: 2rem; }
        h1 { margin-top: 0; }
        form { align-items: center; display: flex; flex-wrap: wrap; gap: 1rem; }
        button { background: #1769aa; border: 0; border-radius: 5px; color: white;
                 cursor: pointer; padding: .65rem 1rem; }
        button:hover { background: #125486; }
        .error { color: #b42318; }
        textarea { box-sizing: border-box; font: 14px/1.5 monospace; margin-top: 1rem;
                   min-height: 350px; padding: .75rem; resize: vertical; width: 100%; }
        a { color: #1769aa; }
    </style>
</head>
<body>
<main>
    <h1>PDF to Text</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="pdf" accept=".pdf,application/pdf" required>
        <button type="submit">Process PDF</button>
    </form>
    {% if error %}<p class="error">{{ error }}</p>{% endif %}
    {% if output %}
        <p>Processed successfully. Saved as
            <a href="{{ url_for('download', filename=filename) }}">{{ filename }}</a>.
        </p>
        <textarea readonly aria-label="Extracted text">{{ output }}</textarea>
    {% endif %}
</main>
</body>
</html>
"""


def extract_text(pdf_path: str, output_path: str) -> None:
    reader = PdfReader(pdf_path)

    text = "\n\n".join(
        page.extract_text() or ""
        for page in reader.pages
    )

    Path(output_path).write_text(text, encoding="utf-8")


@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    filename = None
    error = None

    if request.method == "POST":
        uploaded_file = request.files.get("pdf")
        if uploaded_file is None or not uploaded_file.filename:
            error = "Please choose a PDF file."
        elif Path(uploaded_file.filename).suffix.lower() != ".pdf":
            error = "Only PDF files are supported."
        else:
            safe_name = secure_filename(uploaded_file.filename)
            stem = Path(safe_name).stem or "document"
            filename = f"{stem}_{uuid4().hex[:8]}.txt"
            temporary_path = None
            try:
                PROCESSED_FOLDER.mkdir(exist_ok=True)
                with tempfile.NamedTemporaryFile(
                    suffix=".pdf", delete=False
                ) as temporary_file:
                    uploaded_file.save(temporary_file)
                    temporary_path = Path(temporary_file.name)

                output_path = PROCESSED_FOLDER / filename
                extract_text(str(temporary_path), str(output_path))
                output = output_path.read_text(encoding="utf-8")
            except (OSError, PdfReadError) as exc:
                filename = None
                error = f"Could not process the PDF: {exc}"
            finally:
                if temporary_path is not None:
                    temporary_path.unlink(missing_ok=True)

    return render_template_string(
        PAGE, output=output, filename=filename, error=error
    )


@app.get("/processed/<path:filename>")
def download(filename):
    return send_from_directory(PROCESSED_FOLDER, filename, as_attachment=True)


if __name__ == "__main__":
    app.run()