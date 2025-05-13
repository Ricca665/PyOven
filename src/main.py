import requests
import os
import sys
import subprocess
import urllib.request
import zipfile

base_api = "api.gamebanana.com/"
download_api = "https://gamebanana.com/apiv7/Mod/"
getname_api = "https://api.gamebanana.com/Core/Item/Data?itemtype=Mod&itemid="

stufftokeepin = {"Mod"}

os.chdir(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")) # enters the script directory

if not os.path.isfile("xdelta.exe"): # xdelta cli utility check
    print("Seems a dependency (Delta patcher) is not installed! Make sure you extracted the zip file correctly...")
    sys.exit()

def patch(input_file, delta_patch, output_file): # Patching function
    """Allows for patching, takes in the og data.win, the xdelta patch and the output filename"""
    subprocess.run(["xdelta.exe", "-e", "-v", "-f", "-s",  input_file, delta_patch, output_file])

def getMods(gamebanana_page_number):
    value = requests.get("https://"+base_api + "Core/List/New?page=" + str(gamebanana_page_number) + "&gameid=7692&include_updated=true&AllowedFilters?itemtype=mod")
    if value.status_code == 200: # Simple check so that we not only check for internet connection, but also if the servers are alive
        value = value.json()
        return [item_id for item_type, item_id in value if item_type == 'Mod'] # Filters out just the mods
    else:
        print("Unable to connect to gamebanana servers...")        

def getDownloadLink(mod_id):
    value = requests.get(download_api + str(mod_id) + "?_csvProperties=_aFiles")
    value = value.json()
    return value['_aFiles'][0]['_sDownloadUrl']

def getModName(mod_id):
    value = requests.get(getname_api + str(mod_id) + "&fields=name") # Filters the name of the mod
    return value.json()[0]

def unzipMod(mod_zip):
    pass

def downloadMod(download_link, mod_name):
    mod_name = mod_name.replace(" ","_")
    urllib.request.urlretrieve(getDownloadLink(download_link), mod_name)
    unzipMod(mod_name)

def main():
    page_number = 1
    while True:
        mods = getMods(page_number)
        print("Select mod to download:")
        counter = 1
        for mod in mods:
            print(f"{counter}: {getModName(mod)}")
            counter += 1
        choice = int(input("Choice: "))
        if isinstance(choice, int):
            try:
                mod_name = getModName(mods[choice-1])
                choice -= 1
            except (IndexError, ValueError):
                choice = 1
                mod_name = getModName(mods[choice])
            print(f"Downloading: {mod_name}")
            downloadMod(mods[choice], f"{mod_name}.zip")
        else:
            page_number += 1
    
if __name__ == "__main__":
    main()
