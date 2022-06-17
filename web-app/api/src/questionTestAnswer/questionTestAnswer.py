from flask import Blueprint, request
from util import generateResponse, generateError, getDecodedJWTTokens, paginateArray, validateQueryJson, searchByRoute, isUserAdmin
from models.models import QuestionTestAnswer, Question, Test, Answer, Subject, Topic, db

question_test_answer_blueprint = Blueprint('qta', __name__)

@question_test_answer_blueprint.route('/', methods=['POST'])
def createQuestionTestAnswer():
    if (validateQTAJson(request.json)):
        test = Test.query.filter_by(id=request.json['testID']).first()
        question = Question.query.filter_by(id=request.json['questionID']).first()
        answer = Answer.query.filter_by(id=request.json['answerID']).first()

        check_exists = QuestionTestAnswer.query.filter_by(testID=test.id, questionID=question.id, answerID=answer.id).first()

        if check_exists:
            return generateError(409, "Conflict")

        if not test:
            return generateError(404, "Test not found")

        if not question:
            return generateError(404, "Question not found")

        if not answer:
            return generateError(404, "Answer not found")

        if answer.questionID != question.id:
<<<<<<< HEAD
            return generateError(409, "Answer does not belong to question")
=======
            return generateError(400, "Answer does not belong to question")
>>>>>>> error codes and models adjustment
        
        qta = QuestionTestAnswer(
            questionID=question.id,
            testID=test.id,
            answerID=answer.id
        )

        db.session.add(qta)
        db.session.commit()

        data = {
            "status": "OK"
        }
        return generateResponse(data)
    else:
        return generateError(400, "Bad request body")


# function for ONLY managing existing question-test-answer combinations
@question_test_answer_blueprint.route('/<q_id>/<t_id>/<a_id>', methods=['GET', 'DELETE'])
def manageQuestionTestAnswer(q_id, t_id, a_id):
    result = QuestionTestAnswer.query.filter_by(testID=t_id, questionID=q_id, answerID=a_id).first() # nopep8

    if not result:
        return generateError(404, "QTA not found")

    if (request.method == 'GET'):
        question = Question.query.filter_by(id=q_id).first()
        subject = Subject.query.filter_by(id=question.subjectID).first()
        topic = Topic.query.filter_by(id=question.topicID).first()
        answer = Answer.query.filter_by(id=a_id).first()

        data = {
            "testID": result.testID,
            "question": {
                "id": result.questionID,
                "difficulty": question.difficulty,
                "subject": subject.name,
                "topic": topic.name,
                "text": question.text,
                "description": question.description
            },
            "answer": {
                "id": answer.id,
                "text": answer.text,
                "explanation": answer.explanation
            }
        }
        return generateResponse(data)

    else:
        # only delete is allowed as this is a generated instance on a test
        try:
            id_token, perm_token = getDecodedJWTTokens(request)
        except Exception as error:
            return generateError(error.args[0], error.args[1])

        if not isUserAdmin(perm_token):
<<<<<<< HEAD
<<<<<<< HEAD
            return generateError(403, "Insufficient permissions")
=======
            return generateError(401, "Not Authorized!")
>>>>>>> error codes and models adjustment
=======
            return generateError(403, "Insufficient permissions")
>>>>>>> error code change

        if (request.method == 'DELETE'):
            db.session.delete(result)
            db.session.commit()
            return generateResponse("QTA deleted")

def validateQTAJson(json):
    try:
        testID = json['testID']
        questionID = json['questionID']
        answerID = json['answerID']

        return True
    except:
        return False
