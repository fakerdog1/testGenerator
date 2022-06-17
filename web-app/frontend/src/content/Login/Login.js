import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import styles from './Login.module.scss';
import LoginForm from './../../components/LoginForm';
import RegisterForm from './../../components/RegisterForm';

const Login = (props) => {
    const { t } = useTranslation('translations');
    const validActions = ["login", "register"];
    const [action, setAction] = useState("login")
    const [nextAction, setNextAction] = useState("register")

    const toggleAction = () => {
        let index = validActions.indexOf(action);

        index = (index + 1) % validActions.length;
        setAction(validActions[index]);

        index = (index + 1) % validActions.length;
        setNextAction(validActions[index]);
    }

    const registrationComplete = () => {
        setAction(validActions[validActions.indexOf('login')]);
        setNextAction(validActions[(validActions.indexOf('login') + 1) % validActions.length]);
    }

    return (
        <div className={styles.page}>
            <h1>{t("Login_Page.title")}</h1>
            <h2>{t(`Login_Page.actions.${action}`)}</h2>
            <div>
                <div>
                    {(action === "login") &&
                        <LoginForm
                            postLogIn={props.postLogIn}
                        />
                    }
                    {(action === "register") &&
                        <RegisterForm
                            registrationComplete={registrationComplete}
                        /> 
                    }
                </div>
                <br />
                <button
                    onClick={toggleAction}
                >
                    {t(`Login_Page.actions.${nextAction}`)}
                </button>
            </div>
        </div>
    )
}

export default Login;