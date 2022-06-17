from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
db = SQLAlchemy()


class Profile(db.Model):
    __tablename__ = 'main_api_profile'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    pic_url = db.Column(db.String(300), nullable=True)
    jwt_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Profile %r>' % self.id

    def __init__(self, id, name, pic_url, jwt_id):
        self.id = id
        self.name = name
        self.pic_url = pic_url
        self.jwt_id = jwt_id

    def jsonify(self):
        data = {
            "id": self.id,
            "name": self.name,
            "pic_url": self.pic_url,
        }

        return data


class Question(db.Model):
    __tablename__ = 'main_api_question'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.Integer, db.CheckConstraint('difficulty>0'), db.CheckConstraint('difficulty<11'), nullable=False) #nopep8

    # foreign keys
    ownerID = db.Column(db.Integer, db.ForeignKey('main_api_profile.id', ondelete="set null"), nullable=True)  # nopep8
    subjectID = db.Column(db.Integer, db.ForeignKey('main_api_subject.id', ondelete="set null"), nullable=True)  # nopep8
    topicID = db.Column(db.Integer, db.ForeignKey('main_api_topic.id', ondelete="set null"), nullable=True)  # nopep8

    def __repr__(self):
        return '<Question %r>' % self.id

    def __init__(self, text, description, difficulty, ownerID, subjectID, topicID):
        self.text = text
        self.description = description
        self.difficulty = difficulty
        self.ownerID = ownerID
        self.subjectID = subjectID
        self.topicID = topicID

    def jsonify(self):
        data = {
            "id": self.id,
            "text": self.text,
            "description": self.description,
            "difficulty": self.difficulty,
            "ownerID": self.ownerID,
            "subjectID": self.subjectID,
            "topicID": self.topicID
        }

        return data


class Grade(db.Model):
    __tablename__ = 'main_api_grade'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable = False)

    def __repr__(self):
        return '<Grade %r>' % self.id

    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def jsonify(self):
        data = {
            "id": self.id,
            "name": self.name
        }

        return data


class Subject(db.Model):
    __tablename__ = 'main_api_subject'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    # foreign keys
    gradeID = db.Column(db.Integer, db.ForeignKey('main_api_grade.id', ondelete="set null"), nullable=True)  # nopep8

    def __repr__(self):
        return '<Subject %r>' % self.id

    def __init__(self, name, gradeID):
        self.name = name
        self.gradeID = gradeID

    def jsonify(self):
        data = {
            "id": self.id,
            "name": self.name,
            "gradeID": self.gradeID
        }

        return data


class Topic(db.Model):
    __tablename__ = 'main_api_topic'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    # foreign keys
    subjectID = db.Column(db.Integer, db.ForeignKey('main_api_subject.id', ondelete="set null"), nullable=True)  # nopep8

    def __repr__(self):
        return '<Topic %r>' % self.id

    def __init__(self, name, subjectID):
        self.name = name
        self.subjectID = subjectID

    def jsonify(self):
        data = {
            "id": self.id,
            "name": self.name,
            "subjectID": self.subjectID
        }

        return data


class Answer(db.Model):
    __tablename__ = 'main_api_answer'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    is_correct = db.Column(db.Boolean, nullable=False)

    # foreign keys  
    questionID = db.Column(db.Integer, db.ForeignKey('main_api_question.id', ondelete="set null"), nullable=True)  # nopep8
    ownerID = db.Column(db.Integer, db.ForeignKey('main_api_profile.id', ondelete="cascade"), nullable=False)  # nopep8

    def __repr__(self):
        return '<Answer %r>' % self.id

    def __init__(self, text, explanation, is_correct, questionID, ownerID):
        self.text = text
        self.explanation = explanation
        self.is_correct = is_correct
        self.questionID = questionID
        self.ownerID = ownerID

    def jsonify(self):
        data = {
            "id": self.id,
            "text": self.text,
            # we don't expose whether the answer is correct in the user-facing (student) API by default
            # whether an answer is correct will be added to the json conditionally in the API route if it is needed
            "explanation": self.explanation,
            "questionID": self.questionID,
            "ownerID": self.ownerID
        }

        return data


class Test(db.Model):
    __tablename__ = 'main_api_test'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False)
    date_accessed = db.Column(db.DateTime, nullable=True)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    max_time_allowed = db.Column(db.Integer, nullable=True)
=======
>>>>>>> currentTestTemplate model + CD
=======
    timedelta = db.Column(db.Interval, nullable=True)
>>>>>>> timedelta moved from testInstance to testTemplate
=======
    max_time_allowed = db.Column(db.Interval, nullable=True)
>>>>>>> testTemplate: rename timedelta; testInstance: model change for deadline, condition for GET DELETE access moved in funct
=======
    max_time_allowed = db.Column(db.Integer, nullable=True)
>>>>>>> timedelta model changed - store as integer, convert to interval when needed

    # foreign keys
    ownerID = db.Column(db.Integer, db.ForeignKey('main_api_profile.id', ondelete="set null"), nullable=True)  # nopep8
    subjectID = db.Column(db.Integer, db.ForeignKey('main_api_subject.id', ondelete="set null"), nullable=True)  # nopep8
    topicID = db.Column(db.Integer, db.ForeignKey('main_api_topic.id', ondelete="set null"), nullable=True)  # nopep8

    def __repr__(self):
        return '<Test %r>' % self.id

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    def __init__(self, description, max_time_allowed, ownerID, subjectID, topicID):
=======
    def __init__(self, description, ownerID, subjectID, topicID):
>>>>>>> currentTestTemplate model + CD
        self.description = description
        self.date_created = datetime.now()
        self.date_accessed = None
        self.max_time_allowed = max_time_allowed
=======
    def __init__(self, description, timedelta, ownerID, subjectID, topicID):
        self.description = description
        self.date_created = datetime.now()
        self.date_accessed = None
        self.timedelta = timedelta
>>>>>>> timedelta moved from testInstance to testTemplate
=======
    def __init__(self, description, max_time_allowed, ownerID, subjectID, topicID):
        self.description = description
        self.date_created = datetime.now()
        self.date_accessed = None
        self.max_time_allowed = max_time_allowed
>>>>>>> testTemplate: rename timedelta; testInstance: model change for deadline, condition for GET DELETE access moved in funct
        self.ownerID = ownerID
        self.subjectID = subjectID
        self.topicID = topicID

    def jsonify(self):
        data = {
            "id": self.id,
            "description": self.description,
            "date_created": self.date_created,
            "date_accessed": self.date_accessed,
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            "max_time_allowed": self.max_time_allowed,
=======
            "timedelta": str(self.timedelta) + " hours",
>>>>>>> timedelta moved from testInstance to testTemplate
=======
            "max_time_allowed": str(self.max_time_allowed),
>>>>>>> testTemplate: rename timedelta; testInstance: model change for deadline, condition for GET DELETE access moved in funct
=======
            "max_time_allowed": int(float(self.max_time_allowed.total_seconds())),
>>>>>>> change testTemplate timedelta to be based in seconds
=======
            "max_time_allowed": self.max_time_allowed,
>>>>>>> timedelta model changed - store as integer, convert to interval when needed
            "ownerID": self.ownerID,
            "subjectID": self.subjectID,
            "topicID": self.topicID
        }
        return data


class CurrentTestTemplate(db.Model):
    __tablename__ = 'main_api_current_test_template'

    id = db.Column(db.Integer, primary_key=True)
<<<<<<< HEAD
<<<<<<< HEAD
    is_current = db.Column(db.Boolean, nullable=False)
    
    #foreign keys
    ownerID = db.Column(db.Integer, db.ForeignKey('main_api_profile.id', ondelete="cascade"), nullable=True)  # nopep8
    testID = db.Column(db.Integer, db.ForeignKey('main_api_test.id', ondelete="cascade"), nullable=True)  # nopep8
<<<<<<< HEAD
=======
=======
    is_current = db.Column(db.Boolean, nullable=False)
>>>>>>> edit testTemplate route
    
    #foreign keys
    ownerID = db.Column(db.Integer, db.ForeignKey('main_api_profile.id', ondelete="set null"), nullable=True)  # nopep8
    testID = db.Column(db.Integer, db.ForeignKey('main_api_test.id', ondelete="set null"), nullable=True)  # nopep8
>>>>>>> currentTestTemplate model + CD
=======
>>>>>>> error codes and models adjustment
    previousTestID = db.Column(db.Integer, db.ForeignKey('main_api_test.id', ondelete="set null"), nullable=True)  # nopep8

    def __repr__(self):
        return 'CurrentTestTemplate %r>' % self.id

<<<<<<< HEAD
<<<<<<< HEAD
    def __init__(self, is_current, ownerID, testID, previousTestID):
        self.is_current = is_current
=======
    def __init__(self, ownerID, testID, previousTestID):
>>>>>>> currentTestTemplate model + CD
=======
    def __init__(self, is_current, ownerID, testID, previousTestID):
        self.is_current = is_current
>>>>>>> edit testTemplate route
        self.ownerID = ownerID
        self.testID = testID
        self.previousTestID = previousTestID
    
    def jsonify(self):
        data = {
            "id": self.id,
<<<<<<< HEAD
<<<<<<< HEAD
            "is_current": self.is_current,
=======
>>>>>>> currentTestTemplate model + CD
=======
            "is_current": self.is_current,
>>>>>>> edit testTemplate route
            "ownerID": self.ownerID,
            "testID": self.testID,
            "previousTestID": self.previousTestID
        }
        return data


class QuestionTestAnswer(db.Model):
    __tablename__ = 'main_api_question_test_answer'

    # foreign keys
    questionID = db.Column(db.Integer, db.ForeignKey('main_api_question.id', ondelete="cascade"), primary_key=True)  # nopep8
    testID = db.Column(db.Integer, db.ForeignKey('main_api_test.id', ondelete="cascade"), primary_key=True)  # nopep8
    answerID = db.Column(db.Integer, db.ForeignKey('main_api_answer.id', ondelete="cascade"), primary_key=True)  # nopep8

    def __repr__(self):
        return '<QuestionTestAnswer - %r - %r - %r>' % (self.questionID, self.testID, self.answerID)

    def __init__(self, questionID, testID, answerID):
        self.questionID = questionID
        self.testID = testID
        self.answerID = answerID

    # no jsonify function, as this table is meant to only handle the relationship internally
    # to return data to the user, expand the entries in this table and jsonify them


class TestInstance(db.Model):
    __tablename__ = 'main_api_test_instance'
    
    id = db.Column(db.Integer, primary_key=True)
    time_started = db.Column(db.DateTime, nullable=False)
<<<<<<< HEAD
<<<<<<< HEAD
    time_finished = (db.Column(db.DateTime, nullable=True))
    deadline = db.Column(db.DateTime, nullable=False)
=======
    quarter_hrs = db.Column(db.Integer, nullable=False)
    time_finished = (db.Column(db.DateTime, nullable=True))
<<<<<<< HEAD
    time_limit = db.Column(db.DateTime, nullable=False)
>>>>>>> testInstance CRUD added
=======
    time_limit = db.Column(db.Interval, nullable=False)
>>>>>>> error codes and models adjustment
=======
    time_finished = (db.Column(db.DateTime, nullable=True))
    deadline = db.Column(db.DateTime, nullable=False)
>>>>>>> timedelta moved from testInstance to testTemplate

    #foreign keys
    takerID = db.Column(db.Integer, db.ForeignKey('main_api_profile.id', ondelete="cascade"), nullable=True)  # nopep8
    testID = db.Column(db.Integer, db.ForeignKey('main_api_test.id', ondelete="cascade"), nullable=False)  # nopep8

    def __repr__(self):
        return '<TestInstance %r>' % self.id

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    def __init__(self, takerID, testID, time_limit):
        self.takerID = takerID
        self.testID = testID
        self.time_started = datetime.now()
        self.deadline = datetime.now() + time_limit
=======
    def __init__(self, takerID, testID, quarter_hrs):
        self.takerID = takerID
        self.testID = testID
        self.time_started = datetime.now()
        self.quarter_hrs = quarter_hrs
<<<<<<< HEAD
        self.time_limit = self.time_started + timedelta(minutes=quarter_hrs*15)
>>>>>>> testInstance CRUD added
=======
        self.time_limit = timedelta(minutes=quarter_hrs*15)
>>>>>>> one fucntion to create and update submittedAnswer
=======
    def __init__(self, takerID, testID, time_started, deadline):
        self.takerID = takerID
        self.testID = testID
        self.time_started = time_started
        self.deadline = deadline
>>>>>>> timedelta moved from testInstance to testTemplate
=======
    def __init__(self, takerID, testID, time_limit):
        self.takerID = takerID
        self.testID = testID
        self.time_started = datetime.now()
        self.deadline = datetime.now() + time_limit
>>>>>>> testTemplate: rename timedelta; testInstance: model change for deadline, condition for GET DELETE access moved in funct
        self.time_finished = None
        
    
    def jsonify(self):
        data = {
            "id": self.id,
            "takerID": self.takerID,
            "testID": self.testID,
            "time_started": self.time_started,
<<<<<<< HEAD
<<<<<<< HEAD
            "deadline": self.deadline,
            "time_finished": self.time_finished,
        }

        return data


class SubmittedAnswer(db.Model):
    __tablename__ = 'main_api_submitted_answers'

    #foreign keys
    testInstanceID = db.Column(db.Integer, db.ForeignKey('main_api_test_instance.id', ondelete="cascade"), primary_key=True, nullable=False)  # nopep8
    # can't leave blank because no point to create submitted answer if not tied to question
    questionID = db.Column(db.Integer, db.ForeignKey('main_api_question.id', ondelete="cascade"), primary_key=True, nullable=False)  # nopep8
    answerID = db.Column(db.Integer, db.ForeignKey('main_api_answer.id', ondelete="cascade"), primary_key=True, nullable=True)  # nopep8

    def __repr__(self):
        return '<Answer %r>' % self.id

    def __init__(self, testInstanceID, answerID, questionID):
        self.editable = True
        self.questionID = questionID
        self.testInstanceID = testInstanceID
        self.answerID = answerID
    
    def jsonify(self):
        data = {
            "testInstanceID": self.testInstanceID,
            "questionID": self.questionID,
            "answerID": self.answerID
=======
            "quarter_hrs": self.quarter_hrs,
            "time_finished": self.time_finished,
<<<<<<< HEAD
            "time_limit": self.time_limit
>>>>>>> testInstance CRUD added
=======
            "time_limit": self.time_limit + self.time_started
>>>>>>> one fucntion to create and update submittedAnswer
=======
            "deadline": self.deadline,
            "time_finished": self.time_finished,
>>>>>>> timedelta moved from testInstance to testTemplate
        }

        return data


class SubmittedAnswer(db.Model):
    __tablename__ = 'main_api_submitted_answers'

    #foreign keys
    testInstanceID = db.Column(db.Integer, db.ForeignKey('main_api_test_instance.id', ondelete="cascade"), primary_key=True, nullable=False)  # nopep8
    # can't leave blank because no point to create submitted answer if not tied to question
    questionID = db.Column(db.Integer, db.ForeignKey('main_api_question.id', ondelete="cascade"), primary_key=True, nullable=False)  # nopep8
    answerID = db.Column(db.Integer, db.ForeignKey('main_api_answer.id', ondelete="cascade"), primary_key=True, nullable=True)  # nopep8

    def __repr__(self):
        return '<Answer %r>' % self.id

    def __init__(self, testInstanceID, answerID, questionID):
        self.editable = True
        self.questionID = questionID
        self.testInstanceID = testInstanceID
        self.answerID = answerID
    
    def jsonify(self):
        data = {
            "testInstanceID": self.testInstanceID,
            "questionID": self.questionID,
            "answerID": self.answerID
        }

        return data


class SubscriptionPlan(db.Model):
    __tablename__ = 'main_api_subscription_plan'

    id = db.Column(db.Integer, primary_key=True)
    desciption = db.Column(db.Text, nullable=False)
    price_bgn = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<SubscriptionPlan %r>' % self.id

    def __init__(self, description, price_bgn):
        self.description = description
        self.price_bgn = price_bgn

    def jsonify(self):
        data = {
            'id': self.id,
            'description': self.desciption,
            'price_bgn': self.price_bgn
        }

        return data


class Subscription(db.Model):
    __tablename__ = 'main_api_subscription'

    id = db.Column(db.Integer, primary_key=True)
    is_valid = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    # foreign keys
    planID = db.Column(db.Integer, db.ForeignKey('main_api_subscription_plan.id', ondelete="cascade"))  # nopep8
    profileID = db.Column(db.Integer, db.ForeignKey('main_api_profile.id', ondelete="cascade"))  # nopep8

    def __repr__(self):
        return '<Subscription %r>' % self.id

    def __init__(self, planID, expires, profileID):
        self.planID = planID
        self.is_valid = False
        # expires will have to be calculated before the subscription is created
        # based on the billing period of the subscription plan
        self.expires = expires
        self.profile = profileID

    def jsonify(self):
        data = {"TO": "DO"}
        return data
