from flask import Blueprint, request
from util import generateResponse, generateError, getDecodedJWTTokens, isUserAdmin, validateQueryJson, searchByRoute, paginateArray
from models.models import Test, Profile, Subject, Topic, QuestionTestAnswer, CurrentTestTemplate, Question, db
from datetime import datetime, timedelta

test_blueprint = Blueprint('test', __name__)

@test_blueprint.route('/', methods=['POST'])
def createTest():
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])

    profile = Profile.query.filter_by(jwt_id=id_token['userID']).first()
    # create new Test and return its id
    if not profile.id:
        return generateError(401, "Unauthorized")

    if (validateTestJson(request.json, False)):  
        if request.json['subjectID'] != None:
            subject = Subject.query.filter_by(id=request.json['subjectID']).first()
            if not subject:
                return generateError(404, "Subject not found")

        if request.json['topicID'] != None:
            topic = Topic.query.filter_by(id=request.json['topicID']).first()
            if not topic:
                return generateError(404, "Topic not found")

            if topic.subjectID != subject.id:
                return generateError(409, "Choose topic that belongs to chosen subject")

        test = Test(
            description=request.json['description'],
            max_time_allowed=request.json['max_time_allowed'],
            ownerID=profile.id,
            subjectID=request.json['subjectID'],
            topicID=request.json['topicID']
        )

        db.session.add(test)
        db.session.commit()

        current = CurrentTestTemplate(
            is_current=True,
            ownerID=profile.id,
            testID=test.id,
            previousTestID=None
        )

        db.session.add(current)
        db.session.commit()
        return generateResponse(Test.jsonify(test))
    else:
        return generateError(400, "Bad test data")


# function for ONLY managing (RUD) existing Tests
@test_blueprint.route('/<s_id>', methods=['GET', 'POST', 'DELETE'])
def manageTest(s_id):
    result = Test.query.filter_by(id=s_id).first()

    if not result:
        return generateError(404, "Test not found")

    if (request.method == 'GET'):
        return generateResponse(Test.jsonify(result))

    else:
        # anyone can read Tests, but for editing and deleting you need to be the Owner
        try:
            id_token, perm_token = getDecodedJWTTokens(request)
        except Exception as error:
            return generateError(error.args[0], error.args[1])

        # test can only be edited/deleted by owner or admin
        if (id_token['userID'] != result.ownerID) or not isUserAdmin(perm_token):
            return generateResponse(403, "Forbidden")
        
        if (request.method == 'POST'):
            if (validateTestJson(request.json, True)):
                qta_check = QuestionTestAnswer.query.filter(QuestionTestAnswer.testID==s_id, QuestionTestAnswer.questionID!=request.json['qReplaceID']).all()
                question_new = Question.query.filter_by(id=request.json['qNewID']).first()

                if not qta_check:
                    return generateError(404, 'Test not populated')

                if not question_new:
                    return generateError(404, 'Edited question does not exist!')

                if request.json['subjectID'] != None:
                    s_check = Subject.query.filter_by(id=request.json['subjectID']).first()
                    if not s_check:
                        return generateError(404, "Subject not found")
                    
                    subject = request.json['subjectID']
                else:
                    subject = result.subjectID

                if request.json['topicID'] != None:
                    t_check = Topic.query.filter_by(id=request.json['topicID']).first()
                    if not t_check:
                        return generateError(404, "Topic not found")

                    if t_check.subjectID != subject.id:
                        return generateError(409, "Choose topic that belongs to chosen subject")
                    
                    topic = request.json['topic']
                else:
                    topic = result.topicID
                
                if request.json['description'] != None:
                    description = request.json['description']
                else:
                    description = result.description

                if request.json['timedelta'] != None:
                    max_time_allowed = request.json['max_time_allowed']
                else:
                    max_time_allowed = result.max_time_allowed

                test = Test(
                    description=description,
                    max_time_allowed=max_time_allowed,
                    ownerID=result.ownerID,
                    subjectID=subject,
                    topicID=topic
                )

                db.session.add(test)
                db.session.commit()

                ctt = CurrentTestTemplate(
                    is_current=True,
                    ownerID=result.ownerID,
                    testID=test.id,
                    previousTestID=s_id
                )

                db.session.add(ctt)
                db.session.commit()

                ptt = CurrentTestTemplate.query.filter_by(testID=s_id).first()

                if not ptt:
                    return generateError(404, "Test history not found")
                
                ptt.is_current = False

                db.session.add(ptt)
                db.session.commit()

                for answer in request.json['aNewIDs']:
                    qta = QuestionTestAnswer(
                        questionID=request.json['qNewID'],
                        testID=test.id,
                        answerID=answer
                    )
                    
                    db.session.add(qta)
                    db.session.commit()

                for q in qta_check:
                    qta2 = QuestionTestAnswer(
                        questionID=q.questionID,
                        testID=test.id,
                        answerID=q.answerID
                    )

                    db.session.add(qta2)
                    db.session.commit()

                return generateResponse(Test.jsonify(test))
            else:
                return generateError(400, "Bad request")

        if (request.method == 'DELETE'):
            db.session.delete(result)
            db.session.commit()
            return generateResponse("Test deleted")


@test_blueprint.route('/all', methods=['POST'])
def showAllTests():
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

    all_tests = []
    all_tests = Test.query.filter_by(ownerID=id_token['userID']).all()

    results = []
    for test in all_tests:
        results.append(
            {
                "id": test.id, 
                "description": test.description, 
                "subjectID": test.subjectID, 
                "topicID": test.topicID
            }
        )

    paged_results = list(paginateArray(results, pageSize))

    data = {
        "page": page,
        "pageSize": pageSize,
        "nextPage": (page < (len(paged_results) - 1)),
        "results": paged_results[page] if ((page < len(paged_results))) else []
    }

    return generateResponse(data)


def validateTestJson(json, edit):
    try:
        description = json['description']
        subjectID = json['subjectID']
        topicID = json['topicID']

        if edit == True:
            qReplaceID = json['qReplaceID']
            qNewID = json['qNewID']
            aNewIDs = json['aNewIDs']
        return True
    except:
        return False