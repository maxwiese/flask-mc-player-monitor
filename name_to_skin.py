import requests, base64, json, shutil, os

def name_to_uuid(name):

    url = f"https://api.mojang.com/users/profiles/minecraft/{name}"
    data = requests.get(url).json()

    return data['id']

def id_to_skin(id):
    
    url = f"https://sessionserver.mojang.com/session/minecraft/profile/{id}"
    data = requests.get(url).json()

    player_object = json.loads(base64.b64decode(data['properties'][0]['value']).decode('utf-8'))
    skin_url = player_object['textures']['SKIN']['url']

    request = requests.get(skin_url, stream=True)
    if request.status_code == 200:
        with open(os.path.join(os.getcwd(), f"{player_object['profileName']}.png"), 'wb') as file:
            request.raw.decode_content = True
            shutil.copyfileobj(request.raw, file)


if __name__ == "__main__":
    id_to_skin(name_to_uuid("BreakThisBlock"))