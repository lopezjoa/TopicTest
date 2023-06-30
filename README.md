# Overview:
This section includes one python file that adds new topics to repositories with a README.md, and a .json file that stores the repository data consisting it's contributors and topics

- **add_topics.py**:
  - reads data from [cloud_data.json](https://github.com/lopezjoa/TopicTest/blob/main/cloud_data.json) to validate that user input repositories do exist
  - Script is ran in [main.yaml](https://github.com/lopezjoa/TopicTest/blob/main/.github/workflows/main.yml) through Github Actions
  - Classifies existing repositories with new topics
 
## add_topics.py

### Overview:
Pulls information stored in [cloud_data.json](https://github.com/lopezjoa/TopicTest/blob/main/cloud_data.json) to add new topics to Github repositories with Github Action.

### Inputs:
-Uses a repository secret to be able to access GitHub Cloud data:
- **JL_PAT**: Personal Access Token (PAT)
- Executes python script with command input from [main.yaml](https://github.com/lopezjoa/TopicTest/blob/main/.github/workflows/main.yml) line 42
- Please edit input with the currect format: [Existing_Repo, New_Topic, New_Topic2] [Existing_Repo2, New_Topic]
- topics should only contain lowercase letters in order to receive a 200 response code
- Empty Topics will be invalidated
  
### Logic:
  1. looks within [main.yaml](https://github.com/lopezjoa/TopicTest/blob/main/.github/workflows/main.yml) to grab repository names and exisisting topics
  2. Loops through input to validate entered repositories that exist in [cloud_data.json](https://github.com/lopezjoa/TopicTest/blob/main/cloud_data.json)
  3. New topics are then added to a new dictionary with the repositories as a primary key 
  4. The new dictionary is then passed into a loop where each repository attempts to commit to Github
  5. Inside the loop each Repositories' new topics are verified and then appended 
  6. The python script will then attempt to push the new topic list to the requested Github repositories and return a response code
### Output
  - input will be validated with a response code 200 and pushed or will provide an error code
  - The validated Github repositories will now be classified with the new topics
