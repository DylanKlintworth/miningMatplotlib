# miningMatplotlib

## requirements 
###### pip install openpyxl
###### pip install pandas
###### pip install PyGithub

## GETTING STARTED WITH PYGITHUB 
###### from github import Github
*First create a Github instance using an access token:* 
###### g = Github("access_token")
*Then play with your Github objects:*
###### repo = g.get_repo("matplotlib/matplotlib")


## WHEN CREATING PERSONAL ACCESS TOKEN
###### Go to github.com/settings/tokens
###### Click on Generate new token
###### Select public_repo 
###### Copy token into this line in the code's main function:
> g = Github("token")



