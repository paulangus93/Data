Getting started:
1. Install Git on your system : https://git-scm.com/downloads
2. Install python - minimum version is 3.7
3. Install pip: See tips for:
 * Windows https://phoenixnap.com/kb/install-pip-windows
 * Linux: https://linuxize.com/post/how-to-install-pip-on-ubuntu-20.04/
4. If you already have Python and pip, you can easily install Pipenv into your home directory (ref: https://pipenv.pypa.io/en/latest/#install-pipenv-today):
5. From the terminal (git bash conforms to most linux commands without the hassle of WSL) install pipenv:
   ```
   pip install --user pipenv
   ```
6. From terminal: install repos in Pipenv :
  ```
  pipenv install 
  ``` 
7. For more on pipenv - follow instructions : https://pypi.org/project/pipenv/
8. DO: (Some working tips for code health and clean version control) : 
   * Avoid working on the main branch
   * Commit and make edits on the develop branch, 
   * For test and side efforts work on a side branch.
      ** Working solo tip: Merge into parent branch when done 
   * Working together tips:
    ** Use pull requests for code review 
    ** Use Githubs issues to link bugs and pull requests
    ** Enables auto-merge into parent branch
   * Merge when testing of feature is validated
   * For sanity - Try to have few parallel forks and merge back to parent when feature is working
   * Good practice is to documenet changes using commits. Commit at least once at end of day to keep track of work 
9. DO NOT:
   * Commit non-text files (includes binaries or large log files)
   * Large files can lead eventually exceedign limits  of the GitHub Free restrictions
   * Github free allows for : 

	** Unlimited public/private repos
	** Unlimited collaborators
	** 2,000 Actions minutes/month
	** 500MB of Packages storage
	** Community support

11. Read more on version control using git here: https://git-scm.com/doc 
12. Read more on Pull requests and Bugs here - https://docs.github.com/en/github/managing-your-work-on-github/about-issues
13. Further resources on Github for managing a project: https://docs.github.com/en/github/managing-your-work-on-github/about-project-boards 
