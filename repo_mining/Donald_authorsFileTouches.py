import json
import requests
import csv
import os
from dateutil import parser

lstTokens = ["fake_token_name"]
repo = 'scottyab/rootbeer'

# read source files
source_files = set()
with open('data/file_rootbeer.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) 
    for row in reader:
        source_files.add(row[0])

# get author and date info for these files
rows_data = [] 

def github_auth(url, lsttoken, ct):
    ct = ct % len(lstTokens)
    headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
    req = requests.get(url, headers=headers)
    return json.loads(req.content), ct + 1

ct = 0
ipage = 1

print("Collecting author data... this might take a minute...")

while True:
    url = f'https://api.github.com/repos/{repo}/commits?page={ipage}&per_page=100'
    commits, ct = github_auth(url, lstTokens, ct)
    if not commits:
        break
        
    for commit in commits:
        # get author, date from project
        try:
            author_name = commit['commit']['author']['name']
            date_str = commit['commit']['author']['date']
            
            # Parse date to get week number
            dt = parser.parse(date_str)
            week_num = dt.strftime("%Y-%U") # Year-Week format
            
            sha = commit['sha']
            sha_url = f'https://api.github.com/repos/{repo}/commits/{sha}'
            details, ct = github_auth(sha_url, lstTokens, ct)
            
            for fileObj in details['files']:
                fname = fileObj['filename']
                if fname in source_files:
                    rows_data.append([fname, author_name, date_str, week_num])
        except Exception as e:
            continue
            
    print(f"Processed Page {ipage}")
    ipage += 1


with open('data/authors_touches.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Filename", "Author", "Date", "Week"])
    writer.writerows(rows_data)

print("Done! Data saved to data/authors_touches.csv")