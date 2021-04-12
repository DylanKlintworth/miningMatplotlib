
import datetime, copy, csv
from github import Github # pip install PyGithub
import pandas as pd # pip install pandas 
# don't need to import openpyxl, but need to install it to use to_excel pandas function 
# pip install openpyxl

'''
GETTING STARTED WITH PYGITHUB 

from github import Github
# First create a Github instance using an access token: 
g = Github("access_token")
# Then play with your Github objects:
repo = g.get_repo("matplotlib/matplotlib")

WHEN CREATING PERSONAL ACCESS TOKEN
Go to github.com/settings/tokens
Click on Generate new token
Select public_repo 
Copy token into code below 
'''

def main():
    '''
    Runs the main functions 
    '''
    start  = datetime.datetime.now()
    g      = Github("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")
    repo   = get_repo(g)

    # WORKING WITH ISSUES, uncomment to run
    # warning: will use up API calls if you want to run both commits and issues at the same time 
    # issues = get_all_issues(repo)
    # get_issues_over_time(issues) 

    # WORKING WITH COMMITS 
    commits = get_all_commits(repo)
    commit_iterator(commits)

    end    = datetime.datetime.now()
    print(f"Completed in: {end-start}")
        
def get_repo(tokenized_github):
    """
    Returns the Repository object representation of the matplotlib repository

        Parameters:
            github (github.Github): The main GitHub object representation
    """
    repo = tokenized_github.get_repo("matplotlib/matplotlib")
    return repo


def get_all_issues(repo):
    """
    Returns a PaginatedList of Issue objects (open/closed) sorted by when they were created

        Parameters:
                repo (github.Repository): The repository selected to get the issues of
    """
    issues = repo.get_issues(state="all", sort="created")
    return issues

def get_all_commits(repo):
    """
    Returns a PaginatedList of Issue objects (open/closed) sorted by when they were created

        Parameters:
                repo (github.Repository): The repository selected to get the issues of
    """
    commits = repo.get_commits()
    return commits

def commit_iterator(commits):
    """
    Sends information obtained from API to a xlsx file 

        Parameters:
            commits (PaginatedList of commits): the repositories' issues
        Returns:
            None, instead, prints out xlsx

    """
    
    all_commits = pd.DataFrame()

    for c in commits[2000:3000]:
        sha = c.sha 
        status = c.stats 
        files = c.files 
        len_files = len(files)
        commit_info = c.commit 
        date = commit_info.author.date
        author = commit_info.author.name 
        message = commit_info.message
        parents = commit_info.parents # list 
        tree_url = commit_info.tree.url 

        tree_tree = commit_info.tree.tree
        total_size = 0
        for item in tree_tree:
            path = item.path 
            size = item.size if item.size != None else 0
            total_size += size 

        temp = {
            "Sha": sha, 
            "Status": status,
            "Number of Files": len_files, 
            "Date": date, 
            "Author": author, 
            "Message": message,
            "Tree URL" : tree_url, 
            "Total Size" : total_size
        }
        # Making a one row dataframe of the current issue's information 
        temp_df = pd.DataFrame(temp, index=[0])
        # adding the current issue to all issues dataframe 
        all_commits = all_commits.append(temp_df, ignore_index=True, sort=False)
    
    all_commits.to_excel("matplotlib_commits_information_2000.xlsx", index=False)  


def get_issues_over_time(issues):
    """
    Sends information obtained from API to a xlsx file 

        Parameters:
            issues (PaginatedList of Issues): the repositories' issues
        Returns:
            None, instead, prints out xlsx

    """

    issue_columns = ["Issue ID", "Title", "Body", "User", "State","Created At", "Assignees", "Closed At", "Closed By", "Updated At", "Number of Comments", "Labels", "Milestone Title", "Milestone Number"]
    all_issues = pd.DataFrame()

    for issue in issues[:3000]: #only get the first one hundred open issues 
        # getting information from API
        issue_id = issue.id # int 
        title = issue.title # str
        body = issue.body # string 
        user = issue.user.login 
        state = issue.state 
        created_at = issue.created_at # datetime.datetime
        assignees = issue.assignees # list
        assignees = len(assignees) # get only length of list 
        closed_at = issue.closed_at # datetime.datetime
        closed_by = issue.closed_by # NamedUser or None 
        if closed_by != None:
            closed_by = issue.closed_by.login # NamedUser
        updated_at = issue.updated_at # datetime.datetime
        no_of_comments = issue.comments # int 
        new_label_format = []
        for label in issue.labels: # check to see if any labels exist 
            new_label_format.append(label.name)
        labels = ", ".join(new_label_format)
        
        if issue.milestone != None:
            milestone_title = issue.milestone.title # string
            milestone_number = issue.milestone.number # int or None
        else: 
            milestone_title = "" # string
            milestone_number = None # int or None
        # Making a dict from the information
        temp_dict = make_issue_dict(issue_id, title, body, user, state, created_at, assignees, closed_at, closed_by, updated_at, no_of_comments, labels, milestone_title, milestone_number)
        # Making a one row dataframe of the current issue's information 
        temp_df = pd.DataFrame(temp_dict, columns=issue_columns, index=[0])
        # adding the current issue to all issues dataframe 
        all_issues = all_issues.append(temp_df, ignore_index=True, sort=False)


        # sending information to CSV file
    all_issues.to_excel("matplotlib_issues_information_v3000.xlsx", index=False)    
    print("--- Printed to Excel file ---")


def make_issue_dict(issue_id, title, body, user, state, created_at, assignees, closed_at, closed_by, updated_at, no_of_comments, labels, milestone_title, milestone_number):
    '''
    Create dictionary of values obtained from API 
    Params:
        "Issue ID": str
        "Title": str, 
        "Body": str, 
        "User": str,
        "State": str,
        "Created At": datetime.datetime, 
        "Assignees": int, 
        "Closed At": datetime.datetime, 
        "Closed By": str, or None 
        "Updated At": datetime.datetime, 
        "Number of Comments": int, 
        "Labels": str, 
        "Milestone Title": str, or None
        "Milestone Number": int or None
    Returns: 
        dict 
    '''
    return {
        "Issue ID": issue_id, 
        "Title": title, 
        "Body": body, 
        "User": user, 
        "State": state, 
        "Created At": created_at, 
        "Assignees": assignees, 
        "Closed At": closed_at, 
        "Closed By": closed_by, 
        "Updated At": updated_at, 
        "Number of Comments": no_of_comments, 
        "Labels": labels, 
        "Milestone Title": milestone_title, 
        "Milestone Number": milestone_number
    }

# invoke main 
main()