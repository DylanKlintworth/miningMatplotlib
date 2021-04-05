import github as gh


def get_repo(github):
    """Returns the Repository object representation of the matplotlib repository"""
    repo = github.get_repo("matplotlib/matplotlib")
    return repo


def get_all_issues(repo):
    """Returns a PaginatedList of Issue objects (open/closed) sorted by when they were created"""
    issues = repo.get_issues(state="all", sort="created")
    return issues


def get_issues_over_time(issues):
    """Return a dictionary in which each key represents a timeframe (day, week, month, year, 5 years)
    and holds the value of a list of issues that have been created within that timeframe"""
    time = {
        "day": list(),
        "week": list(),
        "month": list(),
        "year": list(),
        "5_years": list()
    }
