import CONSTANTS from '../../modules/CONSTANTS.json';
import { useState , useEffect } from 'react';
import { postRequest as fetchData } from '../../modules/requests'
import { Dropdown , Col , Row, Button } from 'react-bootstrap'


const SelectTestTopic = (props) => {
    const [gradeData, setGradeData] = useState();
    const [selectedGrade, setSelectedGrade] = useState();
    const [subjectData, setSubjectData] = useState();
    const [selectedSubject, setSelectedSubject] = useState();
    const [topicData, setTopicData] = useState();
    const [selectedTopic, setSelectedTopic] = useState();

    useEffect(() => {
        const gradeAddress = `${CONSTANTS.AUTH_API_ADDRESS}/grade/all`
        const gradeBody = JSON.stringify({
            "page": 0,
            "pageSize": 50
        })
        fetchData(gradeAddress, gradeBody).then(data => {
            console.log(data);
            setGradeData(data)
        })
        const subjectAddress = `${CONSTANTS.AUTH_API_ADDRESS}/subject/all`
        const subjectBody = JSON.stringify({
            "page": 0,
            "pageSize": 50
        })
        fetchData(subjectAddress, subjectBody).then(data => {
            console.log(data);
            setSubjectData(data)
        })
        const topicAddress = `${CONSTANTS.AUTH_API_ADDRESS}/subject/all`
        const topicBody = JSON.stringify({
            "page": 0,
            "pageSize": 50
        })
        fetchData(topicAddress, topicBody).then(data => {
            console.log(data);
            setTopicData(data)
        })
    }, [])

    const handleSelectGrade = (e) => {
        e.preventDefault();

        setSelectedGrade(e.target.value)

        const searchSubjectAddress = `${CONSTANTS.AUTH_API_ADDRESS}/subject/search`
        const subjectBody = {
            "page": 0,
            "pageSize": 50,
            "queries": [
                {
                    "field": "grade",
                    "query": selectedGrade
                }
            ]
        }
        fetchData(searchSubjectAddress, subjectBody).then(data => {
            console.log(data);
            setSubjectData(data)
        })

        // update API for searchTopic to be able to search by subjectID => loop to fetchData(topic) by subjectData ids
    }

    const handleSelectSubject = (e) => {
        e.preventDefault();

        setSelectedSubject(e.target.value)
        const searchTopicAddress = `${CONSTANTS.AUTH_API_ADDRESS}/topic/search`
        const topicBody = {
            "page": 0,
            "pageSize": 50,
            "queries": [
                {
                    "field": "subject",
                    "query": selectedSubject
                }
            ]
        }

        if (selectedGrade === null ) {
            for (let grade in gradeData) {
                // loop like this because grade API doesn't permit grade duplication
                if (grade.id === selectedSubject.gradeID) {
                    setSelectedGrade(grade)
                    break
                }
            }
        }
        
        fetchData(searchTopicAddress, topicBody).then(data => {
            console.log(data);
            setTopicData(data)
        })

        // update API for searchTopic to be able to search by subjectID => loop to fetchData(topic) by subjectData ids
    }

    const handleSelectTopic = (e) => {
        e.preventDefault();

        setSelectedTopic(e.target.value)

        if (selectedSubject === null) {
            for (let subject in subjectData) {
                if (subject.id === selectedTopic.subjectID) {
                    setSelectedSubject(subject)
                    setSelectedGrade(selectedSubject.gradeID)
                    break
                }
            }
        }
    }

    const grade_arr = []
    for (let grade in gradeData) {
        let row = <Dropdown.Item value={grade} onClick={event => handleSelectGrade(event).trim()}>
            {grade.name}
        </Dropdown.Item>

        grade_arr.push(row)
    }

    const subject_arr = []
    for (let subject in subjectData) {
        let row = <Dropdown.Item value={subject} onClick={event => handleSelectSubject(event).trim()}>
            {subject.name}
        </Dropdown.Item>

        subject_arr.push(row)
    }

    const topic_arr = []
    for (let topic in topicData) {
        let row = <Dropdown.Item value={topic} onClick={event => handleSelectTopic(event).trim()}>
            {topic.name}
        </Dropdown.Item>

        topic_arr.push(row)
    }

    return(
        <div className='mw-100'>
            <Row>
                <Col lg={4}>
                    <Dropdown>
                        <Dropdown.Toggle variant='success' id='dropdown-basic'>
                            {selectedGrade}
                        </Dropdown.Toggle>
                        <Dropdown.Menu>
                            {grade_arr}
                        </Dropdown.Menu>
                    </Dropdown>
                </Col>
                <Col lg={4}>
                    <Dropdown>
                        <Dropdown.Toggle variant='success' id='dropdown-basic'>
                            {selectedSubject}
                        </Dropdown.Toggle>
                        <Dropdown.Menu>
                            {subject_arr}
                        </Dropdown.Menu>
                    </Dropdown>
                </Col>
                <Col lg={4}>
                    <Dropdown>
                        <Dropdown.Toggle variant='success' id='dropdown-basic'>
                            {selectedTopic}
                        </Dropdown.Toggle>
                        <Dropdown.Menu>
                            {topic_arr}
                        </Dropdown.Menu>
                    </Dropdown>
                </Col>
            </Row>
            <Row>
                <Button className='w-25' onClick={props.handleLoadQuestionAnswer(selectedTopic.id, selectedSubject.id)}>
                    Generate Questions
                </Button>
            </Row>
        </div>
    )
}

export default SelectTestTopic