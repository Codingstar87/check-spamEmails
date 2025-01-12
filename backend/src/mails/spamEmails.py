from fastapi import APIRouter, HTTPException, Response, status, Body,BackgroundTasks
from src.db.db import spam_emails_list,spam_domain_list
import requests

from src.models.models import spamEmail


GITHUB_LINKS = [
   
         "https://gist.githubusercontent.com/bugwrangler/69c02872dbdc5460d7251792daba7863/raw/09a7ae479aa14a07d177933990e9688e39e91630/gistfile1.txt",
         "https://raw.githubusercontent.com/tsirolnik/spam-domains-list/refs/heads/master/spamdomains.txt",
         "https://raw.githubusercontent.com/harshvardhanmalpani/Spam-List/refs/heads/master/list.md" ,
         "https://gist.githubusercontent.com/E1101/7638434ba448963f45d662158d6eca37/raw/da00895151b841e04ebbc44fd1891b48447dc411/spam_list.txt",
         "https://raw.githubusercontent.com/disposable-email-domains/disposable-email-domains/refs/heads/main/disposable_email_blocklist.conf"

]

# Scheduler for periodic tasks
# scheduler = BackgroundScheduler()
# scheduler.start()

def fetch_spem_data():
    spam_emails = set()
    spam_domains = set()

    for link in GITHUB_LINKS :
        try:
            res = requests.get(link)
            if res.status_code == 200 :
                data = res.text.strip()
                
                if "," in data :
                    entires = data.split(',')
                elif ' OR ' in data :
                    entires = data.split(' OR ')
                elif ' ' in data :
                    entires = data.split()
                else:
                    entires = data.splitlines()
                
                for entire in entires :
                    entire = entire.strip()
                    if "@" in entire :
                        spam_emails.add(entire)
                    else:
                        spam_domains.add(entire)

        except Exception as e :
            print(f"Error in fatching data from {link}: {e}" )
    
    for email in spam_emails :
        spam_emails_list.update_one({"spamEmail" : email}, {"$set": {"email": email}}, upsert=True) 
    for domain in spam_domains :
        spam_domain_list.update_one({"domain": domain}, {"$set": {"domain": domain}}, upsert=True)


