import { Button } from 'react-bootstrap'


const QuestionBox = (props) => {
    const answer_arr = []
        
    for (let ans in props.answerData) {
        let row = 
        <div>
            <h4>{ans.text}</h4>
            <p>{ans.explanation}</p>
            <p>{ans.is_correct}</p>
        </div>

        answer_arr.push(row)
    }
    return(
        <div>
            <h1>{props.questionData.text}</h1>
            <p>{props.questionData.description}</p>
            <h3>{props.questionData.difficulty}</h3>
            <br></br>
            {answer_arr}

            <Button onClick={props.handleReroll(props.questionData.id)}>
                Reroll
            </Button>
            <Button onClick={props.handleDelete(props.questionData.id)}>
                Delete
            </Button>
        </div>
    )
}

export default QuestionBox