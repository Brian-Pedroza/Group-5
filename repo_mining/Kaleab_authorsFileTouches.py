import requests
import csv
import os
from datetime import datetime

repo = "scottyab/rootbeer"

# use env token (safe)
my_token = os.getenv("GITHUB_TOKEN")
if not my_token:
    print("GITHUB_TOKEN not set")
    exit(1)

headers = {"Authorization": f"Bearer {my_token}"}

# read files from script 1 output
files_to_check = []
with open("data/file_rootbeer.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        files_to_check.append(row["Filename"])

# find project start date (oldest commit)
page = 1
project_start = None

while True:
    url = f"https://api.github.com/repos/{repo}/commits?per_page=100&page={page}"
    r = requests.get(url, headers=headers)
    commit_list = r.json()

    if not commit_list:
        break

    last_item = commit_list[-1]
    project_start = datetime.strptime(last_item["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ")
    page += 1

if not project_start:
    print("Could not determine project start date")
    exit(1)

# output csv
out_path = "data/rootbeer_authors_touches.csv"
output_file = open(out_path, "w", newline="", encoding="utf-8")
writer = csv.writer(output_file)
writer.writerow(["Week", "Filename", "Author", "Date"])

for filename in files_to_check:

    page = 1
    while True:
        url = f"https://api.github.com/repos/{repo}/commits?path={filename}&per_page=100&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Error:", response.status_code, filename)
            break

        commit_list = response.json()
        if not commit_list:
            break

        for item in commit_list:
            date_str = item["commit"]["author"]["date"]
            clean_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

            week_num = (clean_date - project_start).days // 7

            # use GitHub login if available, else fallback to commit name
            if item.get("author") and item["author"]:
                author_name = item["author"].get("login", item["commit"]["author"]["name"])
            else:
                author_name = item["commit"]["author"]["name"]

            writer.writerow([week_num, filename, author_name, date_str])

        page += 1

    print("Finished processing", filename)

output_file.close()
print("Done! Wrote:", out_path)
