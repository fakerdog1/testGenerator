from flask import Blueprint, request
from util import generateResponse, generateError, getDecodedJWTTokens, isUserAdmin, validateQueryJson, searchByRoute, paginateArray
from models.models import Subject, Grade, db

subject_blueprint = Blueprint('subject', __name__)


@subject_blueprint.route('/', methods=['POST'])
def createSubject():
    # validate JWT token and permissions token
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])
        
    if not isUserAdmin(perm_token):
        generateError(403, "User is not admin")
    
    if (validateSubjectJson(request.json)):
        grade = Grade.query.filter_by(id=request.json['gradeID']).first()

        if not grade:
            return generateError(404, "Grade does not exist")
    
        subject = Subject(
            name=request.json['name'],
            gradeID=grade.id
        )

        db.session.add(subject)
        db.session.commit()
        return generateResponse(Subject.jsonify(subject))
    else:
        return generateError(400, "Bad subject data")



# function for ONLY managing (RUD) existing subjects
@subject_blueprint.route('/<s_id>', methods=['GET', 'POST', 'DELETE'])
def manageSubject(s_id):
    result = Subject.query.filter_by(id=s_id).first()

    if not result:
        return generateError(404, "Subject not found")

    if (request.method == 'GET'):
        return generateResponse(Subject.jsonify(result))

    else:
        # anyone can read subjects, but for editing and deleting you need to be admin
        # validate JWT token and permissions token
        try:
            id_token, perm_token = getDecodedJWTTokens(request)
        except Exception as error:
            return generateError(error.args[0], error.args[1])

        # check whether the profile of the request sender is amint
        if not isUserAdmin(perm_token):
            return generateError(403, "User is not admin")
        
        if (request.method == 'POST'):
            if (validateSubjectJson(request.json)):
                result.name = request.json['name']
                result.gradeID = request.json['gradeID']

                db.session.add(result)
                db.session.commit()
                return generateResponse(Subject.jsonify(result))
            else:
                return generateError(400, "Bad request")

        if (request.method == 'DELETE'):
            db.session.delete(result)
            db.session.commit()
            return generateResponse("Subject deleted") 


@subject_blueprint.route('/all', methods=['POST'])
def showAllSubjects():
    # try to read optional paramaters in request
    try:
        page = request.json["page"]
    except:
        page = 0
    try:
        pageSize = request.json["pageSize"]
    except:
        pageSize = 50
    
    all_subjects = Subject.query.all()
    
    result = []
    for subject in all_subjects:
        obj = {
            "id": subject.id,
            "name": subject.name,
            "gradeID": subject.gradeID
        }
        result.append(obj)

    paged_results = list(paginateArray(result, pageSize))

    data = {
        "page": page,
        "pageSize": pageSize,
        "nextPage": (page < (len(paged_results) - 1)),
        "results": paged_results[page] if ((page < len(paged_results))) else []
    }

    return generateResponse(data)


# route to handle searching subjects
@subject_blueprint.route('/search', methods=['POST'])
def search_subjects():
    # try to read optional paramaters in request
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

    data = searchByRoute(page, pageSize, queries, performSubjectQuery)

    return generateResponse(data)


# helper function to perform and format the actual queries
def performSubjectQuery(field, value):
    subjects = []
    if (field == "name"):
        subjects = Subject.query.filter(Subject.name.contains(value)).order_by(Subject.id).all()  # nopep8
    if (field == "grade"):
        #TODO contains function can search only within strings // FIND A WAY to search for integers within longer integers
        subjects = Subject.query.filter_by(gradeID=value).order_by(Subject.id).all()  # nopep8
    results = []
    for subject in subjects:
        results.append({
            "id": subject.id, 
            "name": subject.name, 
            "gradeID": subject.gradeID
        })

    return results


def validateSubjectJson(json):
    try:
        name = json['name']
        gradeID = json['gradeID']

        return True
    except:
        return False