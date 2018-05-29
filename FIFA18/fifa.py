from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
import random
import string
from MySQL import userauthentication, usersignup, matchrender, matchinput,pwresetuser,mybids,winnerpointupdate,currentstanding,usr1,adminlogin1,WeeklyPointUpdate1,UpdateMatch1,pwreset3
from flask import jsonify
import smtplib
from flask_mail import Mail,Message
from werkzeug.utils import secure_filename
import os
from datetime import timedelta
from flask import session, app,g
fifa18 = Flask(__name__)
secretkey = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
fifa18.secret_key = secretkey
APP_ROOT=os.path.dirname(os.path.abspath(__file__))
fifa18.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='arijitd1791@gmail.com',
    MAIL_PASSWORD='zwjnvsaitxwdkdwp',     
)
mail=Mail(fifa18)
#login required decorator
def login_required(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			return render_template("index.html", error="Macha you need to login/SignUP first Machaaaaa",b="b")
	return wrap
def login_required2(k):
	@wraps(k)
	def wrap(*args,**kwargs):
		if 'logged_in2' in session:
			return k(*args,**kwargs)
		else:
			return render_template("adminlogin.html", error="you need to login/SignUP first, please contact the administrator ")
	return wrap
@fifa18.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@fifa18.route('/')
def index():
    session.pop('logged_in', None)
    session.pop('id11',None)
    session.pop('teamname11',None)
    session.pop('teamcaptain31',None)
    return render_template("index.html",b="b")
@fifa18.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('logged_in', None)
    session.pop('id11',None)
    session.pop('teamname11',None)
    session.pop('teamcaptain31',None)
    error = None
    if request.method == 'POST':
        #global teamname1, id1,teamcaptain3
        out, id1, teamname1,teamcaptain3 = userauthentication(request.form['username'], request.form['password'])
        session['id11']=id1
        session['teamname11']=teamname1
        session['teamcaptain31']=teamcaptain3
        if out == 'User Not Present':
            error = 'User Not Registered, Please Register'
        else:
            if out == 'false':
                error = 'Invalid Credentials, please try Again'
            else:
                session['logged_in'] = True
                return render_template("main.html",teamname2=session['teamname11'])
    return render_template("index.html", error=error,b="b")


@fifa18.route('/signup', methods=['GET', 'POST'])
def signup():
    session.pop('logged_in', None)
    session.pop('id11',None)
    session.pop('teamname11',None)
    session.pop('teamcaptain31',None)
    message = None
    if request.method == 'POST':
        teamname = request.form["teamname"]
        teamcaptain = request.form["teamcaptain"]
        member1 = request.form["member1"]
        member2 = request.form["member2"]
        member3 = request.form["member3"]
        username = request.form["username1"]
        password = request.form["password1"]
        fname2=request.form["teamname"]
        photo=None
        try:
            photo = request.files['file']
        except Exception as e:
            print(str(e))
        target=os.path.join(APP_ROOT,'static\\img\\faces\\')
        fname=fname2+".jpeg"
        out = usersignup(teamname, teamcaptain, member1,
                         member2, member3, username, password)
        if out == 'failure':
            teamname1=request.form['teamname']
            message = ('Unable to Register,UserId/TeamName already taken')
        else:
            if photo:
                destination=os.path.join(target,fname)
                photo.save(destination)
            else:
                print("no photo found to save")
            message = (request.form['teamname']+' Registered Succesfully')
    return render_template("index.html", message=message,a="a")

@fifa18.route('/pwreset',methods=['GET', 'POST'])
def pwreset():
    session.pop('logged_in', None)
    session.pop('id11',None)
    session.pop('teamname11',None)
    session.pop('teamcaptain31',None)
    message = None
    if request.method == 'POST':
        username = request.form["username2"]
        error, pas, username1, teamcaptain1 = pwresetuser(request.form["username2"])
        error=str(error)
        if error=="None":
            try:
                msg=Message("Password Reset",sender="fifa@gmail.com",recipients=[teamcaptain1])
                msg.body="Hello your password has been succesfully changed your new password is "+pas
                mail.send(msg)
                message="Please check your mail new password has been sent"
            except Exception as e:
                message="technical error,please contact the administrator"
        else:
            message="User Does Not Exist, please register first"
    return render_template("index.html", message3=message,c="c")


@fifa18.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
    message = None
    disabled = None
    teamname2 = session['teamname11']
    id2 = session['id11']
    matchrender1 = matchrender(id2)
    if request.method == 'POST':
        result = request.form
        result2 = result.to_dict(flat=False)
        output = []
        for i in range(len(result2['matchnumber'])):
            di = {}
            for key in result2.keys():
                di[key] = result2[key][i]
            output.append(di)
        for data in output:
            matchinput(id2, data.get('matchnumber'),    
                       data.get('winner'), data.get('point'))
        try:
            msg=Message("Your Bids For Today",sender="fifa@gmail.com",recipients=[session['teamcaptain31'],"arijitd1791@gmail.com"])
            msg.body=render_template("mailtemplate.txt",mybids1=output,teamname2=teamname2)
            msg.html=render_template("mailtemplate.html",mybids1=output,teamname2=teamname2)
            mail.send(msg)
        except Exception as e:
            print(str(e))
        return redirect(url_for('confirm'))
    sumpoints = 0
    for data in matchrender1:
        sumpoints = sumpoints +data.get('points')
    if sumpoints > 0:
        return render_template("welcome.html",message=matchrender1,teamname2=teamname2,disabled=" readonly",k=None,p=None,c1="nav-item active")
    else:
        return render_template("welcome.html",message=matchrender1,teamname2=teamname2,disabled=disabled ,k="k",p=None,c1="nav-item active")


@fifa18.route('/confirm')
@login_required
def confirm():
    return render_template("confirm.html",teamname2=session['teamname11'])

@fifa18.route('/bids',methods=['GET', 'POST'])
@login_required
def bids():
    id2=session['id11']
    mybids1=mybids(id2)
    return render_template("yourbid.html",mybids1=mybids1,teamname2=session['teamname11'],c2="nav-item active")

@fifa18.route('/currentstanding1',methods=['GET', 'POST'])
@login_required
def currentstanding1():
    date=None
    custan=currentstanding()
    for data in custan:
        date=data.get("updatedatetime")
    return render_template("standings.html",custan=custan,teamname2=session['teamname11'],c3="nav-item active")

@fifa18.route('/acc',methods=['GET', 'POST'])
@login_required
def acc():
    id2=session['id11']
    team=usr1(id2)
    return render_template("user.html",teamname2=session['teamname11'],team=team,error1=request.args.get('error'))

@fifa18.route('/pwreset2',methods=['GET', 'POST'])
@login_required
def pwreset2():
    if request.method == 'POST':
        id2=session['id11']
        password2=request.form["Password"]               
        print(password2,id2)
        e=pwreset3(password2,id2)
        if e:
            error="something went wrong please try gain later"
            return redirect(url_for('acc',error=error))
        else:
            session.pop('logged_in', None)
            session.pop('id11',None)
            session.pop('teamname11',None)
            session.pop('teamcaptain31',None)
            return render_template("pwreset.html")       
    return redirect(url_for('acc'))

@fifa18.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('id11',None)
    session.pop('teamname11',None)
    session.pop('teamcaptain31',None)
    #return render_template("logout.html")
    return redirect(url_for('index'))

@fifa18.route('/Fbjxc6FRC8lzslW6FRC8lRC8lzslW6',methods=['GET', 'POST'])
def adminlogin():
    session.pop('logged_in2', None)
    session.pop('logged_in2', None)
    session.pop('logged_in2', None)
    error = None
    print("started")
    if request.method == 'POST':
        global adminusername
        adminusername=request.form['username']
        out = adminlogin1(request.form['username'], request.form['password'])
        print(out)
        if out == 'True':
            session['logged_in2'] = True
            print(session)
            return redirect(url_for('adminpage'))
        else:
            error="usename/password invalid or Something went wrong please try again later"
            return render_template("adminlogin.html", error=error)
    return render_template("adminlogin.html", error=error)
@fifa18.route('/WeeklyPointUpdate',methods=['GET', 'POST'])
@login_required2
def WeeklyPointUpdate():
    error = None
    if request.method == 'POST':
        week = request.form.get("week")
        point= request.form["point"]
        error=WeeklyPointUpdate1(week,point)
        return render_template("adminpage.html", error=error)     
    return render_template("adminpage.html", error=error)
@fifa18.route('/UpdateMatch',methods=['GET', 'POST'])
@login_required2
def UpdateMatch():
    error = None
    if request.method == 'POST':
        matchnumber = request.form["matchnumber"]
        team1= request.form["team1"]
        team2= request.form["team2"]
        error=UpdateMatch1(matchnumber,team1,team2)
        return render_template("adminpage.html", error=error)
    return render_template("adminpage.html", error=error)
@fifa18.route('/UpdateMatchWinner',methods=['GET', 'POST'])
@login_required2
def UpdateMatchWinner():
    error = None
    if request.method == 'POST':
        matchnumber2 = request.form["matchnumber2"]
        matchwinner= request.form["matchwinner"]
        error=winnerpointupdate(matchnumber2,matchwinner)
        return render_template("adminpage.html", error=error)
    return render_template("adminpage.html", error=error)

@fifa18.route('/Fbjxc6FRC8lzslW6FRC8lRC8lzslW6jxc6FRC8lzslW6FRC8',methods=['GET', 'POST'])
@login_required2
def adminpage():
    error = None
    return render_template("adminpage.html", error=error,admin=adminusername)

@fifa18.route('/logout2')
@login_required2
def logout2():
    session.pop('logged_in2', None)
    session.pop('logged_in2', None)
    session.pop('logged_in2', None)
    return redirect(url_for('adminlogin'))


if __name__ == "__main__":
    fifa18.run(debug=True)
