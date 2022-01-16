
from sqlite3.dbapi2 import Date
from db import Database, DatabaseHelpers
from kickbase_api.kickbase import Kickbase
import datetime

username = "myusername" # put username here
password = "mypassword" # put password here

kickbase = Kickbase()
user, leagues = kickbase.login(username, password)
userInfo= kickbase.league_me(leagues[0])
kader = kickbase.league_user_players(leagues[0], user)
dummyPlayer = kader[0]
colNames = ["id", "firstname", "lastname", "team", "value", "trend"]
dummyCols = [dummyPlayer.id, dummyPlayer.first_name, dummyPlayer.last_name, dummyPlayer.team_id, dummyPlayer.market_value, dummyPlayer.market_value_trend]

budget = userInfo.budget
teamValue = userInfo.team_value
effectiveVal = teamValue + budget
today = datetime.date.today()
finance = [[budget, teamValue, effectiveVal, today]]

players = []
for player in kader:
    players.append([player.id, player.first_name, player.last_name, player.team_id, player.market_value, player.market_value_trend])


dbHelper = DatabaseHelpers(colNames)
sqlDict = dbHelper.getTblStructure(dummyCols)
moneyDict = {
    "id": "INTEGER PRIMARY KEY",
    "current": "REAL",
    "teamvalue": "REAL",
    "budget": "REAL",
    "date": "TEXT"
}
with Database("test.db") as db:
    db.createTbl("players", sqlDict)
    db.createTbl("finance", moneyDict)
    db.insert("players", players)
    update = db.update("players", "id")
    oldIds = [x[0] for x in update]
    ids = [x[0] for x in players]
    toDel = list(set(oldIds) - set(ids))
    db.delete("players", toDel)
    db.updateVals("players", players)
    p = db.selectAll("players")
    res = db.selectAll("finance")
    currentDate = [x[4] for x in res]
    if len(currentDate) != 0:
        currentDate = currentDate[-1]   
    if currentDate != str(today):    
        db.insert("finance", finance, False)
    else:
        print(f"Data for {today} already in database.")
    stats = db.select(f"SELECT * FROM finance ORDER BY id DESC LIMIT 2;")
    teamVal = [int(x[3]) for x in stats]
    win = teamVal[0] - teamVal[1]
    with open("kickbase.txt", "w") as file:
        file.write(f"<p>Finanzstatus alt: {str(teamVal[0])} </p>\n")
        file.write(f"<p>Finanzstatus alt: {str(teamVal[1])} </p>\n")
        file.write(f"<b>Differenz Teamwert {win} </b>\n")
        for item in p:
            t = [str(x) for x in item]
            if t[5] == str(2):
                file.write(f"<b style='color:red'>{' '.join(t[1:3])} </b> \n")
            elif t[5] == str(0):
                file.write(f"<p style='color:grey'>{' '.join(t[1:3])} </p> \n")
            else:
                file.write(f"<p style='color:green'>{' '.join(t[1:3])} </p> \n")
    
