#!flask/bin/python
from flask import Flask
from flask.ext.restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class ArmAPI(Resource):
    def __init__(self):
        
    
    def get(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass

class ArmLimbsAPI(Resource):
    def get(self, limb):
        pass

    def put(self, limb, action):
        pass


api.add_resource(ArmAPI, '/roboarm/api/v1.0/arm')
api.add_resource(ArmLimbsAPI, '/roboarm/api/v1.0/arm/<str:limb>/<str:action>')



tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.run(debug=True)
