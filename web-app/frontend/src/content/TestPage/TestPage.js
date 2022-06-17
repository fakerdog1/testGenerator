import styles from './TestPage.module.scss';
import { useTranslation } from 'react-i18next';
import CONSTANTS from '../../modules/CONSTANTS.json';
import SelectTestTopic from '../../components/SelectTestTopic/SelectTestTopic';
import { useState } from 'react'
import { postRequest as fetchData } from '../../modules/requests';
import QuestionBox from '../../components/QuestionBox';

const TestPage = (props) => {
    const { t } = useTranslation('translations');
    const [questions, setQuestions] = useState()
    const [answers, setAnswers] = useState()
    const [description, setDescription] = useState()
    const [topicID, setTopicID] = useState()
    const [subjectID, setSubjectID] = useState()
    const [testID, setTestID] = useState()
    const [maxTime, setMaxTime] = useState(60)

    const handleLoadQuestionAnswer = (topID, subID) => {
        setTopicID(topID);
        setSubjectID(subID);

        const questionAddress = `${CONSTANTS.AUTH_API_ADDRESS}/question/search`
        const questionBody = JSON.stringify({
            "queries": [
                {
                    "field": "topicID",
                    "query": topID
                }
            ]
        })

        fetchData(questionAddress, questionBody).then(data => {
            setQuestions(data)
        })
    }
    
    const handleDelete = (deleteID) => {
        setQuestions(questions.filter(item => item.id !== deleteID))
    }

    const handleReroll = (rerollID) => {
        handleDelete(rerollID)
        
        // need API to get question, different from the ones existing in questions

    }

    const handleCreateTest = () => {
        const testAddress = `${CONSTANTS.AUTH_API_ADDRESS}/test`
        const testBody = JSON.stringify({
            "description": description,
            "topicID": topicID,
            "subjectID": subjectID,
            "max_time_allowed": maxTime
        })

        fetchData(testAddress, testBody).then((data) => {
            setTestID(data.id)
        })
    }

    const handleSubmitTest = () => {
        handleCreateTest()

        for (let questionRow in questions) {
            for (let answerRow in questionRow.answerList) {
                const qtaAddress = `${CONSTANTS.AUTH_API_ADDRESS}/qta`
                const qtaBody = JSON.stringify({
                    "questionID": questionRow.id,
                    "testID": testID,
                    "answerID": answerRow.id
                })

                fetchData(qtaAddress, qtaBody)
            }
        }
    }

    const question_arr = []
    for (let question in questions) {
        const answerAddress = `${CONSTANTS.AUTH_API_ADDRESS}/answer/${question.id}/all`
        const answerBody = JSON.stringify({})

        fetchData(answerAddress, answerBody).then(data => {
            setAnswers(data)
        })

        question['answerList'] = [];
        question.answerList = answers

        let row = 
        <QuestionBox 
            questionData={question}
            answerData={answers}
            handleDelete={handleDelete}
            handleReroll={handleReroll}
            // TODO add handle answer reroll & delete functions
        />

        question_arr.push(row)
    }

    return (
        <div>
            <div className={styles.page}>
                <h1>{t('Test_Page.title')}</h1>
                <SelectTestTopic handleLoadQuestionAnswer={handleLoadQuestionAnswer}/>
            </div>
            {questions !== [] && 
            <form onSubmit={handleSubmitTest}>
                <input 
                    type='text' 
                    placeholder='test description' 
                    value={description}
                    onChange={e => setDescription(e.target.value).trim()}
                    >
                </input>
                <input 
                    type='text' 
                    placeholder='time to complete the test' 
                    value={maxTime}
                    onChange={e => setMaxTime(e.target.value).trim()}
                    >
                </input>
                {question_arr}
                <input type='submit' value='Create Test'/>
            </form>}  
        </div>
    )
}
export default TestPage;