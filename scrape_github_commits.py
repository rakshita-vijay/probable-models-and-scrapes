import sys
import re

import requests
import bs4

def is_valid_github_url_format(url):
  """Checks if the URL string matches common GitHub URL formats."""
  https_pattern = r'^https://github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+(\.git)?(/tree/main)?$'
  ssh_pattern = r'^git@github\.com:[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+(\.git)?(/tree/main)?$'
  git_pattern = r'^git://github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+(\.git)?(/tree/main)?$'

  if re.match(https_pattern, url) or re.match(ssh_pattern, url) or re.match(git_pattern, url):
    return True
  return False

def scrape_github_commits(github_link):
  print("GitHub Link: ", github_link)

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
