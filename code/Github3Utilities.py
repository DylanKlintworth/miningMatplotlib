import csv
import codecs
import datetime
import github3


def get_repo(gh, owner, repository):
    repo = gh.repository(owner, repository)
    return repo


def get_all_commits(repo):
    commits = repo.commits()
    commits_list = list()
    for commit in commits:
        commits_list.append(commit)
    return commits_list


def get_code_size(commits_list, extensions):
    for commit in commits_list:
        tree = commit.commit.tree.to_tree().recurse().as_dict().get('tree')
        code_size = 0
        source_files = 0
        for t in tree:
            filen = t.get("path")
            has_extension = False
            if not t.get("type") == "blob":
                continue
            for extension in extensions:
                if extension in filen:
                    has_extension = True
                    break
            if not has_extension:
                continue
            size = str(t.get("size"))
            if not size == "None":
                print(f"Path: {filen}, Size: {size}")
                code_size += int(size)
                source_files += 1
        return code_size, source_files


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
        extensions = [".css", ".cpp", ".c", ".html", ".h", ".js", ".m"]
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


def main():
    gh = github3.login()
    repo = get_repo(gh)
    commits = get_all_commits(repo)
    code_size, source_files = get_code_size(commits, [])
    print(
        f"Total Code Size: {code_size}, # Source Files {source_files}, Bytes per source file: {code_size / source_files}")


if __name__ == "__main__":
    main()
