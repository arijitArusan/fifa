import MySQLdb
import datetime
import time
from dateutil import parser
import random
import string
from random import choice,randint
DBCONN_NAME="myfifadb.cot3fn6vn803.ap-south-1.rds.amazonaws.com"
DBUSER_NAME="scott"
DBPASSWORD="scotttiger"
DBNAME="S3UploadDB"
referencetime1=datetime.datetime.strptime('2018-06-15 16:45', "%Y-%m-%d %H:%M")
referencetime2=datetime.datetime.strptime('2018-06-17 16:45', "%Y-%m-%d %H:%M")
referencetime3=datetime.datetime.strptime('2018-06-20 16:45', "%Y-%m-%d %H:%M")
referencetime4=datetime.datetime.strptime('2018-06-23 16:45', "%Y-%m-%d %H:%M")
referencetime5=datetime.datetime.strptime('2018-06-26 16:45', "%Y-%m-%d %H:%M")
referencetime6=datetime.datetime.strptime('2018-06-29 16:45', "%Y-%m-%d %H:%M")
referencetime7=datetime.datetime.strptime('2018-07-05 16:45', "%Y-%m-%d %H:%M")
referencetime8=datetime.datetime.strptime('2018-07-09 16:45', "%Y-%m-%d %H:%M")
referencetime9=datetime.datetime.strptime('2018-07-13 16:45', "%Y-%m-%d %H:%M")
timestamp=datetime.datetime.now()
#for debugging
#timestamp=datetime.datetime.strptime('2018-06-29 16:35:01', "%Y-%m-%d %H:%M:%S")
def userauthentication(userid,password):
    error=('true')
    database=MySQLdb.connect(DBCONN_NAME,DBUSER_NAME,DBPASSWORD,DBNAME)
    cursor=database.cursor()
    Null='Error'
    query=("select id,password,teamname,teamcaptain from users where userid in ('"+userid+"')")
    cursor.execute(query)
    data=cursor.fetchall()
    password_temp=[dict(id=row[0],password=row[1],teamname=row[2],teamcaptain=row[3]) for row in data]
    global id1,userid1,teamname1,teamcaptain3
    for data in password_temp:
        password_temp2=data.get('password')
        id1=data.get('id')
        teamname1=data.get('teamname')
        teamcaptain3=data.get('teamcaptain')
    database.close()
    if password_temp==[]:
        error='User Not Present'
        return error,Null,Null
    else:
        if password==password_temp2:
            return error,id1,teamname1,teamcaptain3
        else:
            error=('false')
            return error,Null,Null,Null
def usersignup(teamname1,teamcaptain1,member11,member21,member31,username1,password1):
    error=None
    flag1='false'
    flag2='false'
    database=MySQLdb.connect(DBCONN_NAME,DBUSER_NAME,DBPASSWORD,DBNAME)
    cursor=database.cursor()
    cursor2=database.cursor()
    insertquery=("insert into users (teamname,teamcaptain,member1,member2,member3,userid,password) values('"+teamname1+"','"+teamcaptain1+"','"+member11+"','"+member21+"','"+member31+"','"+username1+"','"+password1+"')")
    fetchquery1=("select userid from users")
    cursor.execute(fetchquery1)
    data=cursor.fetchall()
    userid_temp=[dict(userid=row[0]) for row in data]
    for dic in userid_temp:
        for pas in dic:
            userid_temp2=dic[pas]
            if userid_temp2==username1:
                flag1='true'
    fetchquery2=("select teamname from users")
    cursor.execute(fetchquery2)
    data=cursor.fetchall()
    teamname_temp=[dict(teamname=row[0]) for row in data]
    for dic in userid_temp:
        for pas in dic:
            teamname_temp2=dic[pas]
            if teamname_temp2==teamname1:
                flag2='true'      
    if flag1=='false' and flag2=='false':
        cursor.execute(insertquery)
        database.commit()
        cursor2.execute("select id,teamname from users where userid='"+username1+"'")
        data2=cursor2.fetchall()
        dictionary1=[dict(user=row[0],teamname=row[1]) for row in data2]
        for data in dictionary1:
            user_store=int((data.get('user')))
            user_store1=str((data.get('teamname')))
        cursor2.callproc('insertPrediction',[user_store,user_store1])
        database.commit()
        database.close()
        return('success')
    else:
        database.close()
        return('failure')
def matchrender(id1):
    database=MySQLdb.connect(DBCONN_NAME,DBUSER_NAME,DBPASSWORD,DBNAME)
    cursor=database.cursor()
    status=" readonly"
    id2=str(id1)
    if timestamp<referencetime1:
        cursor.execute("select m.matchno,m.referencedate,m.referencedate,m.team1,m.team2,p.id,p.points from matches m,prediction p where p.matchno=m.matchno and m.matchreference='1' and p.id='"+id2+"'")
        users = [dict(matchno=row[0],referencedate=row[1],date=row[2],team1=row[3],team2=row[4],id2=row[5],points=row[6]) for row in cursor.fetchall()]
        return(users)
    elif timestamp>referencetime1 and timestamp<referencetime2:
        cursor.execute("select m.matchno,m.referencedate,m.referencedate,m.team1,m.team2,p.id,p.points from matches m,prediction p where p.matchno=m.matchno and m.matchreference='2' and p.id='"+id2+"'")
        users = [dict(matchno=row[0],referencedate=row[1],date=row[2],team1=row[3],team2=row[4],id2=row[5],points=row[6]) for row in cursor.fetchall()]
        return(users)
    elif timestamp>referencetime2 and timestamp<referencetime3:
        cursor.execute("select m.matchno,m.referencedate,m.referencedate,m.team1,m.team2,p.id,p.points from matches m,prediction p where p.matchno=m.matchno and m.matchreference='3' and p.id='"+id2+"'")
        users = [dict(matchno=row[0],referencedate=row[1],date=row[2],team1=row[3],team2=row[4],id2=row[5],points=row[6]) for row in cursor.fetchall()]
        return(users)
    elif timestamp>referencetime3 and timestamp<referencetime4:
        cursor.execute("select m.matchno,m.referencedate,m.referencedate,m.team1,m.team2,p.id,p.points from matches m,prediction p where p.matchno=m.matchno and m.matchreference='4' and p.id='"+id2+"'")
        users = [dict(matchno=row[0],referencedate=row[1],date=row[2],team1=row[3],team2=row[4],id2=row[5],points=row[6]) for row in cursor.fetchall()]
        return(users)
    elif timestamp>referencetime4 and timestamp<referencetime5:
        cursor.execute("select m.matchno,m.referencedate,m.referencedate,m.team1,m.team2,p.id,p.points from matches m,prediction p where p.matchno=m.matchno and m.matchreference='5' and p.id='"+id2+"'")
        users = [dict(matchno=row[0],referencedate=row[1],date=row[2],team1=row[3],team2=row[4],id2=row[5],points=row[6]) for row in cursor.fetchall()]
        return(users)
    elif timestamp>referencetime5 and timestamp<referencetime6:
        cursor.execute("select m.matchno,m.referencedate,m.referencedate,m.team1,m.team2,p.id,p.points from matches m,prediction p where p.matchno=m.matchno and m.matchreference='6' and p.id='"+id2+"'")
        users = [dict(matchno=row[0],referencedate=row[1],date=row[2],team1=row[3],team2=row[4],id2=row[5],points=row[6]) for row in cursor.fetchall()]
        return(users)
    elif timestamp>referencetime6 and timestamp<referencetime7:
        cursor.execute("select m.matchno,m.referencedate,m.referencedate,m.team1,m.team2,p.id,p.points from matches m,prediction p where p.matchno=m.matchno and m.matchreference='7' and p.id='"+id2+"'")
        users = [dict(matchno=row[0],referencedate=row[1],date=row[2],team1=row[3],team2=row[4],id2=row[5],points=row[6]) for row in cursor.fetchall()]
        return(users)
    elif timestamp>referencetime7 and timestamp<referencetime8:
        cursor.execute("select m.matchno,m.referencedate,m.referencedate,m.team1,m.team2,p.id,p.points from matches m,prediction p where p.matchno=m.matchno and m.matchreference='8' and p.id='"+id2+"'")
        users = [dict(matchno=row[0],referencedate=row[1],date=row[2],team1=row[3],team2=row[4],id2=row[5],points=row[6]) for row in cursor.fetchall()]
        return(users)
    elif timestamp>referencetime8 and timestamp<referencetime9:
        cursor.execute("select m.matchno,m.referencedate,m.referencedate,m.team1,m.team2,p.id,p.points from matches m,prediction p where p.matchno=m.matchno and m.matchreference='9' and p.id='"+id2+"'")
        users = [dict(matchno=row[0],referencedate=row[1],date=row[2],team1=row[3],team2=row[4],id2=row[5],points=row[6]) for row in cursor.fetchall()]
        return(users)
    elif timestamp>referencetime9:
        cursor.execute("select m.matchno,m.referencedate,m.referencedate,m.team1,m.team2,p.id,p.points from matches m,prediction p where p.matchno=m.matchno and m.matchreference='9' and p.id='"+id2+"'")
        users = [dict(matchno=row[0],referencedate=row[1],date=row[2],team1=row[3],team2=row[4],id2=row[5],points=row[6]) for row in cursor.fetchall()]
        return(users)
    else:
        print('date not found')
def matchinput(id1,matchnumber,winner,point):
    timestamp1=datetime.datetime.now()
    matchnumber=str(matchnumber)
    point=str(point)
    id1=str(id1)
    winner=str(winner)
    database=MySQLdb.connect(DBCONN_NAME,DBUSER_NAME,DBPASSWORD,DBNAME)
    cursor=database.cursor()
    k=("update prediction set winner='"+winner+"',points="+point+",updatedatetime='"+str(timestamp1)+"' where id='"+id1+"' and matchno='"+matchnumber+"'")
    cursor.execute(k)
    database.commit()
    database.close()

def pwresetuser(username):
    try:
        error=None
        userid=username
        database=MySQLdb.connect(DBCONN_NAME,DBUSER_NAME,DBPASSWORD,DBNAME)
        cursor=database.cursor()
        query=("select id,userid,password,teamcaptain from users where userid in ('"+userid+"')")
        cursor.execute(query)
        data=cursor.fetchall()
        pwreset=[dict(id=row[0],username=row[1],password=row[2],teamcaptain=row[3]) for row in data]
        print(pwreset)
        for data in pwreset:
            null="null"
            password_temp2=data.get('password')
            id1=data.get('id')
            username1=data.get('username')
            teamcaptain1=data.get('teamcaptain')
        if pwreset==[]:
            error='User Not Present'
            return error,null,null,null
            database.close()
        else:
            characters = string.ascii_letters + string.punctuation  + string.digits
            pas = "".join(choice(characters) for x in range(randint(8, 16)))
            id1=str(id1)
            pas=str(pas)
            query2=("update users set password='"+pas+"' where id='"+id1+"'")
            cursor.execute(query2)
            database.commit()
            database.close()
            return error,pas,username1,teamcaptain1
    except Exception as e:
        null="null"
        print(str(e))
        return str(e),null,null,null
def mybids(id2):
    try:
        timestamp1=datetime.datetime.now()
        timestamp2=timestamp1.strftime("%m/%d/%Y %H:%M:%S")
        database=MySQLdb.connect(DBCONN_NAME,DBUSER_NAME,DBPASSWORD,DBNAME)
        cursor=database.cursor()
        query=("select matchno,winner,points from prediction where updatedatetime >'"+str(timestamp2)+"' and id='"+str(id2)+"'")
        cursor.execute(query)
        data=cursor.fetchall()
        bids1=[dict(matchno=row[0],winner=row[1],points=row[2]) for row in data]
        return(bids1)
    except Exception as e:
        return(e)
        
def winnerpointupdate(matchno,winner):
    error=None
    try:
        database=MySQLdb.connect(DBCONN_NAME,DBUSER_NAME,DBPASSWORD,DBNAME)
        cursor=database.cursor()
        matchno=str(matchno)
        winner=str(winner)
        query1=("update matches set winner='"+winner+"' where matchno='"+matchno+"'")
        cursor.execute(query1)
        database.commit()
        query2=("select id,winner,points from prediction where matchno='"+matchno+"'")
        cursor.execute(query2)
        data=cursor.fetchall()
        points_temp=[dict(id=row[0],winner=row[1],points=row[2]) for row in data]
        for data in points_temp:
            teamid=str(data.get('id'))
            winner1=str(data.get('winner'))
            points=int(data.get('points'))
            if points==0:
                pointsadd="-500"
                pupdate(matchno,pointsadd,teamid)
                totupdate(teamid)
            elif winner1==winner:
                pointsadd=(1*points)
                pointsadd=str(pointsadd)
                pupdate(matchno,pointsadd,teamid)
                totupdate(teamid)
            else:
                pointsadd=(points*-1)
                pointsadd=str(pointsadd)
                pupdate(matchno,pointsadd,teamid)
                totupdate(teamid)
        return(error)
    except Exception as e:
        return str(e)
    

def pupdate(matchno,pointsadd,teamid):
    database=MySQLdb.connect(DBCONN_NAME,DBUSER_NAME,DBPASSWORD,DBNAME)
    cursor=database.cursor()
    query3=("update pointsummary set match"+matchno+"='"+pointsadd+"' where id='"+teamid+"'")
    cursor.execute(query3)
    database.commit()
def totupdate(teamid):
    database=MySQLdb.connect(DBCONN_NAME,DBUSER_NAME,DBPASSWORD,DBNAME)
    cursor=database.cursor()
    query4=("Select week1,week2,week3,week4,week5,week6,week7,week8,week9,week10,match1,match2,match3,match4,match5,match6,match7,match8,match9,match10,match11,match12,match13,match14,match15,match16,match17,match18,match19,match20,match21,match22,match23,match24,match25,match26,match27,match28,match29,match30,match31,match32,match33,match34,match35,match36,match37,match38,match39,match40,match41,match42,match43,match44,match45,match46,match47,match48,match49,match50,match51,match52,match53,match54,match55,match56,match57,match58,match59,match60,match61,match62,match63,match64 from pointsummary where id='"+teamid+"'")
    cursor.execute(query4)
    data=cursor.fetchall()
    points_tot=[dict(week1=row[0],week2=row[1],week3=row[2],week4=row[3],week5=row[4],week6=row[5],week7=row[6],week8=row[7],week9=row[8],week10=row[9],match1=row[10],match2=row[11],match3=row[12],match4=row[13],match5=row[14],match6=row[15],match7=row[16],match8=row[17],match9=row[18],match10=row[19],match11=row[20],match12=row[21],match13=row[22],match14=row[23],match15=row[24],match16=row[25],match17=row[26],match18=row[27],match19=row[28],match20=row[29],match21=row[30],match22=row[31],match23=row[32],match24=row[33],match25=row[34],match26=row[35],match27=row[36],match28=row[37],match29=row[38],match30=row[39],match31=row[40],match32=row[41],match33=row[42],match34=row[43],match35=row[44],match36=row[45],match37=row[46],match38=row[47],match39=row[48],match40=row[49],match41=row[50],match42=row[51],match43=row[52],match44=row[53],match45=row[54],match46=row[55],match47=row[56],match48=row[57],match49=row[58],match50=row[59],match51=row[60],match52=row[61],match53=row[62],match54=row[63],match55=row[64],match56=row[65],match57=row[66],match58=row[67],match59=row[68],match60=row[69],match61=row[70],match62=row[71],match63=row[72],match64=row[73]) for row in data]
    for data in points_tot:
        global total
        total=sum(data.values())
    total1=str(total)
    query5=("update pointsummary set total='"+total1+"' where id='"+teamid+"'")
    timestamp1=datetime.datetime.now()
    timestamp2=str(timestamp1.strftime("%Y-%m-%d %H:%M:%S"))
    query6=("update pointsummary set updatedatetime='"+timestamp2+"'  where id='"+teamid+"'")
    cursor.execute(query5)
    cursor.execute(query6)
    database.commit()
    database.close()
def currentstanding():
    database=MySQLdb.connect(DBCONN_NAME,DBUSER_NAME,DBPASSWORD,DBNAME)
    cursor1=database.cursor()
    query=("select teamname,total,updatedatetime from pointsummary order by total DESC")
    cursor1.execute(query)
    data=cursor1.fetchall()
    custan=[dict(teamname=row[0],total=row[1],updatedatetime=row[2]) for row in data]
    database.close()
    return custan
def usr1(id1):
    try:
        database=MySQLdb.connect(DBCONN_NAME,DBUSER_NAME,DBPASSWORD,DBNAME)
        cursor1=database.cursor()
        query=("select userid,teamcaptain,member1,member2,member3,teamname from users where id='"+str(id1)+"'")
        cursor1.execute(query)
        data=cursor1.fetchall()
        usr2=[dict(userid=row[0],teamcaptain=row[1],member1=row[2],member2=row[3],member3=row[4],teamname=row[5]) for row in data]
        database.close()
        return usr2
    except Exception as e:
        return str(e)
def adminlogin1(userid,password):
    try:
        database=MySQLdb.connect(DBCONN_NAME,DBUSER_NAME,DBPASSWORD,DBNAME)
        cursor=database.cursor()
        Null='Error'
        query=("select userid,password from admin where userid in ('"+userid+"')")
        cursor.execute(query)
        data=cursor.fetchall()
        password_temp=[dict(userid=row[0],password1=row[1]) for row in data]
        for data in password_temp:
            global password8
            password8=data.get('password1')
        if password8==password:
            k="True"
            return(k)
        else:
            k="False"
            return(k)
    except Exception as e:
        k="False"
        return(k)
def WeeklyPointUpdate1(week,point):
    error=None
    try:
        week1=str(week)
        point1=str(point)
        database=MySQLdb.connect(DBCONN_NAME,DBUSER_NAME,DBPASSWORD,DBNAME)
        cursor1=database.cursor()
        query=("update pointsummary set "+week+"='"+point1+"'")
        cursor1.execute(query)
        database.commit()
        database.close()
        return(None)
    except Exception as e:
        return str(e)

def UpdateMatch1(matchnumber,team1,team2):
    error=None
    try:
        matchnumber1=str(matchnumber)
        team3=str(team1)
        team4=str(team2)
        database=MySQLdb.connect(DBCONN_NAME,DBUSER_NAME,DBPASSWORD,DBNAME)
        cursor1=database.cursor()
        query=("update matches set team1='"+team3+"',team2='"+team4+"' where matchno='"+matchnumber1+"'")
        cursor1.execute(query)
        database.commit()
        database.close()
        return(None)
    except Exception as e:
        return str(e)
        
def pwreset3(pass1,id1):
    error=None
    try:
        pass1=str(pass1)
        id1=str(id1)
        database=MySQLdb.connect(DBCONN_NAME,DBUSER_NAME,DBPASSWORD,DBNAME)
        cursor=database.cursor()
        query=("update users set password='"+pass1+"' where id='"+id1+"'")
        cursor.execute(query)
        database.commit()
        database.close()
        return error
    except Exception as e:
        error=str(e)
        print(error)
        return error
        