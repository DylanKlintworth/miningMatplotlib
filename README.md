# miningMatplotlib
## FILE LOCATIONS
###### All files types are located in the directory associated with their extension
###### Charts are located within Tableau workbooks and Excel workbooks
###### csv data includes that for commits and issues
###### The presentation included in the root directory includes all charts and findings, including answers to research questions and general insights
## DEPENDENCIES 
###### pip install openpyxl
###### pip install pandas
###### pip install PyGithub
###### pip install github3.py

## GETTING STARTED WITH PYGITHUB 
###### from github import Github
*First create a Github instance using an access token:* 
###### g = Github("access_token")
*Then play with your Github objects:*
###### repo = g.get_repo("matplotlib/matplotlib")

## GETTING STARTED WITH GITHUB3 
###### from github3 import login
*First create a Github instance using an access token:* 
###### g = github3.login("username", "access_token")

## WHEN CREATING PERSONAL ACCESS TOKEN
###### Go to github.com/settings/tokens
###### Click on Generate new token
###### Select public_repo 
###### Copy token into this line in the code's main function:
> g = Github("token")

## Included GITHUB3 Utilities
###### repo = get_repo(github3.login()) - gets matplotlib repo
###### commits_list = get_all_commits(repo) - gets list of all commits for matplotlib
###### commits_to_csv(commits_list, path, file_exists) - makes csv of given commits (disclaimer, uses many API calls)
