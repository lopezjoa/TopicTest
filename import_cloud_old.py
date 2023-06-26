import requests
import json
import time
import os

gh_base_url = "https://api.github.com/"
# gh_base_url = "https://api.github.com/lopezjoa/TopicTest/tree/main"

gh_repos_url = gh_base_url + "repos/lopezjoa/repos"
gh_langs_url = "repos/lopezjoa/"

session = requests.Session()
token = os.getenv("JL_PAT")

access = "Bearer " + token
headers = { "Accept": "application/vnd.github+json", "Authorization": access }

class Repo(object):
    name = None
    langs = None

    def __init__(self, name, langs):
        self.name = name
        self.langs = langs

def get_langs(name):
    lang_url = gh_langs_url + name + "/languages"
    lang_resp = session.get(lang_url, headers=headers)
    return lang_resp

def printToFile(data):
    data_pp = json.dumps(data, indent=2)

    directory = os.getcwd()
    # filepath = directory + "/Data-Imports/GitHub/Outputs/"
    # Will write to /gh-repo/scannability/inputs/ for our scannability analysis
    f = open("repos-output.json", "w")
    f.write(data_pp)
    f.close()

def get_repos():
    
    querystring = {"type":"all", "per_page":"100"}

    first_page = session.get(gh_repos_url, params=querystring, headers=headers)
    yield first_page

    next_page = first_page
    while get_next_page(next_page) is not None:
        try:
            next_page_url = next_page.links['next']['url']
            next_page = session.get(next_page_url, headers=headers)
            yield next_page
        except KeyError:
            print("No more github pages")
            break


def get_next_page(page):
    return page if page.headers.get('link') != None else None

# ---------- Begin Main ----------

repo_list = []
for page in get_repos():
    resp = page.json()
    start = time.time()
    for repo in resp:
        try:
            name = repo['name']
            print("repo name: ", name)
            langs = get_langs(name)
            try:
                if langs.status_code == 200:
                    repo_details = Repo(name, langs.json())
                    repo_list.append(repo_details.__dict__)
                else:
                    print("Lang response code not 200")
            except:
                print("Error with repo name: ", name)
        except:
            print("Error with repo: ", repo)
        print("________________________________________________________")

    end = time.time()
    elapsed = end - start
    print(str(page) + " -- done a repo page process -- time: " + str(elapsed))

print("Number of repos: " + str(len(repo_list)))
printToFile(repo_list)
