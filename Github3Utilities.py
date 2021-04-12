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
        tree = commit.commit.tree.to_tree().recurse().as_dict().get('tree')
        code_size = 0
        for t in tree:
            size = str(t.get('size'))
            if not size == "None":
                code_size += int(size)
            else:
                continue
        if commit.author:
            author = str(commit.author.login)
        else:
            author = "N/A"
        temp = {
            "sha": sha,
            "message": message,
            "author": author,
            "date": date,
            "url": url,
            "code_size": code_size
        }
        dict_list.append(temp)
    with codecs.open(path, mode='a+', encoding='utf-8') as csv_file:
        fieldnames = ["sha", "message", "author", "date", "url", "code_size"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for index in dict_list:
            writer.writerow(index)