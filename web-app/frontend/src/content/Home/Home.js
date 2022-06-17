import styles from './Home.module.scss';
import { Row, Col } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';

const Homepage = (props) => {
    const { t } = useTranslation('translations');

    return (
        <div className={styles.page}>
            <Row>
                <Col md={2} lg={1} />
                <Col md={8} lg={10}>
                    <h1>{t('Home_Page.title')}</h1>
                </Col>
                <Col md={2} lg={1} />
            </Row>
        </div>
    )
}
export default Homepage;