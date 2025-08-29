import webview
import csv
import os

CSV_FILE = "reefscape2025.csv"
MATCH_FILE = "current_match.txt"

class CaptainAPI:
    def __init__(self):
        if not os.path.exists(MATCH_FILE):
            with open(MATCH_FILE,"w") as f:
                f.write("1")
        self.timer_seconds = 135
        self.timer_running = False

    def search_team(self, team):
        team = str(team)
        matches = []
        with open(CSV_FILE, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Team"] == team:
                    matches.append(row)
        if not matches:
            return {"matches": [], "average": {}}

        avg = {}
        numeric_fields = ["AutoL1","AutoL2","AutoL3","AutoL4","AutoProcessor","AutoReef",
                          "TeleL1","TeleL2","TeleL3","TeleL4","TeleProcessor","TeleReef",
                          "Auto","Tele","Barge","Total"]
        for field in numeric_fields:
            values = [int(m[field]) for m in matches if m[field].isdigit()]
            avg[field] = round(sum(values)/len(values),2) if values else 0

        return {"matches": matches, "average": avg}

    def set_match_number(self, match):
        with open(MATCH_FILE,"w") as f:
            f.write(str(match))
        return int(match)

    def get_match_number(self):
        try:
            with open(MATCH_FILE) as f:
                return int(f.read())
        except:
            return 1

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>Captain Dashboard</title>
<style>
body { margin:0; padding:0; font-family:Arial; background: linear-gradient(to right, #800000, #000066); color:white; }
.container { display:flex; flex-direction:row; height:100vh; }
.left { flex:2; padding:20px; overflow-y:auto; }
.right { flex:1; display:flex; align-items:center; justify-content:center; }
.right img { width:100%; height:100%; object-fit:cover; opacity:0.85; }
input, button { padding:10px; font-size:16px; margin:5px; }
table { border-collapse: collapse; width:100%; margin-top:15px; background: rgba(0,0,0,0.3);}
th, td { border:1px solid white; padding:6px; text-align:center; }
#timer { font-size:24px; margin:5px; }
</style>
</head>
<body>
<div class="container">
  <div class="left">
    <h1>Captain Dashboard</h1>

    <h2>Match Timer</h2>
    <div id="timer">02:15</div>
    <button onclick="startTimer()">Start</button>
    <button onclick="stopTimer()">Stop</button>
    <button onclick="resetTimer()">Reset</button>

    <h2>Current Match</h2>
    <input id="matchNumber" placeholder="Enter match #"/>
    <button onclick="updateMatch()">Set Match</button>

    <h2>Search Team</h2>
    <input id="teamInput" placeholder="Enter team number"/>
    <button onclick="searchTeam()">Search</button>
    <div id="results"></div>
  </div>
  <div class="right">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTR21NcrZSUy0Shxd8EgBPw2YtHYLcXCCiMGA&s"/>
  </div>
</div>

<script>
let totalTime = 135;
let timerInterval;

function updateTimerDisplay() {
    let m = Math.floor(totalTime/60);
    let s = totalTime % 60;
    document.getElementById("timer").innerText = (m<10?'0':'')+m+":"+(s<10?'0':'')+s;
}

function startTimer(){
    if(timerInterval) clearInterval(timerInterval);
    timerInterval = setInterval(()=>{
        if(totalTime>0){ totalTime--; updateTimerDisplay(); } 
        else clearInterval(timerInterval);
    },1000);
}
function stopTimer(){ clearInterval(timerInterval); }
function resetTimer(){ totalTime=135; updateTimerDisplay(); }

async function updateMatch(){
    let match = document.getElementById("matchNumber").value;
    if(!match){ alert("Enter match number"); return; }
    await pywebview.api.set_match_number(match);
}

async function searchTeam(){
    let team = document.getElementById("teamInput").value;
    if(!team){ alert("Enter team number"); return; }
    let res = await pywebview.api.search_team(team);
    renderResults(res);
}

function renderResults(res){
    let html = "";
    if(res.matches.length === 0){
        html = "<p>No matches found</p>";
    } else {
        html += "<h3>Averages (EPA)</h3><table><tr>";
        for(let k in res.average) html += "<th>"+k+"</th>";
        html += "</tr><tr>";
        for(let k in res.average) html += "<td>"+res.average[k]+"</td>";
        html += "</tr></table>";

        html += "<h3>Individual Matches</h3><table><tr>";
        for(let k in res.matches[0]) html += "<th>"+k+"</th>";
        html += "</tr>";
        res.matches.forEach(m=>{
            html += "<tr>";
            for(let k in m) html += "<td>"+m[k]+"</td>";
            html += "</tr>";
        });
        html += "</table>";
    }
    document.getElementById("results").innerHTML = html;
}
</script>
</body>
</html>
"""

api = CaptainAPI()
webview.create_window("Captain Dashboard", html=html, js_api=api)
webview.start()
