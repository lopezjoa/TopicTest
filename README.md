# Overview:
This repository includes a Python script titled [add_topics.py](https://github.com/lopezjoa/TopicTest/blob/test-safety-controls/add_topics.py) that takes input from the user to add new topics to specific GitHub repositories. This script reads data from a .Json file called [cloud_data.json](https://github.com/lopezjoa/TopicTest/blob/main/cloud_data.json), which holds information about about existing repositories and modifies the topics of these repositories. The script can be run through GitHub Actions with the [main.yaml](https://github.com/lopezjoa/TopicTest/blob/main/.github/workflows/main.yml) file or in a terminal using command-line arguments. 
- **add_topics.py**:
  - Reads data from [cloud_data.json](https://github.com/lopezjoa/TopicTest/blob/main/cloud_data.json) to validate that user input repositories do exist.
  - Script is run in [main.yaml](https://github.com/lopezjoa/TopicTest/blob/main/.github/workflows/main.yml) through GitHub Actions.
  - Uses GitHub commit to add new topics to the specified repositories
 
## add_topics.py

### Overview:
Pulls information stored in [cloud_data.json](https://github.com/lopezjoa/TopicTest/blob/main/cloud_data.json) to add new topics to GitHub repositories with GitHub Action or with a terminal command-line.

### Inputs:
- **Personal Access Token (PAT)**: stored as a repository secret. This token is used to authenticate with GitHub. If you intend to use this script in a different repository, you'll need to create a new personal access token with the appropriate permission for accessing and modifying repository data.
  -  You will only be able to modify the repositories that the token's owner has access to. It won't be able to alter repositories owned by others unless the owner of the token has been given write access to those repositories.
- Command-line arguments in the following format:
    ` [Existing_Repo, new_topic, new_topic2] [existing_Repo2, new_topic].`
  - Topics should only contain lowercase letters.
  - Empty topics will be invalidated.
- An existing [cloud_data.json](https://github.com/lopezjoa/TopicTest/blob/main/cloud_data.json) file in the same directory as the script.
  - File should hold information about the repositories.

### Bad Inputs:
 - Using command-line arguments that do not follow the specified format will result in an error.
 - Running the script without providing a personal access token.
 - Using non-existing repository names. 
 - Providing an empty string or a string with spaces as a topic. `[Existing_Repo, , new_topic2] [existing_Repo2, new topic]`
 - Providing a topic with uppercase letters. `[Existing_Repo, NEW_Topic, New_Topic2]`
 - Using brackets other than square brackets for command-line arguments. `(Existing_Repo, new_topic, new_topic2) `
 - Using special characters in topics. `[Existing_Repo, new_topic!, new_topic##]`


### Logic:
  1. The script starts by opening the [cloud_data.json](https://github.com/lopezjoa/TopicTest/blob/main/cloud_data.json) and loading its data into a Python dictionary.
  2. Command-line arguments are then passed from [main.yaml](https://github.com/lopezjoa/TopicTest/blob/main/.github/workflows/main.yml) to create a new dictionary of the target repositories and their new topics.
  3. The script validates each repository and topic. If any repository or topic is invalid, the script throws an error and exits
  4. Once all inputs have been validated, Each target repository is then iterated over to send a request to GitHub to add the new topics to the existing repository.
      - If an error occurs during the process, an error message will be printed and the program will be terminated.
  5. Once the target's topics have been added, the script will send a GET request to GitHub for each repository to confirm that the new topics were added succesfully.
  
### Output
  - The script will either add the new topics to each repository successfullly, or it will terminate with an error code.
  - If the script was successful, the GitHub repositories will now have the new topics updated.
