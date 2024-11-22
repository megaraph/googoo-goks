import React, { useState } from "react";
import { Container, Row, Col, Form, Button, Card } from "react-bootstrap";

interface Metrics {
    total_essays: number;
    valid_essays: number;
    invalid_essays: number;
    possibly_ai_essays: number;
}

const FormLayout: React.FC = () => {
    const [sourceMaterial, setSourceMaterial] = useState("");
    const [reflectionSheet, setReflectionSheet] = useState<File | null>(null);
    const [isLoading, setIsLoading] = useState(false); // Loading state
    const [metrics, setMetrics] = useState<Metrics | null>(null); // State to hold metrics
    const [csvUrl, setCsvUrl] = useState<string | null>(null); // State to hold CSV URL

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault(); // Prevent the default form submission
        setIsLoading(true); // Set loading state to true

        const formData = new FormData();
        formData.append("source_material", sourceMaterial);
        if (reflectionSheet) {
            formData.append("reflection_sheet", reflectionSheet);
        }

        try {
            const response = await fetch(
                "http://127.0.0.1:5000/api/process_essay",
                {
                    method: "POST",
                    body: formData,
                }
            );

            if (response.ok) {
                const result = await response.json();
                console.log("Success:", result);
                setMetrics(result.metrics); // Set metrics from the response
                setCsvUrl(result.csv_url); // Set CSV URL from the response
            } else {
                const error = await response.json();
                console.error("Error:", error);
            }
        } catch (error) {
            console.error("Error submitting form:", error);
        } finally {
            setIsLoading(false); // Reset loading state after the request is complete
        }
    };

    return (
        <Container fluid className="mt-4">
            <Row
                className="justify-content-center align-items-center"
                style={{ height: "calc(100vh - 64px)" }} // Adjust height to account for navbar
            >
                {/* Left Side: Source Material */}
                <Col
                    md={5}
                    className="d-flex align-items-center justify-content-end pe-5"
                >
                    <Form.Group
                        controlId="sourceMaterial"
                        style={{ width: "100%" }}
                    >
                        <Form.Label style={{ fontSize: "24px" }}>
                            Source Material
                        </Form.Label>
                        <Form.Control
                            as="textarea"
                            rows={15}
                            placeholder="Enter your source material here..."
                            style={{ height: "50%", resize: "none" }}
                            value={sourceMaterial}
                            onChange={(e) => setSourceMaterial(e.target.value)} // Update state on change
                        />
                    </Form.Group>
                </Col>

                {/* Right Side: File Upload and Submit Button */}
                <Col
                    md={5}
                    className="d-flex flex-column align-items-start justify-content-center ps-5"
                >
                    <Form.Group controlId="fileUpload" className="mb-3">
                        <Form.Label style={{ fontSize: "18px" }}>
                            Upload your reflection sheets here (.csv)
                        </Form.Label>
                        <Form.Control
                            type="file"
                            accept=".csv" // Restrict file type to CSV
                            onChange={(
                                e: React.ChangeEvent<HTMLInputElement>
                            ) => {
                                if (
                                    e.target.files &&
                                    e.target.files.length > 0
                                ) {
                                    setReflectionSheet(e.target.files[0]); // Safely access files
                                }
                            }}
                        />
                    </Form.Group>
                    <Button
                        variant="primary"
                        type="submit"
                        onClick={handleSubmit}
                        disabled={isLoading}
                    >
                        {isLoading ? "Uploading..." : "Submit"}{" "}
                        {/* Change button text while loading */}
                    </Button>
                </Col>
            </Row>

            {/* Display Metrics and Download Link */}
            {metrics && (
                <Row className="mt-4">
                    <Col md={12}>
                        <Card>
                            <Card.Body>
                                <Card.Title>Metrics</Card.Title>
                                <Card.Text>
                                    <p>Total Essays: {metrics.total_essays}</p>
                                    <p>Valid Essays: {metrics.valid_essays}</p>
                                    <p>
                                        Invalid Essays: {metrics.invalid_essays}
                                    </p>
                                    <p>
                                        Possibly AI Essays:{" "}
                                        {metrics.possibly_ai_essays}
                                    </p>
                                </Card.Text>
                                {csvUrl && (
                                    <div className="mt-3">
                                        <a
                                            href={csvUrl}
                                            className="btn btn-success"
                                            download
                                        >
                                            Download full report
                                        </a>
                                    </div>
                                )}
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            )}
        </Container>
    );
};
export default FormLayout;
