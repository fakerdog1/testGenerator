import CONSTANTS from './../../modules/CONSTANTS.json';

const Logout = (props) => {
    const delete_cookie = (name) => {
        document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }
    delete_cookie(CONSTANTS.JWT_COOKIE_NAME)
    props.postLogOut()
    window.location.replace("/")

    return (
        <div>
            Logging out...
        </div>
    )
}
export default Logout;