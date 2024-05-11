
from flask import Flask,jsonify,session,request
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:root@localhost/flask_databases'
db = SQLAlchemy(app)

class task(db.Model):
    id = db.Column(db.Integer , primary_key =True , autoincrement =True)
    tital =db.Column(db.String(200), nullable = False)
    done = db.Column(db.Boolean , default = False)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "hey"


@app.route('/tasks')
def get_tasks():
    tasks =task.query.all()
    task_list =[{'id':task.id,'tital':task.tital,'done':task.done} for task in tasks]
    return jsonify({'tasks':   task_list})

@app.route('/task',methods = ['post','GET'])
def create_task():
    Data = request.get_json()
    new_task = task( tital = Data['tital'], done = Data['done'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'msg':'task created'})

if __name__ == "__main__":
    app.run(debug=True,port=5000)