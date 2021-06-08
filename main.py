from flask import Flask, abort
from flask_restful import Api, Resource
import requests
from routes import req

from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.utils import send_from_directory

BASE_1 = "https://jsonplaceholder.typicode.com/users"
BASE_2 = "https://jsonplaceholder.typicode.com/albums"

userdata = requests.get(BASE_1).json()
albumdata = requests.get(BASE_2).json()

app = Flask(__name__)
api= Api(app)
app.config['SWAGGER'] = {"tittle": "swagger-ui", "uiversion": 2}

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Album App"
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
@app.route('/static/<path:path>')
def getswagger(path):
    return send_from_directory('static', path)

class Getuser(Resource):
    def get(self):
        return {'data' : userdata}


class Getalbum(Resource):
    
    def get(self, user_id):
        for album in userdata:
            data =[]
            if user_id not in data:
                data = [element for element in albumdata if element['userId'] == user_id]
                return{'data' : data}
            else:
                abort(404)
            
        
api.add_resource(Getuser, '/users')
api.add_resource(Getalbum, '/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
