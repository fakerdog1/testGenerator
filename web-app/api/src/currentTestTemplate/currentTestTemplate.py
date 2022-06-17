from flask import Blueprint, request
from util import generateResponse, generateError, getDecodedJWTTokens, paginateArray, validateQueryJson, searchByRoute
from models.models import CurrentTestTemplate, Test, Profile, db

current_test_template_blueprint = Blueprint('current_test_template', __name__)

@current_test_template_blueprint.route('/', methods=['POST'])
<<<<<<< HEAD
<<<<<<< HEAD
def registerNewCurrentTestTemplate():
=======
def createCurrentTestTemplate():
>>>>>>> currentTestTemplate model + CD
=======
def registerNewCurrentTestTemplate():
>>>>>>> currentTestTemplate rework according to PR comments
    # validate JWT token and permissions token
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])
    profile = Profile.query.filter_by(jwt_id=id_token['userID']).first()

<<<<<<< HEAD
<<<<<<< HEAD
=======
    # create new question and return its id
>>>>>>> currentTestTemplate model + CD
=======
>>>>>>> currentTestTemplate rework according to PR comments
    if (validateCTTJson(request.json)):
        test = Test.query.filter_by(id=request.json['testID']).first()

        if not test:
            return generateError(404, 'Test not found')
<<<<<<< HEAD
<<<<<<< HEAD
        
        current = CurrentTestTemplate.query.filter_by(testID=request.json['testID']).first()

        if current:
            return generateError(409, "A version of this test template already exists")

        if request.json['previousTestID'] != None:
            prev = CurrentTestTemplate.query.filter_by(id=request.json['previousTestID']).first()

            prev.is_current = False
            db.session.add(prev)

            prevID = prev.id
        else:
            prevID = None
        
        ctt = CurrentTestTemplate(
            is_current=True,
            ownerID=profile.id,
            testID=test.id,
            previousTestID=prevID
=======

        prev = CurrentTestTemplate.query.filter_by(id=request.json['previousTestID']).first()

        if not prev:
            return generateError(404, "Previous test template not found")
=======
>>>>>>> check for previous currentTestTemplate existence in validateJson
        
        current = CurrentTestTemplate.query.filter_by(testID=request.json['testID']).first()

        if current:
            return generateError(409, "A version of this test template already exists")

        if request.json['previousTestID'] != None:
            prev = CurrentTestTemplate.query.filter_by(id=request.json['previousTestID']).first()

            prev.is_current = False
            db.session.add(prev)

            prevID = prev.id
        else:
            prevID = None
        
        ctt = CurrentTestTemplate(
            is_current=True,
            ownerID=profile.id,
<<<<<<< HEAD
            testID=request.json['testID'],
            previousTestID=request.json['previousTestID']
>>>>>>> currentTestTemplate model + CD
=======
            testID=test.id,
<<<<<<< HEAD
            previousTestID=prev.id
>>>>>>> currentTestTemplate rework according to PR comments
=======
            previousTestID=prevID
>>>>>>> check for previous currentTestTemplate existence in validateJson
        )

        db.session.add(ctt)
        db.session.commit()
<<<<<<< HEAD
<<<<<<< HEAD

        return generateResponse(CurrentTestTemplate.jsonify(ctt))
    else:
        return generateError(400, "Bad data")
=======
=======

>>>>>>> currentTestTemplate rework according to PR comments
        return generateResponse(CurrentTestTemplate.jsonify(ctt))
    else:
<<<<<<< HEAD
        return generateError(400, "Bad question data")
>>>>>>> currentTestTemplate model + CD
=======
        return generateError(400, "Bad data")
>>>>>>> check for previous currentTestTemplate existence in validateJson


# function for ONLY managing (RUD) existing questions
@current_test_template_blueprint.route('/<ctt_id>', methods=['GET'])
def manageQuestion(ctt_id):
    result = CurrentTestTemplate.query.filter_by(id=ctt_id).first()
    if not result:
        return generateError(404, "Test Template not found")

    if (request.method == 'GET'):
        return generateResponse(CurrentTestTemplate.jsonify(result))


# function to show all own questions paginated
@current_test_template_blueprint.route('/all', methods=['POST'])
def showTestTemplateHistory():
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])

    # try to read optional parameters in request
    try:
        page = request.json["page"]
    except:
        page = 0
    try:
        pageSize = request.json["pageSize"]
    except:
        pageSize = 50

    all_ctts = []
<<<<<<< HEAD
<<<<<<< HEAD
    all_ctts = CurrentTestTemplate.query.filter_by(ownerID=id_token['userID'], is_current=True).all()

    results = []
    ctt_hist = []
    for ctt in all_ctts:
        ctt_hist.append(
            {
                "CTT ID %s" % (ctt.id): 
                    {
                        "id": ctt.id, 
                        "testID": ctt.testID, 
                        "is_current": ctt.is_current, 
                        "previousTestID": ctt.previousTestID
                    }
            })
        
        if ctt.previousTestID != None:
            hist_row = ctt.previousTestID
            while hist_row != None:
                hist = CurrentTestTemplate.query.filter_by(ownerID=id_token['userID'], id=hist_row).first() # nopep8

                ctt_hist.append(
                    {
                        "PTT ID %s" % (hist.id): 
                            {
                                "id": hist.id, 
                                "testID": hist.testID, 
                                "is_current": hist.is_current, 
                                "previousTestID": hist.previousTestID
                            }
                    })
                
                if hist.previousTestID !=None:
                    hist_row = hist.previousTestID
                else:
                    hist_row = None    
        
        results.append(ctt_hist)
        ctt_hist = []
=======
    all_ctts = CurrentTestTemplate.query.filter_by(ownerID=id_token['userID']).all()
=======
    all_ctts = CurrentTestTemplate.query.filter_by(ownerID=id_token['userID'], is_current=True).all()
>>>>>>> testInstance CRUD added

    results = []
    ctt_hist = []
    for ctt in all_ctts:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        results.append({"id": ctt.id, "testID": ctt.testID, "previousTestID": ctt.previousTestID})
>>>>>>> currentTestTemplate model + CD
=======
        results.append({"id": ctt.id, "is_current": ctt.is_current, "testID": ctt.testID, "previousTestID": ctt.previousTestID})
>>>>>>> edit testTemplate route
=======
        results.append({"id": ctt.id, "testID": ctt.testID, "previousTestID": ctt.previousTestID})
>>>>>>> currentTestTemplate rework according to PR comments
=======
        ctt_hist.append(
            {
                "CTT ID %s" % (ctt.id): 
                    {
                        "id": ctt.id, 
                        "testID": ctt.testID, 
                        "is_current": ctt.is_current, 
                        "previousTestID": ctt.previousTestID
                    }
            })
        
        if ctt.previousTestID != None:
            hist_row = ctt.previousTestID
            while hist_row != None:
                hist = CurrentTestTemplate.query.filter_by(ownerID=id_token['userID'], id=hist_row).first() # nopep8

                ctt_hist.append(
                    {
                        "PTT ID %s" % (hist.id): 
                            {
                                "id": hist.id, 
                                "testID": hist.testID, 
                                "is_current": hist.is_current, 
                                "previousTestID": hist.previousTestID
                            }
                    })
                
                if hist.previousTestID !=None:
                    hist_row = hist.previousTestID
                else:
                    hist_row = None    
        
        results.append(ctt_hist)
        ctt_hist = []
>>>>>>> searchOwnHistory function

    paged_results = list(paginateArray(results, pageSize))

    data = {
        "page": page,
        "pageSize": pageSize,
        "nextPage": (page < (len(paged_results) - 1)),
        "results": paged_results[page] if ((page < len(paged_results))) else []
    }

    return generateResponse(data)


<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> testInstance CRUD added
@current_test_template_blueprint.route('/search', methods=['POST'])
def search_ctt():
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
    data = searchByRoute(page, pageSize, queries, performCTTQuery)

    return generateResponse(data)


# helper function to perform and format the actual queries
def performCTTQuery(field, value):
    ctt_hist = []
<<<<<<< HEAD
<<<<<<< HEAD
    if (field == "is_current"):
        ctt_hist = CurrentTestTemplate.query.filter_by(is_current=value).order_by(CurrentTestTemplate.id).all()  # nopep8
=======
    if (field == "is_correct"):
        ctt_hist = CurrentTestTemplate.query.filter(CurrentTestTemplate.is_correct.contains(value)).order_by(CurrentTestTemplate.id).all()  # nopep8    
>>>>>>> testInstance CRUD added
=======
    if (field == "is_current"):
        ctt_hist = CurrentTestTemplate.query.filter_by(is_current=value).order_by(CurrentTestTemplate.id).all()  # nopep8
>>>>>>> currentTestTemplate rework according to PR comments

    results = []
    for entry in ctt_hist:
        results.append({
            "id": entry.id, 
            "is_current": entry.is_current,
            "ownerID": entry.ownerID, 
            "testID": entry.testID, 
            "previousTestID": entry.previousTestID
        })

    return results


<<<<<<< HEAD
=======
>>>>>>> currentTestTemplate model + CD
=======
>>>>>>> testInstance CRUD added
def validateCTTJson(json):
    try:
        testID = json['testID']
        previousTestID = json['previousTestID']

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> check for previous currentTestTemplate existence in validateJson
        if json['previousTestID'] != None:
            prev_ctt = CurrentTestTemplate.query.filter_by(id=json['previousTestID']).first()

            if not prev_ctt:
                return False
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> currentTestTemplate model + CD
=======
                
>>>>>>> check for previous currentTestTemplate existence in validateJson
=======

>>>>>>> searchOwnHistory function
        return True
    except:
        return False