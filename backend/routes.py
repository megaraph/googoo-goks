import os
from app import app
from flask import request, jsonify, send_file
from utils import (
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

# Directory to store generated CSV files
CSV_DIRECTORY = "generated_csvs/"
os.makedirs(CSV_DIRECTORY, exist_ok=True)


@app.route("/api/process_essay", methods=["GET"])
def get_page():
    return jsonify({"msg": "hello"})


@app.route("/api/process_essay", methods=["POST"])
def process_essay():
    source_material = request.form.get("source_material")
    reflection_sheet_file = request.files.get("reflection_sheet", "")

    if reflection_sheet_file:
        # Read the contents of the reflection sheet CSV file
        csv_reader = csv.reader(
            reflection_sheet_file.stream.read().decode("utf-8").splitlines()
        )

        # Read the first row as the question
        question = next(csv_reader)[0]  # Assuming the first row contains the question

        # Prepare to store results
        results = []
        total_essays = 0
        valid_essays = 0
        invalid_essays = 0
        possibly_ai_essays = 0

        # Process each essay
        for row in csv_reader:  # Skip the first row (the question)
            print("Extracting data...")
            essay = row[0]  # Assuming the essay is in the first column

            # Increment the total essays count
            total_essays += 1

            # Get scores for each phase and plagiarism
            phase_1_score = get_phase_score(question, essay, phase=1)
            phase_2_score = get_phase_score(
                question, essay, source_material=source_material, phase=2
            )
            plagiarism_score = get_plagiarism_score(essay, WINSTON_headers)
            ai_score = get_ai_score(essay, WINSTON_headers)

            # Validation checks
            is_phase_1_valid = phase_1_score >= 4
            is_phase_2_valid = phase_2_score >= 4
            is_plagiarism_valid = plagiarism_score <= 60

            # Determine if the essay is valid
            is_valid = is_phase_1_valid and is_phase_2_valid and is_plagiarism_valid

            # Update valid and invalid counts
            if is_valid:
                valid_essays += 1
            else:
                invalid_essays += 1

            # Check if the essay is possibly AI
            if ai_score < 50:
                possibly_ai_essays += 1

            # Append results as a dictionary
            results.append(
                {
                    "essay": essay,
                    "phase_1_score": phase_1_score,
                    "phase_2_score": phase_2_score,
                    "plagiarism_score": plagiarism_score,
                    "ai_score": ai_score,
                    "valid": is_valid,  # Add validity status
                }
            )

        # Prepare metrics
        metrics = {
            "total_essays": total_essays,
            "valid_essays": valid_essays,
            "invalid_essays": invalid_essays,
            "possibly_ai_essays": possibly_ai_essays,
        }

        # Create a CSV in memory
        csv_filename = os.path.join(CSV_DIRECTORY, "scored_essays.csv")
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as output_file:
            csv_writer = csv.writer(output_file)
            # Write the header
            csv_writer.writerow(
                [
                    "Essay",
                    "Phase 1 Score",
                    "Phase 2 Score",
                    "Plagiarism Score",
                    "AI Score",
                    "Valid",
                ]
            )
            # Write each result
            for result in results:
                csv_writer.writerow(
                    [
                        result["essay"],
                        result["phase_1_score"],
                        result["phase_2_score"],
                        result["plagiarism_score"],
                        result["ai_score"],
                        result["valid"],
                    ]
                )

        # Return metrics and CSV URL
        return (
            jsonify(
                {
                    "question": question,
                    "metrics": metrics,
                    "csv_url": f"/download_csv/scored_essays.csv",
                    "message": "Essays processed successfully!",
                }
            ),
            200,
        )

    else:
        return jsonify({"error": "Reflection sheet file is required."}), 400


@app.route("/download_csv/<path:filename>", methods=["GET"])
def download_csv(filename):
    # Construct the full path to the CSV file
    file_path = os.path.join(CSV_DIRECTORY, filename)

    # Check if the file exists
    if os.path.exists(file_path):
        return send_file(
            file_path, as_attachment=True, mimetype="text/csv", download_name=filename
        )
    else:
        return jsonify({"error": "File not found."}), 404
