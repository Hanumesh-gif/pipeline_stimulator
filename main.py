import os
import time
from flask import Flask, request, jsonify, send_from_directory, render_template
from werkzeug.utils import secure_filename
from celery.exceptions import CeleryError
from worker.celery_worker import run_pipeline as celery_run_pipeline
from pipeline import run_pipeline as pipeline_run

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
RESULT_FOLDER = os.path.join(BASE_DIR, "results")
ALLOWED_EXTENSIONS = {".fastq.gz", ".fq.gz", ".fastq", ".fq"}
SYNC_TASKS = {}

app = Flask(__name__, template_folder="templates")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER

for folder in (UPLOAD_FOLDER, RESULT_FOLDER):
    os.makedirs(folder, exist_ok=True)


def allowed_file(filename):
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)


@app.route("/")
def home():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(uploaded_file.filename):
        return jsonify({"error": "Only .fastq.gz or .fq.gz files are accepted"}), 400

    filename = secure_filename(uploaded_file.filename)
    timestamp = int(time.time())
    save_name = f"{timestamp}_{filename}"
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], save_name)
    uploaded_file.save(save_path)

    try:
        task = celery_run_pipeline.delay(save_path)
        return jsonify({
            "message": "Upload received",
            "task_id": task.id,
            "status_url": f"/status/{task.id}",
            "results_url": f"/results/{task.id}"
        }), 202
    except CeleryError:
        task_id = f"sync-{timestamp}"
        result = pipeline_run(save_path, task_id)
        SYNC_TASKS[task_id] = result
        return jsonify({
            "message": "Upload processed synchronously because task queue was unavailable.",
            "task_id": task_id,
            "status_url": f"/status/{task_id}",
            "results_url": f"/results/{task_id}",
            "result": result
        }), 200


@app.route("/status/<task_id>")
def status(task_id):
    if task_id in SYNC_TASKS:
        return jsonify(SYNC_TASKS[task_id])

    try:
        result = celery_run_pipeline.AsyncResult(task_id)
        state = result.state
    except Exception:
        return jsonify({"status": "pending", "message": "Task backend unavailable"}), 200

    if state == "PENDING":
        return jsonify({"status": "pending"})

    # Treat STARTED/RETRY/PROGRESS as in-progress so the UI can show partial results
    if state in ("PROGRESS", "STARTED", "RETRY"):
        meta = result.result or {"status": "progress"}
        return jsonify(meta)

    if state == "FAILURE":
        return jsonify({"status": "failure", "error": str(result.result)}), 500

    if state == "SUCCESS":
        return jsonify(result.result)

    return jsonify({"status": state})


@app.route("/results/<task_id>")
def results(task_id):
    task_folder = os.path.join(app.config["RESULT_FOLDER"], task_id)
    if not os.path.isdir(task_folder):
        return jsonify({"error": "Results not found"}), 404

    files = sorted(os.listdir(task_folder))
    return jsonify({
        "task_id": task_id,
        "result_folder": f"/download/{task_id}/",
        "files": files,
        "download_urls": [f"/download/{task_id}/{filename}" for filename in files]
    })


@app.route("/download/<task_id>/<path:filename>")
def download(task_id, filename):
    task_folder = os.path.join(app.config["RESULT_FOLDER"], task_id)
    if not os.path.isdir(task_folder):
        return jsonify({"error": "Results not found"}), 404

    return send_from_directory(task_folder, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
