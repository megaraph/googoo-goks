import Container from "react-bootstrap/Container";
import Navbar from "react-bootstrap/Navbar";

function MyNavbar() {
    return (
        <>
            <Navbar className="bg-body-tertiary">
                <Container className="d-flex justify-content-center">
                    <Navbar.Brand
                        href="#home"
                        className="d-flex align-items-center"
                    >
                        <img
                            alt=""
                            src="/img/logo.svg"
                            width="30"
                            height="30"
                            className="d-inline-block align-top me-2" // Add margin to the right
                        />
                        GOKS
                    </Navbar.Brand>
                </Container>
            </Navbar>
        </>
    );
}

export default MyNavbar;
