import csv
import codecs
import datetime
import github3


def get_repo(gh):
    repo = gh.repository('PyGithub', 'PyGithub')
    return repo


def get_all_commits(repo):
    commits = repo.commits()
    commits_list = list()
    for commit in commits:
        commits_list.append(commit)
    return commits_list


def commits_to_csv(commits_list, path, file_exists, gh):
    dict_list = list()
    for commit in commits_list:
        sha = str(commit.sha)
        message = str(commit.commit.message)
        url = str(commit.url)
        time = str(commit.commit.committer.get('date'))
        date = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
        date = date.strftime("%m/%d/%Y %I:%M:%S %p")
        tree = commit.commit.tree.to_tree().recurse().as_dict().get('tree')
        print(gh.rate_limit().get('resources').get('core').get('remaining'))
        code_size = 0
        source_files = 0
        extensions = [".py", ".sh"] 
        ''' if there is a file extension that is one letter, make sure it occurs after any other extensions that start 
         with the same letter e.g ["cpp", "c"] otherwise the code size calc will be messed up'''
        for t in tree:
            filen = t.get("path")
            hasExtension = False
            if not t.get("type") == "blob":
                continue
            for extension in extensions:
                if extension in filen:
                    hasExtension = True
                    break
            if not hasExtension:
                continue
            size = str(t.get("size"))
            if not size == "None":
                code_size += int(size)
                source_files += 1
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
            "code_size": str(code_size),
            "source_files": str(source_files)
        }
        dict_list.append(temp)
    with codecs.open(path, mode='a+', encoding='utf-8') as csv_file:
        fieldnames = ["sha", "message", "author", "date", "url", "code_size", "source_files"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for index in dict_list:
            writer.writerow(index)
