import os
from app import app
from flask import request, jsonify
from utils import (
    get_phase_one,
    get_phase_two,
    get_phase_score,
    get_ai_score,
    get_plagiarism_score,
)
import csv

winston_key = os.getenv("WINSTON_API_KEY")
WINSTON_headers = {
    "Authorization": f"Bearer {winston_key}",
    "Content-Type": "application/json",
}


@app.route("/api/process_essay", methods=["GET"])
def get_page():
    return jsonify({"msg": "hello"})


@app.route("/api/process_essay", methods=["POST"])
def process_essay():
    source_material = request.form.get("source_material")
    reflection_sheet_file = request.files.get("reflection_sheet", "")

    if reflection_sheet_file:
        # Read the contents of the reflection sheet CSV file
        reflection_sheet_content = []
        csv_reader = csv.reader(
            reflection_sheet_file.stream.read().decode("utf-8").splitlines()
        )

        # Read the first row as the question
        question = next(csv_reader)[0]  # Assuming the first row contains the question

        # Prepare to store results
        results = []

        # Process each essay
        for row in csv_reader:  # Skip the first row (the question)
            print("Extracting data...")
            essay = row[0]  # Assuming the essay is in the first column

            # Get scores for each phase and plagiarism
            phase_1_score = get_phase_score(question, essay, phase=1)
            phase_2_score = get_phase_score(
                question, essay, source_material=source_material, phase=2
            )
            plagiarism_score = get_plagiarism_score(essay, WINSTON_headers)
            ai_score = get_ai_score(essay, WINSTON_headers)

            # Append results as a dictionary
            results.append(
                {
                    "essay": essay,
                    "phase_1_score": phase_1_score,
                    "phase_2_score": phase_2_score,
                    "plagiarism_score": plagiarism_score,
                    "ai_score": ai_score,
                }
            )

        # Return the results as JSON
        return (
            jsonify(
                {
                    "question": question,
                    "results": results,
                    "message": "Essays processed successfully!",
                }
            ),
            200,
        )

    else:
        return jsonify({"error": "Reflection sheet file is required."}), 400
