import json
import requests
import csv
import os
import urllib.parse

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# Load file list from CollectFiles.py
def load_files_from_csv(file_list_csv):
    files = []
    try:
        with open(file_list_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                files.append(row['Filename'].strip())
    except Exception as e:
        print(f"Error reading file list CSV: {e}")
    return files

# Source file filtering helpers
def is_source_file(filename):
    source_extensions = ('.java', '.kt', '.c', '.cpp', '.h')
    return filename.lower().endswith(source_extensions)

# Collect (Filename, Author, Date) for each source file
def collect_authors_file_touches(lsttokens, repo, file_list_csv):
    ct = 0  # token counter

    # Output CSV
    fileOutput = 'repo_mining/data/authors_file_touches_rootbeer.csv'
    fileCSV = open(fileOutput, 'w', newline='', encoding='utf-8')
    writer = csv.writer(fileCSV)
    writer.writerow(["Filename", "Author", "Date"])  # Header row

    try:
        # Load filenames from the adapted CollectFiles.py output
        all_files = load_files_from_csv(file_list_csv)

        # Keep only source files
        source_files = []
        for f in all_files:
            if is_source_file(f):
                source_files.append(f)
        
        # For each source file, ask GitHub: "Which commits touched this file?"
        for i in range(len(source_files)):
            filename = source_files[i]

            ipage = 1  # page counter (same naming idea as countfiles)

            while True:
                spage = str(ipage)

                # GitHub API: list commits filtered by path
                commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?path=' + filename + '&page=' + spage + '&per_page=100'

                jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

                # if GitHub returns a dict error object, stop this file
                if type(jsonCommits) == dict:
                    if 'message' in jsonCommits:
                        print("GitHub API message for " + filename + ": " + str(jsonCommits['message']))
                        break

                # break out of the while loop if there are no more commits in the pages
                if len(jsonCommits) == 0:
                    break

                # record each commit as a "touch"
                for commitObj in jsonCommits:
                    author_name = commitObj['commit']['author']['name']
                    commit_date = commitObj['commit']['author']['date']

                    writer.writerow([filename, author_name, commit_date])
                    print("Recorded: " + filename + " by " + author_name)

                ipage += 1

    except:
        print("Error receiving data")
        exit(0)

    finally:
        fileCSV.close()

    print("\nDone! Check " + fileOutput)


# RUN SCRIPT
if __name__ == "__main__":
    repo = 'scottyab/rootbeer'
    lstTokens = ["github_pat_11AUS642I0ZU9GRsaLtNB3_w8pxJbEHgr2YlLFyzpghcJRRB"]
    file_list_csv = 'repo_mining/data/file_rootbeer.csv'

    collect_authors_file_touches(lstTokens, repo, file_list_csv)
