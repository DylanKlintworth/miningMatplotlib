import datetime
import copy
import csv
import github as gh
import codecs

def get_repo(github):
    """
    Returns the Repository object representation of the matplotlib repository

        Parameters:
            github (github.Github): The main GitHub object representation
    """
    repo = github.get_repo("matplotlib/matplotlib")
    return repo


def get_all_issues(repo):
    """
    Returns a PaginatedList of Issue objects (open/closed) sorted by when they were created

        Parameters:
                repo (github.Repository): The repository selected to get the issues of
    """
    issues = repo.get_issues(state="all", sort="created")
    return issues


def get_issues_over_time(issues, query):
    """
    Return a dictionary in which each key represents a timeframe (day, week, month, year, 5 years)
    and holds the value of a list of issues that have been created within that timeframe

        Parameters:
                issues (PaginatedList of Issues): the repositories' issues
                query (str): The state to be queries e.g "open"/"closed"

    """
    time = {
        "day": list(),
        "week": list(),
        "month": list(),
        "year": list(),
        "five_years": list()
    }
    date = datetime.datetime.today()
    day = date - datetime.timedelta(days=1)
    week = date - datetime.timedelta(weeks=1)
    month = date - datetime.timedelta(weeks=4)
    year = date - datetime.timedelta(weeks=52)
    five_years = date - datetime.timedelta(weeks=(52 * 5))
    for issue in issues:
        if issue.state == query:
            created_at = issue.created_at
            if created_at >= day:
                time["day"].append(issue)
            elif day >= created_at >= week:
                time["week"].append(issue)
            elif week >= created_at >= month:
                time["month"].append(issue)
            elif month >= created_at >= year:
                time["year"].append(issue)
            elif year >= created_at >= five_years:
                time["five_years"].append(issue)
    return time


def get_issues_over_time_count(issues_over_time):
    cp = copy.deepcopy(issues_over_time)
    cp["day"] = len(cp["day"])
    cp["week"] = len(cp["week"])
    cp["month"] = len(cp["month"])
    cp["year"] = len(cp["year"])
    cp["five_years"] = len(cp["five_years"])
    return cp


def issues_to_csv(issues, path):
    issues_list = list()
    for issue in issues:
        closed = str(issue.closed_at)
        comment_count = str(issue.comments)
        created = str(issue.created_at)
        number = str(issue.number)
        state = str(issue.state)
        title = str(issue.title)
        temp = {
            "title": title,
            "number": number,
            "state": state,
            "created": created,
            "closed": closed,
            "comment_count": comment_count
        }
        issues_list.append(temp)
    with codecs.open(path, mode='w', encoding='utf-8') as csv_file:
        fieldnames = ["title", "number", "state", "created", "closed", "comment_count"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in issues_list:
            writer.writerow(i)
