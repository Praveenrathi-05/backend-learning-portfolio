import requests, time, os, re, json
from datetime import date


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"API call took {end - start:.2f} seconds")
        return result
    return wrapper


class GitHubProfile:
    def __init__(self, username):
        self.username = username
        self.data = self._fetch()

    @timer
    def _fetch(self):
        try:
            response = requests.get(f"https://api.github.com/users/{self.username}")
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return None

    def public_repos(self):
        if self.data:
            return self.data['public_repos']

    def followers(self):
        if self.data:
            return self.data['followers']

    def bio(self):
        if self.data:
            return self.data['bio']


class RepoScanner:
    def __init__(self, path):
        self.path = path

    def count_python_files(self):
        count = 0
        for _, _, filenames in os.walk(self.path):
            for file in filenames:
                if file.endswith(".py"):
                    count += 1
        return count

    def find_todos(self):
        matches = []
        for root, _, filenames in os.walk(self.path):
            for filename in filenames:
                if filename.endswith(".py"):
                    with open(os.path.join(root, filename), "r") as file:
                        for line in file:
                            match = re.findall(r"TODO|FIXME", line)
                            if len(match) != 0:
                                matches.append((filename, line.strip()))
        return matches

    def count_functions_defined(self):
        count = 0
        for root, _, filenames in os.walk(self.path):
            for filename in filenames:
                if filename.endswith(".py"):
                    with open(os.path.join(root, filename), "r") as file:
                        match = len(re.findall(r"def ", file.read()))
                        count += match
        return count


class PortfolioReport:
    def __init__(self, profile, scanner):
        self.profile = profile
        self.scanner = scanner

    def generate_summary(self):
        # Guard at the source: refuse to build a summary at all if the
        # GitHub fetch failed, rather than silently baking a None into it.
        if not self.profile.data:
            return None

        return {
            'public repos': self.profile.public_repos(),
            'python files': self.scanner.count_python_files(),
            'TODO count': len(self.scanner.find_todos())
        }

    def save_report(self, filename):
        summary = self.generate_summary()
        if summary:
            today = date.today()
            report = {
                'date': today.isoformat(),
                'summary': summary
            }
            with open(filename, "w") as file:
                json.dump(report, file, indent=4)
            return "Report Saved"
        return "Report not saved: GitHub data unavailable."

    def load_previous_report(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                previous_summary = data['summary']
                current_summary = self.generate_summary()

                # Defense in depth: guard again here too, in case a report
                # saved before this fix existed still has a None in it.
                if current_summary is None:
                    return None
                previous_public_repos = previous_summary['public repos']
                if previous_public_repos is None:
                    return None

                current_public_repos = current_summary['public repos']
                public_repos_report = (
                    f"Public repos: {previous_public_repos} → {current_public_repos} "
                    f"({current_public_repos - previous_public_repos:+})"
                )

                previous_python_files = previous_summary['python files']
                current_python_files = current_summary['python files']
                python_files_report = (
                    f"Python files: {previous_python_files} → {current_python_files} "
                    f"({current_python_files - previous_python_files:+})"
                )

                previous_todo_count = previous_summary['TODO count']
                current_todo_count = current_summary['TODO count']
                todo_count_report = (
                    f"TODO count: {previous_todo_count} → {current_todo_count} "
                    f"({current_todo_count - previous_todo_count:+})"
                )

                return f"{public_repos_report}\n{python_files_report}\n{todo_count_report}"
        except FileNotFoundError:
            return None


scanner = RepoScanner("/Users/praveen/Desktop/backend-learning-portfolio")
profile = GitHubProfile("Praveenrathi-05")

portfolio_report = PortfolioReport(profile, scanner)

while True:
    print("1.Fetch/refresh GitHub profile\n2.Run repository scan\n3.Generate and save report\n"
          "4.Compare with previous report\n5.Exit")
    try:
        task = int(input("Enter Task Number: "))
    except ValueError:
        print("Type a Number")
    else:
        if task == 1:
            profile.data = profile._fetch()
            print("GitHub profile refreshed.")
        elif task == 2:
            print(f"Python files: {scanner.count_python_files()}")
            print(f"TODO/FIXME count: {len(scanner.find_todos())}")
            print(f"Functions defined: {scanner.count_functions_defined()}")
        elif task == 3:
            print(portfolio_report.save_report("report.json"))
        elif task == 4:
            comparison = portfolio_report.load_previous_report("report.json")
            if comparison:
                print(comparison)
            else:
                print("No previous report found.")
        elif task == 5:
            break
        else:
            print("Not a valid task")
