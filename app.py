from flask import Flask, render_template, send_file
from mcstatus import MinecraftServer
import requests, base64, json, shutil, os

IP = "5.83.168.21:12600"
server = MinecraftServer.lookup(IP)

def server_status():
    return server.status()
    

def players_online():
    query = server.query()
    players = query.players.names
    return players

def get_skins_for_players(players):
    for player in players:
        
        if not os.path.exists(os.path.join(os.getcwd(), "skins", f"{player}.png")):

            url = f"https://api.mojang.com/users/profiles/minecraft/{player}"
            data = requests.get(url).json()

            url = f"https://sessionserver.mojang.com/session/minecraft/profile/{data['id']}"
            data = requests.get(url).json()

            player_object = json.loads(base64.b64decode(data['properties'][0]['value']).decode('utf-8'))
            skin_url = player_object['textures']['SKIN']['url']

            request = requests.get(skin_url, stream=True)
            if request.status_code == 200:
                with open(os.path.join(os.getcwd(), "skins", f"{player_object['profileName']}.png"), 'wb') as file:
                    request.raw.decode_content = True
                    shutil.copyfileobj(request.raw, file)
        else:
            print("player skin already downloaded ...")


app = Flask(__name__)

@app.route("/")
def index():
    players = players_online()
    #players = ['LooNieFu', 'BreakThisBlock', "Pfalle", "Dinnerbone"]
    get_skins_for_players(players)
    data = server_status()
    return render_template('index.html', players=players, ping=str(data.latency), version=data.version.name, description=data.description['extra'][0]['text'])

@app.route("/skin/<player>")
def skin(player):

    path = os.path.join(os.getcwd(), "skins", f"{player}.png")
    return send_file(path, mimetype="image/png")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)