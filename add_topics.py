import json
import requests
import sys
import os



gh_base_url = "https://api.github.com/"
gh_repos_url = gh_base_url + "users/lopezjoa/repos"
gh_add_topics_url = gh_base_url + "repos/lopezjoa/"
gh_contributors_url = gh_base_url + "repos/lopezjoa/"

session = requests.Session()
token = os.getenv("JL_PAT")

access = "Bearer " + token
headers = { "Accept": "application/vnd.github+json", "Authorization": access }

def open_file(path):
    with open(path, 'r') as file:
        data = json.load(file)
    
    repo_dict = {}
    
    for entry in data:
        name = entry["name"]

        owner = entry["owner"]["login"]  # owner is a dict
        topics = entry["topics"].split(', ') if isinstance(entry["topics"], str) else entry["topics"]
        repo_dict[name] = (owner, topics)
    
    return repo_dict


def get_user_input(repos_dict):
     target_repo = input("Enter the target repo: ")
     topics = []
 # Add multiple topics to one repo instead of one
     if target_repo in repos_dict:
         while True:
             topic = input("Enter a topic (press Enter to finish): ").split(', ') #Using the .split as a delimeter for input
             if topic == "":
                 break
             topics.append(topic)
        
         return target_repo, topics
     else:
         # entered invalid repo name
         return -1, -1

def get_repo_and_topics_from_args(repos_dict):
    if len(repos_dict) < 2:
        print("Usage: add_topics.py (<repo_name>, <topic1>, <topic2>, ...")  # Changing the format to have parenthesis and commas
        sys.exit(1)

    arg = " ".join(sys.argv[1:])  # put everything after add_topics.py into a string
    print("printing arg after join", arg)
    arg = arg.replace("[", "")  # remove ( from string
    args_list = arg.split("]")  # use ) as a delimiter for each repository
    args_list = [element.strip() for element in args_list if element.strip()]  # strip spaces and filter any empty strings
    print("printing arg after split", args_list)
    repo_name = {}  # where we store repos and their topics
    for i in args_list:
        print("i ", i)
        i_list = i.split(",")  # split string into list by ,
        i_list = [element.strip() for element in i_list]  # strip spaces
        print("i list: ", i_list)
        repo_key = i_list.pop(0)  # store the first value of i_list
        print("Repo Name: " + repo_key)
        repo_name[repo_key] = []
        if repo_key in repos_dict:  # check if repo_key exists as a key in repos_dict
            for topic in i_list:
                if topic:  # check if the topic is not empty
                    repo_name[repo_key].append(topic) # add topics to repo name dictionary if it's in repo dictionary
                    print("Topics: ", repo_name[repo_key])
                else:
                    print("Error: At least one topic must be provided.")
                    sys.exit(1)
        else:
            return repo_name
    return repo_name


def add_topics(repo, new_topics, existing_topics, repo_owner):
    existing_topics = set(existing_topics) # changing to set to avoid duplicates
    for topic in new_topics:
        existing_topics.add(topic)

    existing_topics = list(existing_topics) # converting set back into a list
    if len(existing_topics) > 0:
        data = {
            "names": existing_topics
        }
        resp = session.put(gh_add_topics_url+repo+"/topics", headers=headers, json=data)
        return resp
    else:
        print("0 topics provided. Quitting.")
        sys.exit(1)
        

def test_obtained(target_repo):
    topics_url = gh_contributors_url + target_repo + "/topics"
    topics_resp = session.get(topics_url, headers=headers)
    return topics_resp

if __name__ == "__main__":
    # MODIFY THIS SO IT READS FROM LATEST REPO DATA WITH TOPICS PULLED
    repo_dict = open_file("cloud_data.json")

    repo_dict = get_repo_and_topics_from_args(repo_dict)
    # target_repo, topics = get_user_input(repo_dict)
    for target_repo, topics in repo_dict.items():
        if target_repo != -1:
            print("You wish to add the following topics to: ", target_repo)
            print(topics)
            
            existing_topics = repo_dict[target_repo][1]  # returns existing topics
            
            repo_owner = repo_dict[target_repo][0]
            add_topics_resp = add_topics(target_repo, topics, existing_topics, repo_owner)
            print("Attempted adding topics, resp code: ")
            print(add_topics_resp)
            
            topics_resp = test_obtained(target_repo)
            if topics_resp.status_code == 200:
                print("Topics after being added: ")
                print(topics_resp.json())
            else:
                print("Error obtaining latest topics for repo: ", target_repo)
                print("Error code: ", topics_resp)
        else:
            print("Repo could not be found.")
        print(repo_dict)
    
        
    while True:
        target_repo, topics = get_user_input(repo_dict)

        if target_repo != -1:
            print("You wish to add the following topics to: ", target_repo)
            print(topics)
            choice = input("Do you wish to proceed? (Y/N)")
            if choice == "Y":
                existing_topics = repo_dict[target_repo][1]  # returns existing topics
                repo_owner = repo_dict[target_repo][0]
                add_topics(target_repo, topics, repo_dict, existing_topics, repo_owner)
            else:
                cancel = input("Restarting. Enter 'quit' to abort program.")
                if cancel == "quit":
                    break
        else:
            cancel = input("Repo could not be found, please enter 'quit' to abort or press anything else to continue.")
            if cancel == "quit":
                    break
