from flask import Blueprint, request
from util import generateResponse, generateError, getDecodedJWTTokens, paginateArray, validateQueryJson, searchByRoute
from models.models import Question, Profile, Topic, db

question_blueprint = Blueprint('question', __name__)


@question_blueprint.route('/', methods=['POST'])
def createQuestion():
    # validate JWT token and permissions token
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])
    profile = Profile.query.filter_by(jwt_id=id_token['userID']).first()

    # create new question and return its id
    if (validateQuestionJson(request.json)):
        topic = Topic.query.filter_by(id=request.json['topicID']).first()

        question = Question(
            text=request.json['text'],
            description=request.json['description'],
            difficulty=request.json['difficulty'],
            ownerID=profile.id,
            subjectID=topic.subjectID,
            topicID=topic.id
        )

        db.session.add(question)
        db.session.commit()
        return generateResponse(Question.jsonify(question))
    else:
        return generateError(400, "Bad question data")


# function for ONLY managing (RUD) existing questions
@question_blueprint.route('/<q_id>', methods=['GET', 'POST', 'DELETE'])
def manageQuestion(q_id):
    result = Question.query.filter_by(id=q_id).first()
    if not result:
        return generateError(404, "Question not found")

    if (request.method == 'GET'):
        return generateResponse(Question.jsonify(result))

    else:
        # anyone can read questions, but for editing and deleting you need to be the owner of the question
        # validate JWT token and permissions token
        try:
            id_token, perm_token = getDecodedJWTTokens(request)
        except Exception as error:
            return generateError(error.args[0], error.args[1])

        # find the owner of the token
        profile = Profile.query.filter_by(jwt_id=id_token['userID']).first()
        if not profile:
            return generateError(400, "User profile has not been created!")
        # check whether the profile of the request sender is the owner of the question
        if not (result.ownerID == profile.id):
            return generateError(403, 'Not Authorized')

        if (request.method == 'POST'):
            if (validateQuestionJson(request.json)):
                topic = Topic.query.filter_by(
                    id=request.json['topicID']).first()

                if result:
                    result.text = request.json['text'],
                    result.description = request.json['description'],
                    result.subjectID = topic.subjectID,
                    result.topicID = topic.id

                    db.session.add(result)
                    db.session.commit()
                    return generateResponse(Question.jsonify(result))
            else:
                return generateError(400, "Bad request")

        if (request.method == 'DELETE'):
            db.session.delete(result)
            db.session.commit()
            return generateResponse("Question deleted")


# function to show all own questions paginated
@question_blueprint.route('/all', methods=['POST'])
def showAllQuestions():
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

    all_questions = []
    all_questions = Question.query.filter_by(ownerID=id_token['userID']).all()

    results = []
    for question in all_questions:
        results.append({"id": question.id, "text": question.text})

    paged_results = list(paginateArray(results, pageSize))

    data = {
        "page": page,
        "pageSize": pageSize,
        "nextPage": (page < (len(paged_results) - 1)),
        "results": paged_results[page] if ((page < len(paged_results))) else []
    }

    return generateResponse(data)


# route to handle searching users
@question_blueprint.route('/search', methods=['POST'])
def search_questionss():
    # try to read optional parameters in request
    try:
        page = request.json["page"]
    except:
        page = 0
    try:
        pageSize = request.json["pageSize"]
    except:
        pageSize = 50
    # try to read mandatory paramater in request
    queries = validateQueryJson(request.json['queries'])
    data = searchByRoute(page, pageSize, queries, performQuestionQuery)

    return generateResponse(data)


# helper function to perform and format the actual queries
def performQuestionQuery(field, value):
    questions = []
    if (field == "text"):
        questions = Question.query.filter(Question.text.contains(value)).order_by(Question.id).all()  # nopep8
    if (field == "subjectID"):
        questions = Question.query.filter_by(subjectID=value).order_by(Question.id).all()  # nopep8    
    if (field == "topicID"):
        questions = Question.query.filter_by(topicID=value).order_by(Question.id).all()  # nopep8  
    if (field == "difficulty"):
        questions = Question.query.filter_by(difficulty=value).order_by(Question.id).all()  # nopep8

    results = []
    for question in questions:
        results.append({
            "id": question.id, 
            "text": question.text, 
            "difficulty": question.difficulty, 
            "subjectID": question.subjectID, 
            "topicID": question.topicID
        })

    return results


def validateQuestionJson(json):
    try:
        text = json['text']
        description = json['description']
        difficulty = json['difficulty']

        return True
    except:
        return False
