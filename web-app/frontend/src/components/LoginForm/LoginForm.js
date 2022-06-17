import styles from './LoginForm.module.scss';
import CONSTANTS from './../../modules/CONSTANTS.json';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { sendRequest as submitForm } from './../../modules/requests';

const LoginForm = (props) => {
    const { t } = useTranslation('translations');

    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [errorMsgs, setErrorMsgs] = useState("")
    const [responseError, setResponseError] = useState([])


    const handleFormSubmit = (event) => {
        event.preventDefault();
        setErrorMsgs([])

        const errors = getFormErrors()
        if (errors.length === 0) {
            try {
                const address = `${CONSTANTS.AUTH_API_ADDRESS}/auth`
                const body = JSON.stringify({
                    "username": username,
                    "password": password
                })

                submitForm('POST', address, body).then(data => {
                    if (parseInt(data.code) === 200) {
                        props.postLogIn()
                        const urlParams = new URLSearchParams(window.location.search);
                        const destination = urlParams.get('next');
                        if (destination) {
                            if (!validURL(destination)) window.location.replace(destination)
                            else window.location.replace("/")
                        }
                        else
                            window.location.replace("/")
                    }
                    if (parseInt(data.code) === 403) {
                        setResponseError(createErrorMsg(t('LoginForm_Component.errors.wrong_credentials')))
                    }
                    setErrorMsgs(errors);
                });
            } catch (err) {
                console.error(err);
                errors.push(
                    createErrorMsg(t('LoginForm_Component.errors.network_error'))
                )
                setErrorMsgs(errors);
            }
        }
        else setErrorMsgs(errors);
    }

    const getFormErrors = () => {
        const errors = []
        if (username.length === 0) errors.push(createErrorMsg(t('LoginForm_Component.errors.empty_username')))
        if (password.length === 0) errors.push(createErrorMsg(t('LoginForm_Component.errors.empty_password')))
        else {
            if (password.length < 8) errors.push(createErrorMsg(t('LoginForm_Component.errors.short_password')))
        }
        return errors
    }

    const createErrorMsg = (txt) => {
        return (
            <li key={txt} className={styles.errorsItem}>
                {txt}
            </li>
        )
    }

    return (
        <div>
            <div>
                <ul className={styles.errors}>
                    {errorMsgs}
                    {responseError}
                </ul>
            </div>
            <form>
                <div>
                    <label>{t('LoginForm_Component.labels.username')}</label>
                    <br />
                    <input
                        value={username}
                        onChange={e => setUsername(e.target.value.trim())}
                    />
                </div>
                <div>
                    <label>{t('LoginForm_Component.labels.password')}</label>
                    <br />
                    <input
                        value={password}
                        type="password"
                        onChange={e => setPassword(e.target.value.trim())}
                    />
                </div>
                <br />
                <button onClick={handleFormSubmit}>
                    {t('LoginForm_Component.labels.submit')}
                </button>
            </form>
        </div>
    )
}
export default LoginForm

const validURL = (str) => {
    var pattern = new RegExp('^(https?:\\/\\/)?' + // protocol
        '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
        '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR ip (v4) address
        '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
        '(\\#[-a-z\\d_]*)?$', 'i'); // fragment locator
    return !!pattern.test(str);
}