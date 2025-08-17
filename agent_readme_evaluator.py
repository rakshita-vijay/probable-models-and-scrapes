# agentic ai that will evaluate readmes

import importlib.util

import sys
# Check Python version compatibility
if not (sys.version_info >= (3, 10) and sys.version_info < (3, 14)):
  print("Error: CrewAI requires Python >=3.10 and <3.14")
  print(f"Your Python version: {sys.version}")
  sys.exit(1)

import warnings
warnings.filterwarnings('ignore')

import os
from crewai import Agent, Task, Crew, LLM

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
  raise ValueError("GOOGLE_API_KEY environment variable not set. Please set it as a secret in your GitHub repository. If in command line/terminal, run the command: export GOOGLE_API_KEY='YOUR_API_KEY' ")

llm = LLM(
  model="gemini/gemini-2.0-flash",
  temperature=0.8,
  api_key=GOOGLE_API_KEY
)

checker = Agent(
  role = "Resume Completeness Checker",
  goal = f"To collect {numberOfTopics} engaging topics related to the theme: {theam}, addressed to an academic audience",
  backstory = f"You have been given a theme - {theam} - and you must collect {numberOfTopics} topics related to the theme, for people to write articles about. It can be in-depth core topics related to the theme, or informatory topics as well. Your work is the basis for the user to write an article (college graduate level) on these topics.",
  llm = llm,
  max_iter = 100,
  verbose = False,
  allow_delegation = False
)
