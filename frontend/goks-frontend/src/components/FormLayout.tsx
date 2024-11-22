import React from "react";
import { Container, Row, Col, Form, Button } from "react-bootstrap";

const FormLayout: React.FC = () => {
    return (
        <Container fluid className="mt-4">
            {" "}
            {/* Adjust spacing below the navbar */}
            <Row
                className="justify-content-center align-items-center"
                style={{ height: "calc(100vh - 64px)" }} // Adjust height to account for navbar
            >
                {/* Left Side: Source Material */}
                <Col
                    md={5} // Maintain column width
                    className="d-flex align-items-center justify-content-end pe-5" // Add padding to the right
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
                        />
                    </Form.Group>
                </Col>

                {/* Right Side: File Upload and Submit Button */}
                <Col
                    md={5} // Maintain column width
                    className="d-flex flex-column align-items-start justify-content-center ps-5" // Add padding to the left
                >
                    <Form.Group controlId="fileUpload" className="mb-3">
                        <Form.Label style={{ fontSize: "18px" }}>
                            Upload your reflection sheets here
                        </Form.Label>
                        <Form.Control type="file" />
                    </Form.Group>
                    <Button variant="primary" type="submit">
                        Submit
                    </Button>
                </Col>
            </Row>
        </Container>
    );
};

export default FormLayout;
