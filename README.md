# Overview:
This section includes one python file that adds new topics to repositories with a README.md, and a .json file that stores the repository data consisting it's contributors and topics

- **add_topics.py**:
  - reads data from [cloud_data.json](https://github.com/lopezjoa/TopicTest/blob/main/cloud_data.json) to validate that user input repositories do exist
  - Runs within [main.yaml](https://github.com/lopezjoa/TopicTest/blob/main/.github/workflows/main.yml)
 
## add_topics.py

### Overview:
Pulls information stored in [cloud_data.json](https://github.com/lopezjoa/TopicTest/blob/main/cloud_data.json) to add new topics to Github repositories with Github Action.

### Inputs:
-Uses a repository secret to be able to access GitHub Cloud data:
  - **JL_PAT**: Personal Access Token (PAT)
- grabs input from [main.yaml](https://github.com/lopezjoa/TopicTest/blob/main/.github/workflows/main.yml) line 42 in the following format:
  [Exisisting_Repo, New_Topic]
### Logic:
  1. looks within [main.yaml](https://github.com/lopezjoa/TopicTest/blob/main/.github/workflows/main.yml) to grab repository names and exisisting topics
  2. Loops through input to validate entered Repos and adds new Topics with Repo contained inside brackets
  3. Repos and New topics are put into a dictionary where they are passed into a loop in attempt to commit to Github
  4. Inside the loop each Repositories' new topics are appended to the existing topics
  5. The python script will then attempt to push the new topic list to the requested Github repositories and return a response code 
### Output
  - input will be validated with a response code 200 or will provide an error code
  - The validated Github repositories will now be classified with the new topics
