// import styles from './Navbar.module.scss';
import { Navbar, Nav } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

const Navigation = (props) => {
    return (
        <Navbar bg="light" expand="lg">
            <Navbar.Brand href="/">E-Ducation</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                    <LinkContainer to={'/'}>
                        <Nav.Link>Home</Nav.Link>
                    </LinkContainer>
                    <LinkContainer to={'/test_page'}>
                        <Nav.Link>Test</Nav.Link>
                    </LinkContainer>
                    <LinkContainer to={'/history'}>
                        <Nav.Link>History</Nav.Link>
                    </LinkContainer>
                    <LinkContainer to={'/search'}>
                        <Nav.Link>Search</Nav.Link>
                    </LinkContainer>
                    {(!props.loggedIn) &&
                        <LinkContainer to={'/login'}>
                            <Nav.Link>Login</Nav.Link>
                        </LinkContainer>
                    }
                    {(props.loggedIn) &&
                        <LinkContainer to={'/logout'}>
                            <Nav.Link>Logout</Nav.Link>
                        </LinkContainer>
                    }

                    <LinkContainer to={'/user'}>
                        <Nav.Link>User</Nav.Link>
                    </LinkContainer>
                </Nav>
            </Navbar.Collapse>
        </Navbar >
    )
}

export default Navigation;