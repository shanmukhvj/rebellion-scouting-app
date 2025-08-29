import webview
import csv
import os

CSV_FILE = "reefscape2025.csv"
MATCH_FILE = "current_match.txt"

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Team",
                "AutoL1","AutoL2","AutoL3","AutoL4","AutoProcessor","AutoReef",
                "TeleL1","TeleL2","TeleL3","TeleL4","TeleProcessor","TeleReef",
                "Auto","Tele","Barge","Total","Match"
            ])
    if not os.path.exists(MATCH_FILE):
        with open(MATCH_FILE,"w") as f:
            f.write("1")

class ScoutAPI:
    def __init__(self):
        self.reset()

    def reset(self):
        self.team = ""
        self.data = {
            "AutoL1":0,"AutoL2":0,"AutoL3":0,"AutoL4":0,"AutoProcessor":0,"AutoReef":0,
            "TeleL1":0,"TeleL2":0,"TeleL3":0,"TeleL4":0,"TeleProcessor":0,"TeleReef":0,
            "Auto":0,"Tele":0,"Barge":0,"Total":0
        }
        return self.get_data()

    def set_team(self, team):
        self.team = str(team)
        return self.get_data()

    def add_score(self, section, points, field):
        self.data[field] += 1
        self.data[section] += points
        self.data["Total"] = self.data["Auto"] + self.data["Tele"] + self.data["Barge"]
        return self.get_data()

    def add_barge(self, value):
        points = {"Park":2,"Shallow":6,"Deep":12}
        self.data["Barge"] = points.get(value,0)
        self.data["Total"] = self.data["Auto"] + self.data["Tele"] + self.data["Barge"]
        return self.get_data()

    def save_match(self):
        if not self.team:
            return self.get_data()
        # Read current match
        try:
            with open(MATCH_FILE) as f:
                match_number = f.read().strip()
        except:
            match_number = "1"
        # Append row
        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "Team",
                "AutoL1","AutoL2","AutoL3","AutoL4","AutoProcessor","AutoReef",
                "TeleL1","TeleL2","TeleL3","TeleL4","TeleProcessor","TeleReef",
                "Auto","Tele","Barge","Total","Match"
            ])
            writer.writerow({"Team": self.team, **self.data, "Match": match_number})
        self.reset()  # clear for next match
        return self.get_data()

    def get_data(self):
        return {
            "Auto": self.data["Auto"],
            "Tele": self.data["Tele"],
            "Barge": self.data["Barge"],
            "Total": self.data["Total"]
        }

    def get_match_number(self):
        try:
            with open(MATCH_FILE) as f:
                return int(f.read().strip())
        except:
            return 1

init_csv()
api = ScoutAPI()

scout_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>Reefscape 2025 Scouter</title>
<style>
body { margin:0; padding:0; font-family:Arial; background: linear-gradient(to right, #800000, #000066); color:white; }
.container { display:flex; flex-direction:row; height:100vh; }
.left { flex:2; padding:20px; overflow-y:auto; }
.right { flex:1; display:flex; align-items:center; justify-content:center; }
.right img { width:100%; height:100%; object-fit:cover; opacity:0.85; }
button { margin:3px; padding:8px 12px; font-weight:bold; border:none; border-radius:5px; cursor:pointer; background: rgba(255,255,255,0.2); color:white; }
button:hover { background: rgba(255,255,255,0.4); }
input { margin:5px; padding:6px; }
h2 { margin-top:20px; }
.score { font-size:18px; margin:5px 0; }
</style>
</head>
<body>
<div class="container">
  <div class="left">
    <h1>Reefscape 2025 Scouter</h1>
    <div>Current Match: <span id="currentMatch">1</span></div>
    <input id="teamInput" placeholder="Enter team number"/>
    <button onclick="setTeam()">Set Team</button>

    <h2>Autonomous</h2>
    <button onclick="add('Auto',3,'AutoL1')">L1</button>
    <button onclick="add('Auto',4,'AutoL2')">L2</button>
    <button onclick="add('Auto',6,'AutoL3')">L3</button>
    <button onclick="add('Auto',7,'AutoL4')">L4</button>
    <button onclick="add('Auto',6,'AutoProcessor')">Processor</button>
    <button onclick="add('Auto',4,'AutoReef')">Reef</button>

    <h2>Teleoperated</h2>
    <button onclick="add('Tele',2,'TeleL1')">L1</button>
    <button onclick="add('Tele',3,'TeleL2')">L2</button>
    <button onclick="add('Tele',4,'TeleL3')">L3</button>
    <button onclick="add('Tele',5,'TeleL4')">L4</button>
    <button onclick="add('Tele',6,'TeleProcessor')">Processor</button>
    <button onclick="add('Tele',4,'TeleReef')">Reef</button>

    <h2>Barge Climb</h2>
    <button onclick="barge('Park')">Park</button>
    <button onclick="barge('Shallow')">Shallow</button>
    <button onclick="barge('Deep')">Deep</button>

    <h2>Scores</h2>
    <div class="score">Autonomous: <span id="autoScore">0</span></div>
    <div class="score">Teleoperated: <span id="teleScore">0</span></div>
    <div class="score">Barge: <span id="bargeScore">0</span></div>
    <div class="score">Total: <span id="totalScore">0</span></div>

    <button onclick="saveMatch()">Save Match</button>
    <button onclick="clearInputs()">Clear Inputs</button>
  </div>
  <div class="right">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTR21NcrZSUy0Shxd8EgBPw2YtHYLcXCCiMGA&s"/>
  </div>
</div>

<script>
async function updateUI() {
    const data = await pywebview.api.get_data();
    document.getElementById("autoScore").innerText = data.Auto;
    document.getElementById("teleScore").innerText = data.Tele;
    document.getElementById("bargeScore").innerText = data.Barge;
    document.getElementById("totalScore").innerText = data.Total;
}

async function updateCurrentMatch() {
    let match = await pywebview.api.get_match_number();
    document.getElementById("currentMatch").innerText = match;
}
setInterval(updateCurrentMatch, 2000);

async function setTeam() {
    let t = document.getElementById("teamInput").value;
    if(!t){ alert("Enter team number"); return; }
    await pywebview.api.set_team(t);
    updateUI();
}

async function add(section, pts, field) {
    await pywebview.api.add_score(section, pts, field);
    updateUI();
}

async function barge(type) {
    await pywebview.api.add_barge(type);
    updateUI();
}

async function saveMatch() {
    await pywebview.api.save_match();
    updateUI();
}

async function clearInputs() {
    await pywebview.api.reset();
    updateUI();
}
</script>
</body>
</html>
"""

webview.create_window("Reefscape 2025 Scouter", html=scout_html, js_api=api)
webview.start()
