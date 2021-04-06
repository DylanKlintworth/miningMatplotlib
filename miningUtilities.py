
import datetime, copy, csv
from github import Github # pip install PyGithub
import pandas as pd # pip install pandas 



'''
GETTING STARTED WITH PYGITHUB 

from github import Github
# First create a Github instance using an access token: 
g = Github("access_token")
# Then play with your Github objects:
repo = g.get_repo("matplotlib/matplotlib"):

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
    g      = Github("token")
    repo   = get_repo(g)
    issues = get_all_issues(repo)
    get_issues_over_time(issues) 
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

def get_issues_over_time(issues):
    """
    Sends information obtained from API to a CSV file 

        Parameters:
            issues (PaginatedList of Issues): the repositories' issues
        Returns:
            None, instead, prints out csv 

    """
    # time = {
    #     "day": list(),
    #     "week": list(),
    #     "month": list(),
    #     "year": list(),
    #     "five_years": list()
    # }
    # date = datetime.datetime.today()
    # day = date - datetime.timedelta(days=1)
    # week = date - datetime.timedelta(weeks=1)
    # month = date - datetime.timedelta(weeks=4)
    # year = date - datetime.timedelta(weeks=52)
    # five_years = date - datetime.timedelta(weeks=(52 * 5))
    issue_columns = ["Issue ID", "Title", "Body", "User", "State","Created At", "Assignees", "Closed At", "Closed By", "Updated At", "Number of Comments", "Labels", "Milestone Title", "Milestone Number"]
    all_issues = pd.DataFrame()

    for issue in issues: #only get the first one hundred open issues 
        # getting information from API
        issue_id = issue.id # int 
        title = issue.title # str
        body = issue.body # string 
        user = issue.user.login 
        state = issue.state 
        created_at = issue.created_at # datetime.datetime
        assignees = [] # list 
        for assignee in issue.assignees:
            assignees.append(assignee.login)
        assignees = ", ".join(assignees)
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

        # # doing some date math 
        # if created_at >= day:
        #     time["day"].append(issue)
        # elif day >= created_at >= week:
        #     time["week"].append(issue)
        # elif week >= created_at >= month:
        #     time["month"].append(issue)
        # elif month >= created_at >= year:
        #     time["year"].append(issue)
        # elif year >= created_at >= five_years:
        #     time["five_years"].append(issue)

        # sending information to CSV file
    all_issues.to_csv("matplotlib_issues_information.csv", index=False)    
    print("--- Printed to CSV file ---")


# def get_issues_over_time_count(issues_over_time):
#     cp = copy.deepcopy(issues_over_time)
#     cp["day"] = len(cp["day"])
#     cp["week"] = len(cp["week"])
#     cp["month"] = len(cp["month"])
#     cp["year"] = len(cp["year"])
#     cp["five_years"] = len(cp["five_years"])
#     return cp

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
        "Assignees": str, 
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