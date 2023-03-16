import requests
import json
import os
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

N = "\n" #universal new line
R = "\033[1;31m" #universal red font
W = "\033[1;0m" #universal white font
C = "\033[1;36m" #universal cyan font
B = "\033[1m" #universal bold style
U = "\033[4m" #universal underline style
D = "\033[0m" #universal default style

HP_KEY = os.getenv('hp_key')

#clears terminal and prints header
os.system("cls")
print(f"{C}{B}{U}Skyblock Death Count{D}{N}")

#default requests.get function
def get_info(call):
    r = requests.get(call)
    return r.json()

#asks user for minecraft username and retrieves associated UUID via mojang API, returns error if not found
def uuid_retriever():
    while True:
        username = input(f"{B}Enter Minecraft username:{D} ")
        try:
            mjng_pckg = get_info(f"https://api.mojang.com/users/profiles/minecraft/{username}")
            uuid = mjng_pckg["id"]
            return username, uuid
        except:
            print(f"{N}{R}Error: User '{username}' not found.{W}{N}")

#uses mojang UUID and user-inputted skyblock profile name to retrieve the profile id, returns errors if profile name is not found or if server sends back an error
def profile_id_retriever():
    username, uuid = uuid_retriever()
    
    hp_data = get_info(f"https://api.hypixel.net/player?key={HP_KEY}&uuid={uuid}")

    if hp_data["success"] == True:
        while True:
            p_id = None
            p_name = input(f"{N}{B}Enter SkyBlock Profile Fruit Name:{D} ")

            for i in hp_data["player"]["stats"]["SkyBlock"]["profiles"]:
                if p_name.capitalize() == hp_data["player"]["stats"]["SkyBlock"]["profiles"][i]["cute_name"]:
                    p_id = str(i)
                    break
            else:
                print(f"{N}{R}Error: Profile '{p_name}' not found.{W}")       
                
            if p_id != None:
                break

        return username, uuid, p_id                                                                    
       
    if hp_data["success"] == False:
        print(f"{R}Error: {str(hp_data['cause'])}{W}")

#finds all profile data from hypixel API and looks for death count from desired profile using profile ID from profile_id_retriever()
def stats_retriever():
    _, uuid, p_id = profile_id_retriever()

    sb_data = get_info(f"https://api.hypixel.net/skyblock/profiles?key={HP_KEY}&uuid={uuid}")
    no_of_profiles = len(sb_data["profiles"])

    for i in range(no_of_profiles): #sorts through list of profiles and looks for matching profile ID, then saves the index of that profile 
        if sb_data["profiles"][i]["profile_id"] == p_id:
            lst_index = i

    try: 
        death_count = sb_data["profiles"][lst_index]["members"][uuid]["death_count"]
        print(f"{N}{C}Death Count: {B}{death_count}{D}{W}{N}")
    except:
        print(f"{N}{C}{B}No recorded deaths on profile.{D}{W}{N}")
    
stats_retriever()
