# import libraries
import flask
from flask_cors import CORS
from models.models import db
import os
from dotenv import load_dotenv

# import routes
from liveliness.liveliness import liveliness_blueprint
from userProfile.userProfile import profile_blueprint
from question.question import question_blueprint
from grade.grade import grade_blueprint
from subject.subject import subject_blueprint
from topic.topic import topic_blueprint
from answer.answer import answer_blueprint
from testTemplate.testTemplate import test_blueprint
from questionTestAnswer.questionTestAnswer import question_test_answer_blueprint
from currentTestTemplate.currentTestTemplate import current_test_template_blueprint
<<<<<<< HEAD
<<<<<<< HEAD
from testInstance.testInstance import test_instance_blueprint
from submittedAnswer.submittedAnswer import submitted_answer_blueprint
<<<<<<< HEAD
=======
>>>>>>> currentTestTemplate model + CD
=======
from testInstance.testInstance import test_instance_blueprint
>>>>>>> testInstance CRUD added
=======
>>>>>>> submittedAnswer CRUD

# Load env variables
load_dotenv()
DB_URL = os.getenv('DB_URL')
DB_DBNAME = os.getenv('DB_DBNAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')


app = flask.Flask(__name__)
api_cors_headers = {
    "origins": [
        "localhost:3000",
        "http://localhost:3000",
    ],
    "methods": ["OPTIONS", "DELETE", "GET", "POST"],
    "allow_headers": ["Authorization", "Content-Type"]
}
cors = CORS(app, resources={"/*": api_cors_headers}, supports_credentials=True)  # nopep8


@app.before_first_request
def startup_project():
    db.create_all()


# define routes
@app.route('/', methods=['GET'])
def home():
    return {
        "data": {
            "message": "Currently supported endpoints",
            "endpoints": ["/liveliness"]
        },
        "status": 200
    }


app.register_blueprint(liveliness_blueprint, url_prefix='/liveliness')
app.register_blueprint(profile_blueprint, url_prefix='/profile')
app.register_blueprint(question_blueprint, url_prefix='/question')
app.register_blueprint(grade_blueprint, url_prefix='/grade')
app.register_blueprint(subject_blueprint, url_prefix='/subject')
app.register_blueprint(topic_blueprint, url_prefix='/topic')
app.register_blueprint(answer_blueprint, url_prefix='/answer')
app.register_blueprint(test_blueprint, url_prefix='/test')
app.register_blueprint(question_test_answer_blueprint, url_prefix='/qta')
app.register_blueprint(current_test_template_blueprint, url_prefix='/current_test_template')
<<<<<<< HEAD
<<<<<<< HEAD
app.register_blueprint(test_instance_blueprint, url_prefix='/test_instance')
app.register_blueprint(submitted_answer_blueprint, url_prefix='/submitted_answer')
=======
>>>>>>> currentTestTemplate model + CD
=======
app.register_blueprint(test_instance_blueprint, url_prefix='/test_instance')
<<<<<<< HEAD
>>>>>>> testInstance CRUD added
=======
app.register_blueprint(submitted_answer_blueprint, url_prefix='/submitted_answer')
>>>>>>> submittedAnswer CRUD


app.config["DEBUG"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + DB_USER+':'+DB_PASS+'@'+DB_URL+'/'+DB_DBNAME  # nopep8
db.init_app(app)

if __name__ == "__main__":
    # set up app variables for development
    # the production entrypoint for the project is the wsgi.py file in this dir

    print(app.url_map)
    app.run(port=8002)
    db.create_all()
