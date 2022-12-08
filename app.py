import os
from flask import Flask,request,redirect
from flask import render_template
from models import db
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm

from models import Fcuser

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('hello.html')


@app.route('/register',methods = ['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
   
        # DB 저장 
        fcuser = Fcuser()
        fcuser.userid = form.data.get('userid')
        fcuser.username = form.data.get('username')
        fcuser.password = form.data.get('password')

        db.session.add(fcuser)
        db.session.commit()
        print('Success')
        return redirect('/')

    return render_template('register.html' , form = form)



if __name__ == '__main__':

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(BASE_DIR, 'db.sqlite')

    app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///'+ dbfile
    # 사용자 요청이 끝날때마다 커밋을한다 (커밋 데이터베이스에 반영한다.)
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'weflsdflsdoclsdflwefcvlcs'


    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)
    db.app = app
        
    with app.app_context():
        db.create_all()

    app.run(debug=True)