from flask import Blueprint, request
<<<<<<< HEAD
<<<<<<< HEAD
from datetime import datetime, timedelta
from util import generateResponse, generateError, getDecodedJWTTokens, paginateArray, validateQueryJson, searchByRoute, isUserAdmin
from models.models import Profile, TestInstance, Test, QuestionTestAnswer, SubmittedAnswer, Answer, db
=======
from datetime import datetime
=======
from datetime import datetime, timedelta
>>>>>>> timedelta model changed - store as integer, convert to interval when needed
from util import generateResponse, generateError, getDecodedJWTTokens, paginateArray, validateQueryJson, searchByRoute, isUserAdmin
<<<<<<< HEAD
from models.models import Profile, TestInstance, Test, db
>>>>>>> testInstance CRUD added
=======
from models.models import Profile, TestInstance, Test, QuestionTestAnswer, SubmittedAnswer, Answer, db
>>>>>>> check for previous currentTestTemplate existence in validateJson

test_instance_blueprint = Blueprint('test_instance', __name__)

@test_instance_blueprint.route('/', methods=['POST'])
def createTestInstance():
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])

    profile = Profile.query.filter_by(id=id_token['userID']).first()

    if not profile:
<<<<<<< HEAD
<<<<<<< HEAD
        return generateError(401, "Unauthorized")
=======
        return generateError(404, "User profile not found")
>>>>>>> testInstance CRUD added
=======
        return generateError(401, "Unauthorized")
>>>>>>> error codes and models adjustment
        
    if (validateTestInstanceJson(request.json)):
        test = Test.query.filter_by(id=request.json['testID']).first()

        if not test:
            return generateError(404, "Test not found")
        
        test_instance = TestInstance(
            takerID=profile.id,
            testID=test.id,
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            time_limit=timedelta(seconds=test.max_time_allowed)
=======
            quarter_hrs=request.json['quarter_hrs']
>>>>>>> testInstance CRUD added
=======
            time_started=datetime.now(),
            deadline=datetime.now() + test.timedelta
>>>>>>> timedelta moved from testInstance to testTemplate
=======
            time_limit=test.max_time_allowed
>>>>>>> testTemplate: rename timedelta; testInstance: model change for deadline, condition for GET DELETE access moved in funct
=======
            time_limit=timedelta(seconds=test.max_time_allowed)
>>>>>>> timedelta model changed - store as integer, convert to interval when needed
        )

        db.session.add(test_instance)
        db.session.commit()

        return generateResponse(TestInstance.jsonify(test_instance))
    else:
        return generateError(400, "Bad request body")


# function for ONLY managing existing question-test-answer combinations
<<<<<<< HEAD
<<<<<<< HEAD
@test_instance_blueprint.route('/<ti_id>', methods=['GET', 'DELETE'])
=======
@test_instance_blueprint.route('/<ti_id>', methods=['GET', 'POST', 'DELETE'])
>>>>>>> testInstance CRUD added
=======
@test_instance_blueprint.route('/<ti_id>', methods=['GET', 'DELETE'])
>>>>>>> split POST into a different function submitTestInstance
def manageTestInstance(ti_id):
    result = TestInstance.query.filter_by(id=ti_id).first() # nopep8
    
    if not result:
<<<<<<< HEAD
<<<<<<< HEAD
        return generateError(404, "TestInstance not found")
    
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])
    
    if (result.takerID == id_token['userID']) or isUserAdmin(perm_token):
        if (request.method == 'GET'):
            return generateResponse(TestInstance.jsonify(result)) 

        if (request.method == 'DELETE'):

            db.session.delete(result)
            db.session.commit()
            return generateResponse("TestInstance deleted")
    else:
        return generateError(403, "Not Authorized!")


@test_instance_blueprint.route('/submit/<ti_id>', methods=['POST'])
def submitTestInstance(ti_id):
    result = TestInstance.query.filter_by(id=ti_id).first() # nopep8
    
    if not result:
        return generateError(404, "TestInstance not found")

    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])
    
    if result.takerID != id_token['userID']:
        return generateError(403, "Forbidden")
    
    if result.time_finished != None:
            return generateError(409, "Test already submitted")
    
    if (request.method == 'POST'):
        result.time_finished = datetime.now()

        db.session.add(result)
        db.session.commit()
        return generateResponse(TestInstance.jsonify(result))

    
@test_instance_blueprint.route('/submitted', methods=['POST'])
def showSaved():
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])

    try:
        page = request.json["page"]
    except:
        page = 0
    try:
        pageSize = request.json["pageSize"]
    except:
        pageSize = 50
    try:
        isFinished = request.json["isFinished"]
    except:
        isFinished = None

    if isFinished:
        test_instance = TestInstance.query.filter(TestInstance.id==request.json['testInstanceID'], TestInstance.time_finished!=None).first()

        if test_instance == None:
            data = {
                "page": page,
                "pageSize": pageSize,
                "nextPage": False,
                "results": []
            }
            return generateResponse(data)
    else:
        test_instance = TestInstance.query.filter_by(id=request.json['testInstanceID']).first()
    
    if test_instance.takerID != id_token['userID']:
        return generateError(403, "Forbidden")
    
    qta_pull = QuestionTestAnswer.query.filter_by(testID=test_instance.testID).all()
    submitted_answers = SubmittedAnswer.query.filter_by(testInstanceID=test_instance.id).all()
    submitted_answers_arr = []
    for a in submitted_answers:
        push_answer = {"answerID": a.answerID, "questionID": a.questionID, "testInstanceID": a.testInstanceID}
        submitted_answers_arr.append(push_answer)

    results = []
    for qta in qta_pull:
        answer = Answer.query.filter_by(id=qta.answerID).first()
        if any(answer_obj['answerID'] == answer.id for answer_obj in submitted_answers_arr):
            submitted = True
        else:
            submitted = False
        
        if not any(d['questionID'] == qta.questionID for d in results):
            question_dict = {
                "questionID": qta.questionID, 
                "answers": [
                    {
                        "answerID": answer.id, 
                        "wasSelected": submitted, 
                        "isCorrect":answer.is_correct
                    }
                ]
            }
            results.append(question_dict)
        else:
            for d in results:
                if d['questionID'] == qta.questionID:
                    d['answers'].append(
                        {
                            "answerID": answer.id, 
                            "wasSelected": submitted, 
                            "isCorrect":answer.is_correct
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



@test_instance_blueprint.route('/all', methods=['POST'])
def showAllTests():
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])

    try:
        page = request.json["page"]
    except:
        page = 0
    try:
        pageSize = request.json["pageSize"]
    except:
        pageSize = 50
    try:
        testID = request.json["testID"]
    except:
        testID = None

    all_tests = []
    if testID == None:
        all_tests = TestInstance.query.filter_by(takerID=id_token['userID']).all()
    else:
        all_tests = TestInstance.query.filter_by(takerID=id_token['userID'], testID=testID).all()

    results = []
    for test in all_tests:
        results.append(
            {
                "id": test.id, 
                "takerID": test.takerID, 
                "testID": test.testID, 
                "time_started": test.time_started,
                "deadline": test.deadline,
                "time_finished": test.time_finished
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

=======
        return generateError(404, "Instance not found")
=======
        return generateError(404, "TestInstance not found")
>>>>>>> error codes and models adjustment
    
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])
    
    if (result.takerID == id_token['userID']) or isUserAdmin(perm_token):
        if (request.method == 'GET'):
            return generateResponse(TestInstance.jsonify(result)) 

        if (request.method == 'DELETE'):

<<<<<<< HEAD
    if (request.method == 'DELETE'):
        if (result.takerID != id_token['userID']) or not isUserAdmin(perm_token):
            return generateError(401, "Not Authorized!")

<<<<<<< HEAD
            db.session.delete(result)
            db.session.commit()
<<<<<<< HEAD
            return generateResponse("Question deleted")
>>>>>>> testInstance CRUD added
=======
            return generateResponse("TestInstance deleted")
>>>>>>> error codes and models adjustment
=======
        db.session.delete(result)
        db.session.commit()
        return generateResponse("TestInstance deleted")
>>>>>>> testInstance owner check for GET and POST
=======
            db.session.delete(result)
            db.session.commit()
            return generateResponse("TestInstance deleted")
    else:
        return generateError(403, "Not Authorized!")
>>>>>>> testTemplate: rename timedelta; testInstance: model change for deadline, condition for GET DELETE access moved in funct


@test_instance_blueprint.route('/submit/<ti_id>', methods=['POST'])
def submitTestInstance(ti_id):
    result = TestInstance.query.filter_by(id=ti_id).first() # nopep8
    
    if not result:
        return generateError(404, "TestInstance not found")

    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])
    
    if result.takerID != id_token['userID']:
        return generateError(403, "Forbidden")
    
    if result.time_finished != None:
            return generateError(409, "Test already submitted")
    
    if (request.method == 'POST'):
        result.time_finished = datetime.now()

        db.session.add(result)
        db.session.commit()
        return generateResponse(TestInstance.jsonify(result))

    
@test_instance_blueprint.route('/submitted', methods=['POST'])
def showSaved():
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])

    try:
        page = request.json["page"]
    except:
        page = 0
    try:
        pageSize = request.json["pageSize"]
    except:
        pageSize = 50
    try:
        isFinished = request.json["isFinished"]
    except:
        isFinished = None

    if isFinished:
        test_instance = TestInstance.query.filter(TestInstance.id==request.json['testInstanceID'], TestInstance.time_finished!=None).first()

        if test_instance == None:
            data = {
                "page": page,
                "pageSize": pageSize,
                "nextPage": False,
                "results": []
            }
            return generateResponse(data)
    else:
        test_instance = TestInstance.query.filter_by(id=request.json['testInstanceID']).first()
    
    if test_instance.takerID != id_token['userID']:
        return generateError(403, "Forbidden")
    
    qta_pull = QuestionTestAnswer.query.filter_by(testID=test_instance.testID).all()
    submitted_answers = SubmittedAnswer.query.filter_by(testInstanceID=test_instance.id).all()
    submitted_answers_arr = []
    for a in submitted_answers:
        push_answer = {"answerID": a.answerID, "questionID": a.questionID, "testInstanceID": a.testInstanceID}
        submitted_answers_arr.append(push_answer)

    results = []
    for qta in qta_pull:
        answer = Answer.query.filter_by(id=qta.answerID).first()
        if any(answer_obj['answerID'] == answer.id for answer_obj in submitted_answers_arr):
            submitted = True
        else:
            submitted = False
        
        if not any(d['questionID'] == qta.questionID for d in results):
            question_dict = {
                "questionID": qta.questionID, 
                "answers": [
                    {
                        "answerID": answer.id, 
                        "wasSelected": submitted, 
                        "isCorrect":answer.is_correct
                    }
                ]
            }
            results.append(question_dict)
        else:
            for d in results:
                if d['questionID'] == qta.questionID:
                    d['answers'].append(
                        {
                            "answerID": answer.id, 
                            "wasSelected": submitted, 
                            "isCorrect":answer.is_correct
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



@test_instance_blueprint.route('/all', methods=['POST'])
def showAllTests():
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])

    try:
        page = request.json["page"]
    except:
        page = 0
    try:
        pageSize = request.json["pageSize"]
    except:
        pageSize = 50
    try:
        testID = request.json["testID"]
    except:
        testID = None

    all_tests = []
    if testID == None:
        all_tests = TestInstance.query.filter_by(takerID=id_token['userID']).all()
    else:
        all_tests = TestInstance.query.filter_by(takerID=id_token['userID'], testID=testID).all()

    results = []
    for test in all_tests:
        results.append(
            {
                "id": test.id, 
                "takerID": test.takerID, 
                "testID": test.testID, 
                "time_started": test.time_started,
                "deadline": test.deadline,
                "time_finished": test.time_finished
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


def validateTestInstanceJson(json):
    try:
        testID = json['testID']
<<<<<<< HEAD
<<<<<<< HEAD
=======
        quarter_hrs = json['quarter_hrs']
>>>>>>> testInstance CRUD added
=======
>>>>>>> timedelta moved from testInstance to testTemplate

        return True
    except:
        return False