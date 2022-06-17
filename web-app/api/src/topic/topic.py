from flask import Blueprint, request
from util import generateResponse, generateError, getDecodedJWTTokens, isUserAdmin, validateQueryJson, searchByRoute, paginateArray
from models.models import Topic, Subject, db

topic_blueprint = Blueprint('topic', __name__)


@topic_blueprint.route('/', methods=['POST'])
def createTopic():
    # TODO subject id validation
    # validate JWT token and permissions token
    try:
        id_token, perm_token = getDecodedJWTTokens(request)
    except Exception as error:
        return generateError(error.args[0], error.args[1])

    # create new Topic and return its id
    if (validateTopicJson(request.json)):
        subject = Subject.query.filter_by(id=request.json['subjectID']).first()

        if not subject:
            return generateError(404, "Subject not found")

        if isUserAdmin(perm_token):
            topic = Topic(
                name=request.json['name'],
                subjectID=subject.id
            )

            db.session.add(topic)
            db.session.commit()
            return generateResponse(Topic.jsonify(topic))
        else:
            return generateError(403, "Not Authorized")
    else:
        return generateError(400, "Bad Topic data")


# function for ONLY managing (RUD) existing Topics
@topic_blueprint.route('/<t_id>', methods=['GET', 'POST', 'DELETE'])
def manageTopic(t_id):
    result = Topic.query.filter_by(id=t_id).first()

    if not result:
        return generateError(404, "Topic not found")

    if (request.method == 'GET'):
        return generateResponse(Topic.jsonify(result))

    else:
        # anyone can read Topics, but for editing and deleting you need to be admin
        # validate JWT token and permissions token
        try:
            id_token, perm_token = getDecodedJWTTokens(request)
        except Exception as error:
            return generateError(error.args[0], error.args[1])

        # check whether the profile of the request sender is admin
        if isUserAdmin(perm_token):
            if (request.method == 'POST'):
                if (validateTopicJson(request.json)):
                    if result:
                        subject = Subject.query.filter_by(id=request.json['subjectID']).first()
                        if subject:
                            result.name = request.json['name'],
                            result.subjectID = request.json['subjectID']

                            db.session.add(result)
                            db.session.commit()
                            return generateResponse(Topic.jsonify(result))
                        else:
                            return generateError(404, "Subject not found")
                    else:
                        return generateError(404, "Topic not found")
                else:
                    return generateError(400, "Bad request")

            if (request.method == 'DELETE'):
                db.session.delete(result)
                db.session.commit()
                return generateResponse("Topic deleted")
        else:
            return generateError(403, "Not Authorized")


@topic_blueprint.route('/all', methods=['POST'])
def showAllTopics():
    # try to read optional paramaters in request
    try:
        page = request.json["page"]
    except:
        page = 0
    try:
        pageSize = request.json["pageSize"]
    except:
        pageSize = 50
    try:
        subjectID = request.json["subjectID"]
    except:
        subjectID = None
    
    
    if subjectID == None:
        return generateError(400, "Bad request")
    else:
        subject = Subject.query.filter_by(id=subjectID).first()
        if not subject:
            return generateError(404, "Subject not found")
        all_topics = Topic.query.filter_by(subjectID=subject.id).all()

    result = []
    for topic in all_topics:
        obj = {
            "id": topic.id, 
            "name": topic.name, 
            "subjectID": topic.subjectID
        }
        result.append(obj)

    paged_results = list(paginateArray(result, pageSize))

    data = {
        "page": page,
        "pageSize": pageSize,
        "nextPage": (page < (len(paged_results) - 1)),
        "subjectFilterID": subjectID,
        "results": paged_results[page] if ((page < len(paged_results))) else []
    }

    return generateResponse(data)


# route to handle searching users
@topic_blueprint.route('/search', methods=['POST'])
def search_topics():
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

    data = searchByRoute(page, pageSize, queries, performTopicQuery)

    return generateResponse(data)


# helper function to perform and format the actual queries
def performTopicQuery(field, value):
    topics = []
    if (field == "name"):
        topics = Topic.query.filter(Topic.name.contains(value)).order_by(Topic.id).all()  # nopep8

    results = []
    for topic in topics:
        results.append(
            {
                "id": topic.id, 
                "name": topic.name
            })

    return results


def validateTopicJson(json):
    try:
        name = json['name']
        subjectID = json['subjectID']

        return True
    except:
        return False