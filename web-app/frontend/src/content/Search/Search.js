import styles from './Search.module.scss';
import { useTranslation } from 'react-i18next';

const Search = (props) => {
    const { t } = useTranslation('translations');

    return (
        <div className={styles.page}>
            <h1>{t('Search_Page.title')}</h1>
        </div>
    )
}
export default Search;