import sys
import re
import os
import requests
import bs4
import lxml
import urllib.robotparser
import base64

token = os.environ.get("REPO_SCRAPING_TOKEN")
if not token:
  raise ValueError("REPO_SCRAPING_TOKEN environment variable not set. Please set it as a secret in your GitHub repository. If in command line/terminal, run the command: export REPO_SCRAPING_TOKEN=YOUR_TOKEN ")
headers = {"Authorization": f"token {token}"}

def is_repo_link(url):
  https_pattern = r'^https://github\.com/([a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38})/[a-zA-Z0-9_.-]+(\.git)?(/tree/[a-zA-Z0-9_.-]+)?$'
  ssh_pattern = r'^git@github\.com:([a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38})/[a-zA-Z0-9_.-]+(\.git)?(/tree/[a-zA-Z0-9_.-]+)?$'
  git_pattern = r'^git://github\.com/([a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38})/[a-zA-Z0-9_.-]+(\.git)?(/tree/[a-zA-Z0-9_.-]+)?$'

  if re.match(https_pattern, url) or re.match(ssh_pattern, url) or re.match(git_pattern, url):
    return True
  return False

def is_handle_link(url):
  https_pattern = r'^https://github\.com/([a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38})$'
  ssh_pattern = r'^git@github\.com:([a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38})$'
  git_pattern = r'^git://github\.com/([a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38})$'

  if re.match(https_pattern, url) or re.match(ssh_pattern, url) or re.match(git_pattern, url):
    return True
  return False

def is_valid_github_url_format(url):
  r_link = is_repo_link(url)
  h_link = is_handle_link(url)

  if (r_link and not h_link) or (not r_link and h_link):
    return True
  else:
    return False

def extract_github_username(url):
  https_pattern = r'^https://github\.com/([a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38})/?'
  ssh_pattern = r'^git@github\.com:([a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38})/?'
  git_pattern = r'^git://github\.com/([a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38})/?'

  if re.match(https_pattern, url):
    return re.search(https_pattern, url).group(1)

  elif re.match(ssh_pattern, url):
    return re.match(ssh_pattern, url).group(1)

  elif re.match(git_pattern, url):
    return re.search(git_pattern, url).group(1)

  else:
    raise ValueError("Username associated with repository couldn't be extracted :(")

def get_public_repos(username):
  rp = urllib.robotparser.RobotFileParser()
  rp.set_url("https://github.com/robots.txt")
  rp.read()
  if rp.can_fetch("*", f"https://github.com/{username}"):
    pass
  else:
    return []

  repos = []
  page = 1

  while True:
    url = f"https://api.github.com/users/{username}/repos"
    params = {"per_page": 100, "page": page}
    response = requests.get(url, params=params)

    if response.status_code != 200:
      print(f"Error: {response.status_code} - {response.json().get('message')}")
      break

    data = response.json()
    if not data:  # No more repos
      break

    for repo in data:
      repos.append(repo["name"])

    page += 1

  return repos

def get_readme_text(repo_owner, url):
  api_url = f"https://api.github.com/repos/{repo_owner}/readme"

  token = os.environ.get("REPO_SCRAPING_TOKEN")
  if not token:
    raise ValueError("REPO_SCRAPING_TOKEN environment variable not set. Please set it as a secret in your GitHub repository. If in command line/terminal, run the command: export REPO_SCRAPING_TOKEN=YOUR_TOKEN ")
  headers = {"Authorization": f"token {token}"}

  resp = requests.get(url, headers=headers)

  if resp.status_code == 200:
    data = resp.json()
    # README content is base64-encoded under 'content' key
    content = base64.b64decode(data['content']).decode('utf-8')
  else:
    raise ValueError(f"Could not fetch README. Status code: {resp.status_code}")

  return content

def check_readmes_to_see_if_length_is_legit(repo_owner, url, repo_list):
  if is_repo_link(url):
    # then do specific stuff and only look through that repo
    readme_text = get_readme_text(repo_owner, url)
    if len(readme_text) < 150:
      return False
    else:
      return True

  else is_handle_link(url):
    # find specific repo that matches project desc based on name or readme by agentic ai
    r_list = repo_list
    for ind, repo in enumerate(r_list):
      repo_url = f"https://api.github.com/repos/{repo_owner}/{repo}"
      readme_text = get_readme_text(repo_owner, repo_url)
      if len(readme_text) < 150:
        r_list.pop(ind)

def scrape_github_commits(url):
  gh_username = extract_github_username(url)

  token = os.environ.get("REPO_SCRAPING_TOKEN")
  if not token:
    raise ValueError("REPO_SCRAPING_TOKEN environment variable not set. Please set it as a secret in your GitHub repository. If in command line/terminal, run the command: export REPO_SCRAPING_TOKEN=YOUR_TOKEN ")
  headers = {"Authorization": f"token {token}"}

  repo_list = get_public_repos(gh_username)
  if len(repo_list) == 0:
    raise ValueError("No repos to show in GitHub")

  length_legit_or_not = check_readmes_to_see_if_length_is_legit(gh_username, url, repo_list)





  """files = requests.get(url, headers=headers)

  # files = requests.get(url)
  soup = bs4.BeautifulSoup(files.text, 'lxml')
  print(soup.prettify())
  content_div = soup.find_all(class="react-directory-truncate", href=True)
  print(content_div)

  i have the specific github repository and i need to scrape the commits"""

if __name__ == "__main__":
  if len(sys.argv) != 2:
    github_link = "invalid"
    while not is_valid_github_url_format(github_link):
      github_link = input("Please enter a valid GitHub repository link: ")
    scrape_github_commits(github_link)

  elif len(sys.argv) == 2:
    github_link = sys.argv[1]
    while not is_valid_github_url_format(github_link):
      github_link = input("Please enter a valid GitHub repository link: ")
    scrape_github_commits(github_link)
