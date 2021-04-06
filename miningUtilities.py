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
<<<<<<< HEAD
            writer.writerow(i)


def get_all_commits(repo):
    commits = repo.get_commits()
    return commits


def commits_to_csv(commits, path, file_exists):
    commits_list = list()
    for commit in commits:
        sha = commit.sha
        commit_info = commit.commit
        if commit.author:
            author = str(commit.author.login)
        else:
            author = "None"
        date = str(commit_info.author.date)
        file_count = str(len(commit.files))
        message = commit_info.message
        total = str(commit.stats.total)
        tree_tree = commit_info.tree.tree
        total_size = 0
        for item in tree_tree:
            size = item.size if item.size is not None else 0
            total_size += size
        temp = {
            "sha": sha,
            "author": author,
            "date": date,
            "message": message,
            "total": total,
            "file_count": file_count,
            "total_size": total_size
        }
        commits_list.append(temp)
    with codecs.open(path, mode='a+', encoding='utf-8') as csv_file:
        fieldnames = ["sha", "author", "date", "message", "total", "file_count", "total_size"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for index in commits_list:
            writer.writerow(index)


if __name__ == "__main__":
    g = github.Github()
    repo = get_repo(g)
    commits = get_all_commits(repo)

=======
            writer.writerow(i)
>>>>>>> 1fde134ad440fc885fee0536501c33577ee9329a
