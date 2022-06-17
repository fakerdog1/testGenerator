import styles from './RegisterForm.module.scss';
import CONSTANTS from './../../modules/CONSTANTS.json';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { sendRequest as submitForm } from './../../modules/requests';
import { useHistory } from "react-router-dom";

const RegisterForm = (props) => {
    const { t } = useTranslation('translations');

    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [password_2, setPassword_2] = useState("")
    const [email, setEmail] = useState("")
    const [email_2, setEmail_2] = useState("")
    const [errorMsgs, setErrorMsgs] = useState([])
    const [responseError, setResponseError] = useState([])
    const history = useHistory()

    const handleFormSubmit = (event) => {
        event.preventDefault();
        setErrorMsgs([])

        const errors = getFormErrors()
        if (errors.length === 0) {
            const address = `${CONSTANTS.AUTH_API_ADDRESS}/register`
            const body = JSON.stringify({
                "username": username,
                "password": password,
                "email": email
            })

            submitForm('POST', address, body).then(data => {
                if (parseInt(data.code) === 200) {
                    history.push("/register_acc_type")
                }
                if (parseInt(data.code) === 400) {
                    if (data.message.toLowerCase() === "Invalid email".toLowerCase())
                        setResponseError(createErrorMsg(t('RegisterForm_Component.errors.invalid_email')))
                    if (data.message.toLowerCase() === "Username already in use".toLowerCase())
                        setResponseError(t("RegisterForm_Component.errors.username_in_use"))
                    if (data.message.toLowerCase() === "Email already in use".toLowerCase())
                        setResponseError(t("RegisterForm_Component.errors.email_in_use"))
                }
            })
        }
        else setErrorMsgs(errors)
    }

    const getFormErrors = () => {
        const errors = [];
        if (username.length === 0) errors.push(createErrorMsg(t('RegisterForm_Component.errors.empty_username')))
        if (password.length === 0) errors.push(createErrorMsg(t('RegisterForm_Component.errors.empty_password')))
        else {
            if (password.length < 8) errors.push(createErrorMsg(t('RegisterForm_Component.errors.short_password')))
            if (password !== password_2) errors.push(createErrorMsg(t('RegisterForm_Component.errors.password_mismatch')))
        }
        if (email.length === 0) errors.push(createErrorMsg(t('RegisterForm_Component.errors.empty_email')))
        else {
            if (!validateEmail(email)) errors.push(createErrorMsg(t('RegisterForm_Component.errors.invalid_email')))
            if (email !== email_2) errors.push(createErrorMsg(t('RegisterForm_Component.errors.email_mismatch')))
        }
        return errors;
    }

    function validateEmail(email) {
        const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
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
                    <label>{t('RegisterForm_Component.labels.username')}</label>
                    <br />
                    <input
                        value={username}
                        onChange={e => setUsername(e.target.value.trim())}
                    />
                </div>
                <div>
                    <label>{t('RegisterForm_Component.labels.password')}</label>
                    <br />
                    <input
                        value={password}
                        onChange={e => setPassword(e.target.value.trim())}
                    />
                </div>
                <div>
                    <label>{t('RegisterForm_Component.labels.repeat_password')}</label>
                    <br />
                    <input
                        value={password_2}
                        onChange={e => setPassword_2(e.target.value.trim())}
                    />
                </div>
                <div>
                    <label>{t('RegisterForm_Component.labels.email')}</label>
                    <br />
                    <input
                        value={email}
                        onChange={e => setEmail(e.target.value.trim().toLowerCase())}
                    />
                </div>
                <div>
                    <label>{t('RegisterForm_Component.labels.repeat_email')}</label>
                    <br />
                    <input
                        value={email_2}
                        onChange={e => setEmail_2(e.target.value.trim().toLowerCase())}
                    />
                </div>
                <br />
                    <button
                        onClick={handleFormSubmit}
                    >
                        {t('RegisterForm_Component.labels.submit')}
                    </button>
            </form>
        </div>
    )
}
export default RegisterForm