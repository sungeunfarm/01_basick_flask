import os
from flask import Flask,request,redirect
from flask import render_template
from models import db

from models import Fcuser

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('hello.html')


@app.route('/register',methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        # print(request.form)
        userid = request.form.get('userid')
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re-password')

        if (userid and username and password and re_password) and password == re_password :
            # DB 저장 
            fcuser = Fcuser()
            fcuser.userid = userid
            fcuser.username = username
            fcuser.password = password

            db.session.add(fcuser)
            db.session.commit()

            return redirect('/')

    return render_template('register.html')



if __name__ == '__main__':

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(BASE_DIR, 'db.sqlite')

    app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///'+ dbfile
    # 사용자 요청이 끝날때마다 커밋을한다 (커밋 데이터베이스에 반영한다.)
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    db.app = app
        
    with app.app_context():
        db.create_all()

    app.run(debug=True)