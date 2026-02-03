import json
import requests
import csv
import os

if not os.path.exists("data"):
    os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lsttoken)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct


# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def get_author_info(lsttokens, repo):
    ipage = 1
    ct = 0

    #Create CSV file
    filename = 'data/rootbeer_author_touches.csv'
    fileCSV = open(filename, 'w', newline='', encoding='utf-8')
    writer = csv.writer(fileCSV)
    # Get header row
    writer.writerow(['SrcFileName', 'Author', 'Date'])

    # Is there a way to read from the csv file and get the commit info? Work on that on Sunday

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break

            # Fix Excemption at the end
            if not jsonCommits:
                break

            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']

                #Get commit info from the shaObject
                commitAuthor = shaObject['commit']['author']['name']
                commitDate = shaObject['commit']['author']['date']


                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)

                #print(sha)


                #print("Loop")

                # might need to check for files in shaDetails first?
                # filesjson = shaDetails['files']
                if 'files' in shaDetails:
                    for filenameObj in shaDetails['files']:
                        commitfilename = filenameObj['filename']
                        #EDIT:
                        # Source files languages: Java, Kotlin, C++, C, and CMake
                        srcExtensions = ('.java', '.kt', '.cpp', '.c', '.h')

                        #print("1st If")

                        # only collect files with correct extensions
                        if commitfilename.endswith(srcExtensions):
                            # file has correct extension
                            writer.writerow([commitfilename, commitAuthor, commitDate])
                            print(f"Commit in {commitfilename} by {commitAuthor} on {commitDate} saved into CSV file.")


            ipage += 1
    except Exception as e:
        print("Error when extracting commit data")
    finally:
        fileCSV.close()
# GitHub repo
repo = 'scottyab/rootbeer'

lstTokens = ["lol"]

get_author_info(lstTokens, repo)
print("All data has been proecssed!")