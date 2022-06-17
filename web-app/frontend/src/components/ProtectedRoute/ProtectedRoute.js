const ProtectedRoute = (props) => {
    if (!props.authenticated) {
        const destination = window.location.pathname;
        window.location.replace(`/login/?next=${destination}`)
    }
    else {
        return (
            props.component
        )
    }
}
export default ProtectedRoute