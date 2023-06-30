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
  2. Loops through input to validate existing repos with main.yamn and adds new topics within a list
  3. The new topics are then appended to the existing topics that are associated with the defined repository
  4. The python script will then attempt to add topics to the requested Github repositories and return a response code 
### Output
  - input will be validated with a response code 200 or will provide an error code
  - The validated Github repositories will now be classified with the inputted topics
