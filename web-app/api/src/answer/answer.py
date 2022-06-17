from flask import Blueprint, request
from util import generateResponse, generateError, getDecodedJWTTokens, paginateArray, validateQueryJson
from models.models import Question, Answer, Profile, db

answer_blueprint = Blueprint('answer', __name__)

@answer_blueprint.route('/', methods=['POST'])
def createAnswer():
    # validate JWT token and permissions token
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])
    profile = Profile.query.filter_by(jwt_id=id_token['userID']).first()
    question = Question.query.filter_by(id=request.json['questionID']).first()

    # create new answer and return its id
    if question.ownerID != profile.id:
        return generateError(400, "Question does not belong to you")
    
    if (validateAnswerJson(request.json)):
        answer = Answer(
            text=request.json['text'],
            explanation=request.json['explanation'],
            is_correct=request.json['is_correct'],
            questionID=question.id,
            ownerID=profile.id
        )

        db.session.add(answer)
        db.session.commit()
        return generateResponse(Answer.jsonify(answer))
    else:
        return generateError(400, "Bad Answer data")


# function for ONLY managing (RUD) existing answers
@answer_blueprint.route('/<a_id>', methods=['GET', 'POST', 'DELETE'])
def manageAnswer(a_id):
    #answer viewable from any visitor
    result = Answer.query.filter_by(id=a_id).first()
    if not result:
        return generateError(404, "Answer not found")

    if (request.method == 'GET'):  
        #validate JWT  
        try:
            id_token, perm_token = getDecodedJWTTokens(request)
        except:
            return generateResponse(Answer.jsonify(result))
        
        #is_correct visibility assigned only to question creator
        if result.ownerID != id_token['userID']:
            return generateResponse(Answer.jsonify(result))
        
        result_creator = Answer.jsonify(result)
        result_creator['is_correct'] = result.is_correct
        return generateResponse(result_creator)
    
    else:
        # anyone can read answers, but for editing and deleting you need to be the owner of the answer
        try:
            id_token, perm_token = getDecodedJWTTokens(request)
        except Exception as error:
            return generateError(error.args[0], error.args[1])
        
        # find the owner of the token
        profile = Profile.query.filter_by(jwt_id=id_token['userID']).first()
        if not profile:
            return generateError(400, "User profile has not been created!")
        
        # check whether the profile of the request sender is the owner of the answer
        if not (result.ownerID == profile.id):
            return generateError(403, 'Not Authorized')

        if (request.method == 'POST'):
            if (validateAnswerJson(request.json)):
                if result:
                    result.text = request.json['text'],
                    result.explanation = request.json['explanation'],
                    result.is_correct = request.json['is_correct']

                    db.session.add(result)
                    db.session.commit()
                    return generateResponse(Answer.jsonify(result))
            else:
                return generateError(400, "Bad request")

        if (request.method == 'DELETE'):
            db.session.delete(result)
            db.session.commit()
            return generateResponse("Answer deleted")


# function to show all own answers paginated
@answer_blueprint.route('<q_id>/all', methods=['POST'])
def showAllAnswers(q_id):
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])
    
    # try to read optional paramaters in request
    try:
        page = request.json["page"]
    except:
        page = 0
    try:
        pageSize = request.json["pageSize"]
    except:
        pageSize = 50
    
    question_all_answers = []
    question_all_answers = Answer.query.filter_by(ownerID=id_token['userID'], questionID=q_id).all() # nopep8

    results = []
    for answer in question_all_answers:
        results.append({"id": answer.id, "text": answer.text})
    
    paged_results = list(paginateArray(results, pageSize))

    data = {
        "page": page,
        "pageSize": pageSize,
        "nextPage": (page < (len(paged_results) -1)),
        "results": paged_results[page] if ((page < len(paged_results))) else []
    }

    return generateResponse(data)


def validateAnswerJson(json):
    try:
        text = json['text']
        explanation = json['explanation']
        is_correct = json['is_correct']
        questionID = json['questionID']

        return True
    except:
        return False
