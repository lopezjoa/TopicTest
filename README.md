# Overview:
This Repository includes a Python script titled [add_topics.py](https://github.com/lopezjoa/TopicTest/blob/test-safety-controls/add_topics.py) that takes input from the user to add new topics to specific Github Repositories. This script reads data from a .json file called 'cloud_data.json', which holds information about about existing repositories and modifies the topics of these repositories. The script is designed to be ran through Github Actions in the [main.yaml](https://github.com/lopezjoa/TopicTest/blob/main/.github/workflows/main.yml) file.
- **add_topics.py**:
  - reads data from [cloud_data.json](https://github.com/lopezjoa/TopicTest/blob/main/cloud_data.json) to validate that user input repositories do exist
  - Script is ran in [main.yaml](https://github.com/lopezjoa/TopicTest/blob/main/.github/workflows/main.yml) through Github Actions
  - Updates existing repositories with new topics
 
## add_topics.py

### Overview:
Pulls information stored in [cloud_data.json](https://github.com/lopezjoa/TopicTest/blob/main/cloud_data.json) to add new topics to Github repositories with Github Action.

### Inputs:
This script requires several input
- **JL_PAT**: Personal Access Token (PAT) that's sotred as a repository secret
- Command-line arguments in the following format: [Existing_Repo, New_Topic, New_Topic2] [Existing_Repo2, New_Topic]
  - Topics should only contain lowercase letters 
  - Empty Topics will be invalidated
- An existing [cloud_data.json](https://github.com/lopezjoa/TopicTest/blob/main/cloud_data.json) file in the same directory as the script.
  - File should hold information about the repositories
  
### Logic:
  1. Opens [main.yaml](https://github.com/lopezjoa/TopicTest/blob/main/.github/workflows/main.yml) and loads data into a Python dictionary
  2. Command line Arguments are then passed to create a new dictionary of the target repositories and their new topics
  3. Each target repository is then interated over to send a request to Github to add the new topics to the Repository
      - If an error occurs during the process, an error message will be printed and the program will be terminated
  4. Once the Target's topics have been added the script will verify that topics have been commited successfully with a response code 200
  
### Output
  - The script will either add the new topics to each Repository successfullly, or it will terminate with an error code
  - If the script was successful, the Github repositories will now have the new topics updated
