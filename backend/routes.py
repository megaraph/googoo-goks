from app import app, db
from flask import request, jsonify
import csv


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
        for row in csv_reader:
            reflection_sheet_content.append(
                ", ".join(row)
            )  # Join each row into a string

        # Combine all rows into a single string or process them as needed
        reflection_sheet = "\n".join(reflection_sheet_content)
    else:
        return jsonify({"error": "Reflection sheet file is required."}), 400

    # Here you can add any processing logic or just return the received data for testing
    return (
        jsonify(
            {
                "source_material": source_material,
                "reflection_sheet": reflection_sheet,
                "message": "Data received successfully!",
            }
        ),
        200,
    )
