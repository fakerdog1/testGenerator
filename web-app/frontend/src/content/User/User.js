import { useTranslation } from 'react-i18next';
import styles from './User.module.scss';

const User = (props) => {
    const { t } = useTranslation('translations');

    return (
        <div className={styles.page}>
            <h1>{t('User_Page.title')}</h1>
        </div>
    );
}
export default User