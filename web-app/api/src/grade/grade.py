from flask import Blueprint, request
from util import generateResponse, generateError, getDecodedJWTTokens, isUserAdmin, validateQueryJson, searchByRoute
from models.models import Grade, db

grade_blueprint = Blueprint('grade', __name__)

@grade_blueprint.route('/', methods=['POST'])
def createGrade():
    # validate JWT token and permissions token
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])
    
    if not isUserAdmin(perm_token):
        generateError(403, "User is not admin")

    # create new Grade and return its id and name if no grade with the same id is found
    if (validateGradeJson(request.json, True)):
        result = Grade.query.filter_by(id=request.json['id']).first()

        if result:
            return generateError(409, "Grade with this ID already exists")
        
        grade = Grade(
            id=request.json['id'],
            name=request.json['name']
        )

        db.session.add(grade)
        db.session.commit()
        return generateResponse(Grade.jsonify(grade))
    else:
        return generateError(400, "Bad request format")


# function for ONLY managing (RUD) existing Grades Update Delete accessible only by admins
@grade_blueprint.route('/<g_id>', methods=['GET', 'POST', 'DELETE'])
def manageGrade(g_id):
    result = Grade.query.filter_by(id=g_id).first()

    if not result:
        return generateError(404, "Grade not found")

    if (request.method == 'GET'):
        return generateResponse(Grade.jsonify(result))

    else:
        try:
            id_token, perm_token = getDecodedJWTTokens(request)
        except Exception as error:
            return generateError(error.args[0], error.args[1])
            
        if not isUserAdmin(perm_token):
            return generateResponse(403, "User is not Admin")
        
        if (request.method == 'POST'):  
            if validateGradeJson(request.json, False):
                result.name = request.json['name']

                db.session.add(result)
                db.session.commit()
                return generateResponse(Grade.jsonify(result))
            else:
                return generateError(400, "Bad request")
        
        if (request.method == 'DELETE'):
            db.session.delete(result)
            db.session.commit()
            return generateResponse("Grade deleted")


@grade_blueprint.route('/all', methods=['GET'])
def showAllGrades():
    all_grades = Grade.query.all()

    result = []
    for grade in all_grades:
        grade_push = Grade.jsonify(grade)
        result.append(grade_push)

    return generateResponse(result)


def validateGradeJson(json, includeID):
    try:
        if includeID:
            id = json['id']
        
        name = json['name']

        return True
    except:
        return False