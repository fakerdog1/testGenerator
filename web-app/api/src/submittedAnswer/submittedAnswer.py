from flask import Blueprint, request
from datetime import datetime
from util import generateResponse, generateError, getDecodedJWTTokens, paginateArray, validateQueryJson, searchByRoute, isUserAdmin
from models.models import Profile, SubmittedAnswer, TestInstance, Answer, QuestionTestAnswer, Question, db

submitted_answer_blueprint = Blueprint('submitted_answer', __name__)

@submitted_answer_blueprint.route('/', methods=['POST'])
def createSubmittedAnswer():
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])

    profile = Profile.query.filter_by(id=id_token['userID']).first()

    if not profile:
        return generateError(401, "Unauthorized")
        
<<<<<<< HEAD
<<<<<<< HEAD
    if (validateSubmittedAnswerJson(request.json)):
        result = SubmittedAnswer.query.filter_by(testInstanceID=request.json['testInstanceID'], answerID=request.json['answerID'], questionID=request.json['questionID']).first()
<<<<<<< HEAD
=======
    if (validateSubmittedAnswerJson(request.json, False)):
=======
    if (validateSubmittedAnswerJson(request.json)):
>>>>>>> one fucntion to create and update submittedAnswer
        test_instance = TestInstance.query.filter_by(id=request.json['testInstanceID']).first()
        answer = Answer.query.filter_by(id=request.json['answerID']).first()
        question = Question.query.filter_by(id=request.json['questionID']).first()
        qta = QuestionTestAnswer.query.filter_by(testID=test_instance.testID, answerID=answer.id).first()

        if not test_instance:
            return generateError(404, "Test not found")

        if test_instance.time_finished != None:
            return generateError(400, "Test Instance already ended. Cannot be changed.")
>>>>>>> error codes and models adjustment
        
        if not result:
            submitted_answer = SubmittedAnswer(
                testInstanceID=request.json['testInstanceID'],
                answerID=request.json['answerID'],
                questionID = request.json['questionID']
            )

            db.session.add(submitted_answer)
            db.session.commit()

<<<<<<< HEAD
<<<<<<< HEAD
            return generateResponse(SubmittedAnswer.jsonify(submitted_answer))
=======
        if not qta:
            return generateError(400, "Submitted answer does not belong to test")
        
        submitted_answer = SubmittedAnswer(
            testInstanceID=test_instance.id,
            answerID=answer.id
        )
>>>>>>> error codes and models adjustment

        # serves as EDIT route if an instance of submittedAnswer for this test, question, and answer already exists (check for answer too because of multiple choice questions)
        else: 
            answer = Answer.query.filter_by(id=request.json['answerID']).first()
            new_answer = Answer.query.filter_by(id=request.json['newAnswerID']).first()

<<<<<<< HEAD
            if not new_answer:
                    return generateError(404, "Answer not found")
=======
        return generateResponse(SubmittedAnswer.jsonify(submitted_answer))
=======
        if not question:
            return generateError(404, "Question not found")

        if not qta:
            return generateError(400, "Submitted answer does not belong to test")
        
        result = SubmittedAnswer.query.filter_by(testInstanceID=test_instance.id, answerID=answer.id, questionID=question.id).first()
=======
>>>>>>> submittedAnswers check question, testInstance, answer, and QTA existence in validateJSON
        
        if not result:
            submitted_answer = SubmittedAnswer(
                testInstanceID=request.json['testInstanceID'],
                answerID=request.json['answerID'],
                questionID = request.json['questionID']
            )

            db.session.add(submitted_answer)
            db.session.commit()

            return generateResponse(SubmittedAnswer.jsonify(submitted_answer))

        # serves as EDIT route if an instance of submittedAnswer for this test, question, and answer already exists (check for answer too because of multiple choice questions)
        else: 
            answer = Answer.query.filter_by(id=request.json['answerID']).first()
            new_answer = Answer.query.filter_by(id=request.json['newAnswerID']).first()

            if not new_answer:
                    return generateError(404, "Answer not found")

            if answer.questionID != new_answer.questionID:
                return generateError(409, "Answer does not belong to question") 

            check = SubmittedAnswer.query.filter_by(testInstanceID=request.json['testInstanceID'], answerID=new_answer.id, questionID=request.json['questionID']).first()

            if check:
                return generateError(409, "Conflict")

            result.answerID = new_answer.id

            db.session.add(result)
            db.session.commit()

            return generateResponse(SubmittedAnswer.jsonify(result))
>>>>>>> one fucntion to create and update submittedAnswer
    else:
        return generateError(400, "Bad request body")


# function for ONLY managing existing question-test-answer combinations
@submitted_answer_blueprint.route('/<t_id>/<a_id>/<q_id>', methods=['GET'])
def manageSubmittedAnswer(t_id, a_id, q_id):
    result = SubmittedAnswer.query.filter_by(testInstanceID=t_id, answerID=a_id, questionID=q_id).first() # nopep8
    
    if not result:
        return generateError(404, "SubmittedAnswer not found")
    
    question_info = Question.query.filter_by(id=result.questionID).first()
    
<<<<<<< HEAD
    if (request.method == 'GET'):
<<<<<<< HEAD
        return generateResponse(SubmittedAnswer.jsonify(result))
>>>>>>> error codes and models adjustment

            if answer.questionID != new_answer.questionID:
                return generateError(409, "Answer does not belong to question") 

<<<<<<< HEAD
            check = SubmittedAnswer.query.filter_by(testInstanceID=request.json['testInstanceID'], answerID=new_answer.id, questionID=request.json['questionID']).first()
=======
        data = {
            "submitted_answer": SubmittedAnswer.jsonify(result),
            "question_info": Question.jsonify(question_info)
        }
        return generateResponse(data)
>>>>>>> get returns question info + submitted answer

<<<<<<< HEAD
            if check:
                return generateError(409, "Conflict")
=======
            if test_instance.time_finished != None:
                return generateError(400, "Test Instance already ended. Cannot be changed.")
            
            if validateSubmittedAnswerJson(request.json, True):
                question_compat = Answer.query.filter_by(id=result.answerID).first()
                answer = Answer.query.filter_by(id=request.json['answerID']).first()
>>>>>>> error codes and models adjustment

<<<<<<< HEAD
            result.answerID = new_answer.id

<<<<<<< HEAD
            db.session.add(result)
            db.session.commit()
=======
                if question_compat.questionID != answer.questionID:
                    return generateError(400, "Answer does not belong to question")
                
                result.answerID = request.json['answerID']
>>>>>>> error codes and models adjustment
=======
    data = {
        "submitted_answer": SubmittedAnswer.jsonify(result),
        "question_info": Question.jsonify(question_info)
    }
    return generateResponse(data)
>>>>>>> submittedAnswers check question, testInstance, answer, and QTA existence in validateJSON

            return generateResponse(SubmittedAnswer.jsonify(result))
    else:
        return generateError(400, "Bad request body")

<<<<<<< HEAD

# function for ONLY managing existing question-test-answer combinations
@submitted_answer_blueprint.route('/<t_id>/<a_id>/<q_id>', methods=['GET'])
def manageSubmittedAnswer(t_id, a_id, q_id):
    result = SubmittedAnswer.query.filter_by(testInstanceID=t_id, answerID=a_id, questionID=q_id).first() # nopep8
    
    if not result:
        return generateError(404, "SubmittedAnswer not found")
    
    question_info = Question.query.filter_by(id=result.questionID).first()
    
    data = {
        "submitted_answer": SubmittedAnswer.jsonify(result),
        "question_info": Question.jsonify(question_info)
    }
    return generateResponse(data)
=======
=======
>>>>>>> one fucntion to create and update submittedAnswer
        if (request.method == 'DELETE'):
            if not isUserAdmin(perm_token):
                return generateError(401, "Not Authorized!")

            db.session.delete(result)
            db.session.commit()
            return generateResponse("SubmittedAnswer deleted")
>>>>>>> error codes and models adjustment

=======
>>>>>>> left only GET functionality on manageSubmitAnswer

def validateSubmittedAnswerJson(json):
    try:
        answerID = json['answerID']
        testInstanceID = json['testInstanceID']
        questionID = json['questionID']
<<<<<<< HEAD

        test_instance = TestInstance.query.filter_by(id=json['testInstanceID']).first()
        if not test_instance:
            return False

        answer = Answer.query.filter_by(id=json['answerID']).first()
        if not answer:
            return False
        
        question = Question.query.filter_by(id=json['questionID']).first()
        if not question:
            return False
        
        qta = QuestionTestAnswer.query.filter_by(testID=test_instance.testID, answerID=answer.id, questionID=question.id).first()
        if not qta:
            return False

        edit = SubmittedAnswer.query.filter_by(testInstanceID=test_instance.id, answerID=answer.id, questionID=question.id).first() # nopep8
=======

<<<<<<< HEAD
        edit = SubmittedAnswer.query.filter_by(testInstanceID=json['testInstanceID'], answerID=json['answerID'], questionID=json['questionID']).first() # nopep8
>>>>>>> one fucntion to create and update submittedAnswer
=======
        test_instance = TestInstance.query.filter_by(id=json['testInstanceID']).first()
        if not test_instance:
            return False

        answer = Answer.query.filter_by(id=json['answerID']).first()
        if not answer:
            return False
        
        question = Question.query.filter_by(id=json['questionID']).first()
        if not question:
            return False
        
        qta = QuestionTestAnswer.query.filter_by(testID=test_instance.testID, answerID=answer.id, questionID=question.id).first()
        if not qta:
            return False

        edit = SubmittedAnswer.query.filter_by(testInstanceID=test_instance.id, answerID=answer.id, questionID=question.id).first() # nopep8
>>>>>>> submittedAnswers check question, testInstance, answer, and QTA existence in validateJSON
        if edit:
            newAnswerID = json['newAnswerID']

        return True
    except:
        return False