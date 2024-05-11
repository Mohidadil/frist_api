from flask import Flask,jsonify,session,request,render_template,redirect
from flask_sqlalchemy import SQLAlchemy 
import bcrypt
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:root@localhost/flask_databases'
db = SQLAlchemy(app)

class task(db.Model):
    id = db.Column(db.Integer , primary_key =True , autoincrement =True)
    name =db.Column(db.String(200), nullable = False)
    email =db.Column(db.String(200), unique = True , nullable = False)
    #done = db.Column(db.Boolean , default = False)
    password = db.Column(db.String(100),nullable = False)

    def __init__(self, email , password  ,name):

        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'),bcrypt,gensalt().decode('uft-8')) # type: ignore

    def check_password(self,password):
        return bcrypt.checkpw(password,encode('utf-8'), self,password.encode('utf-8')) # type: ignore
    
        
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "hey"


@app.route('/login',methods=['GET','POST'] )
def login():
     if request.method == 'post':
         email = request.form['email']
         password = request.form['password']
         user = User.query.filter_by(email=email).first
         
         if user and user.check_password(password):
             session['name']= user.name
             session['email']=user.email
             session['password']=user.password
             return redirect ('/dashboard')
     else :
         return render_template('login.page.html')

        
     #=task.query.all()
    #task_list =[{'id':task.id,'name':task.name,'done':task.done} for task in tasks]
    #return jsonify({'tasks':   task_list})


@app.route('/task',methods = ['post','GET'])
def create_task():
    Data = request.get_json()
    new_task = task( name = Data['tital'], done = Data['done'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'msg':'task created'})
 

if __name__ == "__main__":
    app.run(debug=True,port=5000)