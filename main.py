import os, json, requests, subprocess
import write_regionInfo
from colorama import Fore, Style
from clint.textui import progress


def change_conf(cf):
    config_path = os.environ["APPDATA"] + f"\\{cf}\\"

    rfile = open(config_path+"config.json", "r")
    js = json.loads(rfile.read())
    rfile.close()
    js["serverURL"] = "https://amongusvoice.ga:8000/"
    wfile = open(config_path+"config.json", "w")
    wfile.writelines(json.dumps(js))
    wfile.close()

def w_region():
    path = os.environ["APPDATA"] + "\\..\\LocalLow\\Innersloth\\Among Us\\"
    write_regionInfo.write_file("UGD Server", "194.124.41.128")
    os.replace("regionInfo.dat", path + "regionInfo.dat")

def check_crewlink():
    b_path = os.environ["APPDATA"] + "\\..\\Local\\Programs\\bettercrewlink"
    b_t = os.path.isdir(b_path)
    c_path = os.environ["APPDATA"] + "\\..\\Local\\Programs\\crewlink"
    c_t = os.path.isdir(c_path)
    return {"c": c_t, "b": b_t}

def download(url, path, name):
    print("Downloading: " + name)
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()
    print("Done")

def install(what):
    if what == "b":
        if os.path.isfile("BetterCrewlinkInstaller.exe") == False:
            url = json.loads(requests.get("https://api.github.com/repos/OhMyGuus/BetterCrewLink/releases").text)[0]["assets"][0]["browser_download_url"]
            download(url, "BetterCrewlinkInstaller.exe", "BetterCrewlink")
        print("Installing BetterCrewlink")
        p = subprocess.Popen(["BetterCrewlinkInstaller.exe"])
        p.wait()
        p = subprocess.call(["taskkill", "/IM", "Better-CrewLink.exe"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        print("Done")
    if what == "c":
        if os.path.isfile("CrewlinkInstaller.exe") == False:
            url = json.loads(requests.get("https://api.github.com/repos/ottomated/CrewLink/releases").text)[0]["assets"][0]["browser_download_url"]
            download(url, "CrewlinkInstaller.exe", "Crewlink")
        print("Installing Crewlink")
        p = subprocess.Popen(["CrewlinkInstaller.exe"])
        p.wait()
        subprocess.call(["taskkill", "/IM", "CrewLink.exe"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        print("Done")
        


def start():
    print("Checking for Crewlink:")
    sc = check_crewlink()
    if sc["c"]:
        print(Fore.GREEN + " Crewlink: Installed")
    else:
        print(Fore.RED + " Crewlink: not Installed")
    if sc["b"]:
        print(Fore.GREEN + " BetterCrewlink: Installed")
    else:
        print(Fore.RED + " BetterCrewlink:  not Installed")
    print(Style.RESET_ALL)


    print("Would you like to install BetterCrewlink (1), Crewlink (2) or skip (0)")
    i = input("[0, 1, 2]: ")
    try:
        i = int(i)
        if int(i) == 0:
            print("Skip")
        elif int(i) == 1:
            install("b")
        elif int(i) == 2:
            install("c")
    except:
        print("Skip")
    
    print("Would you like to add the custom server to Crewlink ?")
    i = input("[y/n]: ")
    if i == "y":
        sc = check_crewlink()
        print("Changing to custom Server")
        if sc["b"]:
            change_conf("bettercrewlink")
        if sc["c"]:
            change_conf("crewlink")
    
    print("Would you like to change to the custom server in AmongUs ?")
    i = input("[y/n]: ")
    if i == "y":
        print("Changing to custom AmongUs server")
        w_region()
    input("press any key to exit ...")

        
if __name__ == "__main__":
    start()

