from flask import Blueprint, request
import validators
from util import generateResponse, generateError, getDecodedJWTTokens, isUserAdmin, validateQueryJson, searchByRoute
from models.models import Profile, db

profile_blueprint = Blueprint('profile', __name__)

@profile_blueprint.route('/register', methods=['POST'])
def registerProfile():
    # validate JWT token and permissions token
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])

    result = Profile.query.filter_by(jwt_id=id_token['userID']).first()
    if result:
        return generateError(400, "Profile already registered")

    if (validateProfileJson(request.json)):
        newProf = Profile(
            id=id_token['userID'],
            name=request.json['name'],
            pic_url=request.json['pic_url'],
            jwt_id=id_token['userID']
        )

        db.session.add(newProf)
        db.session.commit()
        return generateResponse(Profile.jsonify(newProf))
    else:
        generateError(400, "Bad profile info")


# this route is ONLY for managing your own profile.
@ profile_blueprint.route('/', methods=['GET', 'POST', 'DELETE'])
def manageOwnProfile():
    # validate JWT token and permissions token
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])

    # get entry for profile and handle request
    result = Profile.query.filter_by(jwt_id=id_token['userID']).first()
    if not result:
        return generateError(404, "Profile not found")

    if (request.method == 'GET'):
        return generateResponse(Profile.jsonify(result))

    if (request.method == 'POST'):
        if (validateProfileJson(request.json)):
            if result:
                result.name = request.json['name'],
                result.pic_url = request.json['pic_url'],

                db.session.add(result)
                db.session.commit()
                return generateResponse(Profile.jsonify(result))
        else:
            return generateError(400, "Bad request")

    if (request.method == 'DELETE'):
        db.session.delete(result)
        db.session.commit()
        return generateResponse("Profile deleted")


# this route is for managing other's profiles.
@profile_blueprint.route('/byID/<p_id>', methods=['GET', 'DELETE'])
def manage_profile(p_id):
    if (request.method == 'GET'):
        profile = Profile.query.filter_by(id=p_id).first()

        if (profile):
            return generateResponse(Profile.jsonify(profile))
        else:
            return generateError(404, "Profile not found")

    # validate JWT token and permissions
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])

    if (request.method == 'DELETE'):
        if (isUserAdmin(perm_token)):
            profile = Profile.query.filter_by(id=p_id).first()
            if (profile):
                db.session.delete(profile)
                db.session.commit()

                return generateResponse("Profile deleted")
            else:
                return generateError(404, "Profile not found")


# route to handle searching users
@profile_blueprint.route('/search', methods=['POST'])
def search_profiles():
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
    queries = validateQueryJson(request.json["queries"])

    data = searchByRoute(page, pageSize, queries, performProfileQuery)

    return generateResponse(data)


# helper function to perform and format the actual queries
def performProfileQuery(field, value):
    profiles = []
    if (field == "name"):
        profiles = Profile.query.filter(
            Profile.name.contains(value)).order_by(Profile.id).all()

    results = []
    for profile in profiles:
        results.append({"id": profile.id, "name": profile.name})

    return results


def validateProfileJson(json):
    try:
        name = json['name']
        pic_url = json['pic_url']

        if not (validators.url(pic_url)):
            return False

        return True
    except:
        return False
