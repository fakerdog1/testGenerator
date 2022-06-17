import styles from './History.module.scss';
import { useTranslation } from 'react-i18next';

const History = (props) => {
    const { t } = useTranslation('translations');

    return (
        <div className={styles.page}>
            <h1>{t('History_Page.title')}</h1>
        </div>
    )
}
export default History;