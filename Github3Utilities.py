import csv
import codecs
import datetime
import github3


def get_repo(gh):
    repo = gh.repository('matplotlib', 'matplotlib')
    return repo


def get_all_commits(repo):
    commits = repo.commits()
    commits_list = list()
    for commit in commits:
        commits_list.append(commit)
    return commits_list


def commits_to_csv(commits_list, path, file_exists):
    dict_list = list()
    for commit in commits_list:
        sha = str(commit.sha)
        message = str(commit.commit.message)
        url = str(commit.url)
        time = str(commit.commit.committer.get('date'))
        date = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
        date = date.strftime("%m/%d/%Y %I:%M:%S %p")
        if commit.author:
            author = str(commit.author.login)
        else:
            author = "N/A"
        temp = {
            "sha": sha,
            "message": message,
            "author": author,
            "date": date,
            "url": url
        }
        dict_list.append(temp)
    with codecs.open(path, mode='a+', encoding='utf-8') as csv_file:
        fieldnames = ["sha", "message", "author", "date", "url"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for index in dict_list:
            writer.writerow(index)


if __name__ == "__main__":
    gh = github3.login()  # enter uname/passwd as arguments
    repo = get_repo(gh)
    commits = get_all_commits(repo)
