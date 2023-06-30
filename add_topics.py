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
        topics = entry["topics"]
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
def check_str(myStr):
    open = "["
    close = "]"
    stack = []
    for i in myStr:   # check each character in the string for a [ or a ]
        if i == open: 
            stack.append(i) # if character equals [ add to stack list
        elif i == close:    # check previous character for [
            if len(stack) > 0 and open == stack[len(stack)-1]:
                stack.pop() # remove characters from stack list
            else: # if unable to find [ in stack list then brackets are not contained
                print("Items are not contained within the brackets")
                sys.exit(1)
    if len(stack) == 0:
        return 
    else: # if [ is still in list then items are not contained
        print("Items are not contained within the brackets")
        sys.exit(1)	    
def get_repo_and_topics_from_args(repos_dict):
    if len(repos_dict) < 2:
        print("Usage: add_topics.py (<repo_name>, <topic1>, <topic2>, ...")  # Changing the format to have parenthesis and commas
        sys.exit(1)
    arg = " ".join(sys.argv[1:])  # put everything after add_topics.py into a string
    bracket_only = bool(re.search(r"[({})]", args))
    if bracket_only == False:
        print("Please only use bracket")
        sys.exit(1)
    check_str(args)
    print("printing arg after join", arg)
    arg = arg.replace("[", "")  # remove ( from string
    args_list = arg.split("]")  # use ) as a delimiter for each repository
    args_list = [element.strip() for element in args_list if element.strip()]  # strip spaces and filter any empty strings
    print("printing arg after split", args_list)
    repo_dict = {}  # where we store repos and their topics
    for i in args_list:
        i_list = i.split(",")  # split string into list by ,
        for item in i_list:
            if " " in item:
                print("items are not being separated by , ")
                sys.exit(1)
        i_list = [element.strip() for element in i_list]  # strip spaces
        repo_key = i_list.pop(0)  # store the first value of i_list
        print("Repo Name: " + repo_key)
        repo_dict[repo_key] = []
        if repo_key in repos_dict:  # check if repo_key exists as a key in repos_dict
            for topic in i_list:
                if bool(re.search("[a-z]", args)) == False:
                    print("items must be in all lowercase")
                    sys.exit(1)
                if topic:  # check if the topic is not empty
                    repo_dict[repo_key].append(topic) # add topics to repo name dictionary if it's in repo dictionary
                else:
                    print("Error: At least one topic must be provided.")
                    sys.exit(1)
        else:
            return repo_dict
    return repo_dict

def add_topics(repo, new_topics, existing_topics, repo_owner):
    existing_topics = set(existing_topics) # changing to set to avoid duplicates
    for topic in new_topics:
        if topic: #if topic isn't empty
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
    existing_repo_dict = open_file("cloud_data.json")

    repo_dict = get_repo_and_topics_from_args(existing_repo_dict)
    # target_repo, topics = get_user_input(repo_dict)
    for target_repo, topics in repo_dict.items():
        if target_repo != -1:
            print("You wish to add the following topics to: ", target_repo)
            print(topics)
            existing_topics = existing_repo_dict[target_repo][1]  # returns existing topics
            
            repo_owner = repo_dict[target_repo][0]
            add_topics_resp = add_topics(target_repo, topics, existing_topics, repo_owner)
            if add_topics_resp != 200:
                
                print("Attempted adding topics, resp code: ")
                print(add_topics_resp)
                print(add_topics_resp.json())
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
    
        
    # while True:
    #     target_repo, topics = get_user_input(repo_dict)

    #     if target_repo != -1:
    #         print("You wish to add the following topics to: ", target_repo)
    #         print(topics)
    #         choice = input("Do you wish to proceed? (Y/N)")
    #         if choice == "Y":
    #             existing_topics = repo_dict[target_repo][1]  # returns existing topics
    #             repo_owner = repo_dict[target_repo][0]
    #             add_topics(target_repo, topics, repo_dict, existing_topics, repo_owner)
    #         else:
    #             cancel = input("Restarting. Enter 'quit' to abort program.")
    #             if cancel == "quit":
    #                 break
    #     else:
    #         cancel = input("Repo could not be found, please enter 'quit' to abort or press anything else to continue.")
    #         if cancel == "quit":
    #                 break
