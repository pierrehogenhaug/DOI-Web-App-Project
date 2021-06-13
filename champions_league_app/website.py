from flask import Flask, render_template, url_for, flash, redirect, request, Blueprint, request, session
from datetime import timedelta
import pandas as pd
import sqlite3

app = Flask(__name__)

theList = []


conn = sqlite3.connect('letsgo.db', check_same_thread=False)

data = pd.read_csv('skrt.csv')
df = pd.DataFrame(data, columns= ['MATCHID','MATCHDATE','COUNTRY','LEAGUE','SEASON','HOME_TEAM',\
    'AWAY_TEAM','FTR','FTHG','FTAG','A_COR','H_COR','A_FL','H_FL','A_RC','H_RC'])

cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS CLDATA(\
    MATCHID integer PRIMARY KEY,\
    MATCHDATE DATE,\
    COUNTRY varchar(30),\
    LEAGUE varchar(20),\
    SEASON varchar(20),\
    HOME_TEAM varchar(20),\
    AWAY_TEAM varchar(20),\
    FTR varchar(20),\
    FTHG varchar(20),\
    FTAG varchar(3),\
    A_COR varchar(20),\
    H_COR varchar(20),\
    A_FL varchar(20),\
    H_FL varchar(20),\
    A_RC varchar(20),\
    H_RC varchar(20))')

for row in df.itertuples():
    cursor.execute('''
                INSERT OR IGNORE INTO CLDATA (MATCHID,MATCHDATE,COUNTRY,LEAGUE,SEASON,HOME_TEAM,
    AWAY_TEAM,FTR,FTHG,FTAG,A_COR,H_COR,A_FL,H_FL,A_RC,H_RC)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''', (
                row.MATCHID,
                row.MATCHDATE,
                row.COUNTRY,
                row.LEAGUE,
                row.SEASON,
                row.HOME_TEAM,
                row.AWAY_TEAM,
                row.FTR,
                row.FTHG,
                row.FTAG,
                row.A_COR,
                row.H_COR,
                row.A_FL,
                row.H_FL,
                row.A_RC,
                row.H_RC))


conn.commit()

@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/BELGIUM")
def BELGIUM():
	return render_template("BELGIUM.html")

@app.route("/about")
def about():
    return render_template("login.html")

'''
@app.route("/admin")
def admin():
	return redirect(url_for("whereyougoing"))
'''

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        input_team = request.form["team"]
        input_result = request.form["result"]
        input_Goals = request.form["goals"]
        theList.append(user)
        return redirect(url_for("user", team = input_team, result = input_result, Goals = input_Goals))
    else:
        cursor.execute("SELECT DISTINCT HOME_TEAM FROM CLDATA UNION SELECT DISTINCT AWAY_TEAM FROM CLDATA")
        front_data = cursor.fetchall()
        #cursor.close()
        return render_template("login.html", table = front_data, length = len(front_data))

@app.route("/<team>/<result>/<Goals>")
def user(team,result,Goals):
    #usr = theList[-1]
    
    print('Result', result)
    print('Goals', Goals)
    print('Team',team)
    cursor = conn.cursor()
    
    if team == 'All':
        if result == 'Win' or result == 'Loss':
            cursor.execute(f"SELECT *, (FTAG + FTHG) as goals FROM CLDATA \
            WHERE (FTR = 'H' OR FTR = 'A')\
            AND ( goals >= {Goals})")

        if result == 'Draw':
            cursor.execute(f"SELECT *, (FTAG + FTHG) as goals FROM CLDATA \
            WHERE FTR = 'D'\
            AND ( goals >= {Goals})")

#f"SELECT *, FTAG + FTHG AS goals FROM CLDATA \
#            WHERE FTR = 'D'\
#            AND goals < '{Goals}'")

    else:
        if result == 'Win':
            cursor.execute(f"SELECT *, (FTAG + FTHG) as goals FROM CLDATA \
            WHERE (HOME_TEAM = '{team}'\
            AND FTR = 'H'\
            AND FTHG >= {Goals})\
            OR (AWAY_TEAM = '{team}'\
            AND FTR = 'A'\
            AND FTAG >= {Goals})")

        if result == 'Loss':
            cursor.execute(f"SELECT * , (FTAG + FTHG) as goals FROM CLDATA \
            WHERE (HOME_TEAM = '{team}'\
            AND FTR = 'A'\
            AND FTHG >= {Goals})\
            OR (AWAY_TEAM = '{team}'\
            AND FTR = 'H'\
            AND FTAG >= {Goals})")
        if result == 'Draw':
            cursor.execute(f"SELECT *, (FTAG + FTHG) as goals FROM CLDATA \
            WHERE (HOME_TEAM = '{team}'\
            AND FTR = 'D'\
            AND FTHG >= '{Goals}')\
            OR (AWAY_TEAM = '{team}'\
            AND FTR = 'D'\
            AND FTAG >= {Goals})")
        if result == 'All':
            cursor.execute(f"SELECT *, (FTAG + FTHG) as goals FROM CLDATA \
            WHERE (HOME_TEAM = '{team}' AND FTHG >= {Goals})\
            OR (AWAY_TEAM = '{team}' AND FTAG >= {Goals})")


            


#        if location == 'A':
#            cursor.execute(f"SELECT * FROM CLDATA \
#            WHERE AWAY_TEAM = '{team}'\
#            AND FTR = '{result}'\
#            AND FTAG < '{Goals}'")

    all_data = cursor.fetchall()
    #cursor.execute(f"SELECT * FROM {all_data}")
    #new_data = cursor.fetchall()
    #cursor.close()
    return render_template('DENMARK.html', all_data=all_data, length = len(all_data), team=team)


if __name__ == "__main__":
    app.run(debug = True)

