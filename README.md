  [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/uryyakir/all-repos-readme/master.svg)](https://results.pre-commit.ci/latest/github/uryyakir/all-repos-readme/master)  ![tox tests](https://github.com/uryyakir/all-repos-readme/actions/workflows/tox-github-action.yml/badge.svg) ![linters](https://github.com/uryyakir/all-repos-readme/actions/workflows/github-linters-CI.yml/badge.svg)
# Add a dynamically generated *<span>README.md</span>* to all of your repos!
### This tool automatically generates a dynamic *<span>README.md</span>* file for all of the user owned Github repositories (that don't already have one).
##### An example for the tool's automatically generated README can be found at the end.

### Why is this useful?
1. Composing a *<span>README.md</span>* file can be a tedious task. Sometimes our use-case doesn't require a tailor-made explanation for our repos, and a simple metadata-based README may be sufficient .
2. One README to rule them all - this tool also supports leveraging a user-created README and using that for all of the user's repos. This custom README may be provided through a local `.md` file, or via `STDIN`.

## INSTALLATION:

This package is NOT distributed to pypi, please install the package directly from this public repo:<br>
<li>If a virtualenv is activated:</li>

`python3 -m pip install git+git://github.com/uryyakir/all-repos-readme.git`
<li>If you want to install globally:</li>

`sudo python3 -m pip install git+git://github.com/uryyakir/all-repos-readme.git`

## PREREQUISITES:

After the installation is complete, you should already be able to run `all-repos-add-readme --help`.
However, if you try to use the tool right away, you will notice an exception:
```bash
> all-repos-add-readme --dry-run
> Traceback (most recent call last):
....
FileNotFoundError: [Errno 2] No such file or directory: '/Users/your_user/your/PWD/config.json'
```
This exception is raised because the tool needs your Github authentication key to access and update your repositories. Please refer to [Github's documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) that throughly explains how to generate that key.

Successfully generated a key? Great!
Now, all you have to do is create a simple `config.json` file as following:
```json
{
	"apiKey": "your-api-key",
	"username": "your-github-username"
}
```
To resolve that exception, you may either:
-  Create this file within your current working directory
-  Create the file in another directory, and point the tool to it using the `--config-filepath` CLI argument

## USAGE:
When you install the tool, it enables the internal tool's CLI:

```bash
usage: all-repos-add-readme [-h] [--readme-file README_FILE]
[--readme-string README_STRING] [--verbose]
[--dry-run] [--commit-message COMMIT_MESSAGE]
[--log-to-file [LOG_TO_FILE]]
[--config-filename CONFIG_FILENAME]
[--repoignore-filename REPOIGNORE_FILENAME]
A tool to create a generic README.md for all of the user owned REPOs.

optional arguments:
-h, --help
	show this help message and exit
--readme-file README_FILE, -rf README_FILE
	path to readme file that would be added to all repos
--readme-string README_STRING, -rs README_STRING
	markdown-supported string to be added as a README to all repos
--verbose, -v
	provide debugging information when running tool
--dry-run
	prevents tool from actually making commits to user repos, but preforms the same workflow
--commit-message COMMIT_MESSAGE
	provide a custom commit message for the creation or update of the README.md file. Default: 'add README.md (automatically committed by the `all_repos_readme` tool)'
--log-to-file [LOG_TO_FILE]
	output tool logs to file
--config-filepath CONFIG_FILEPATH
	path to config.json file that includes GitHub's api key
--repoignore-filepath REPOIGNORE_FILEPATH
	path to .repoignore file
```
Example usage:
1. `> all-repos-add-readme --dry-run` --> Runs a dry run. The tool will spit out the exact changes that it proposes. This is highly recommended before any actual wet run.
2. Insert custom markdown-supported text via STDIN:
```bash
> read -r -d '' VAR << EOM
# Here's a title
## Here's a sub-title
This is just some random text.
EOM
> all-repos-add-readme --readme-string "$VAR"
```
3. `> all-repos-add-readme --commit-message "Custom commit message"` - customize the commit message for the new README file.
4. `> all-repos-add-readme --readme-file path/to/custom/README.md` - provide a path to a local markdown file that will be used for all repos.

## FEATURES
- `.repoignore` - You may create a `.repoignore` file somewhere in your local FS. That file shall contain a newline-separated list of regular expressions. These regular expressions would be leveraged by the tool to determine whether it should act on some repository or not. For example:
```bash:
// Example A
echo all-repos-readme-testing >> .repoignore
> all-repos-add-readme
> (The tool will operate on all repos BUT the 'all-repos-readme-testing' repo)

// Example B
> python3 -c 'import shlex; print(shlex.quote("^(?!(.*?all-repos-readme-testing)).*"));' | xargs echo >> .repoignore
> all-repos-add-readme
> (The tool will operate ONLY on the 'all-repos-readme-testing' repo)
```

- I've implemented custom `.githooks` that prevent contributors from accidentally committing their Github auth keys when testing their changes.
*Contributors* - to opt-in, please set git's hookPath to use my custom hooks directory.
Simply clone the repo and run:
`git config core.hooksPath .githooks/`
You may also need to explicitly make the hooks' bash scripts executable (e.g. `chmod +x .githooks/pre-commit`). Please note that even when not using this feature, this is not a security risk as Github automatically invalidates accidentally committed auth keys.
- Integration with [pre-commit](https://pre-commit.com/).
- Providing a custom README file from the local FS instead of the default repo statistics-based auto generated README.
- Providing a custom commit message as a part of the README update.
---
### Example for the tool's automatically generated README:
---
*(+++repo title+++)*
# `uryyakir/all-repos-readme-testing`

*(+++repo description+++)*

### a repo designated to testing functionality of all-repos-readme
*(+++repo statistics template+++)*
<ol>
 <li>
  Repo was created at: 2021-08-22 21:28:53
 </li>
 <li>
  Repo was last updated at: 2021-09-13 16:39:59
 </li>
 <li>
  Total commits: >= 267
 </li>
 <li>
  Used languages distribution:
 </li>
 <ul id="used_languages">
  <li>
   Python: 69.03%
  </li>
  <li>
   JavaScript: 18.71%
  </li>
  <li>
   Shell: 12.26%
  </li>
 </ul>
 <li>
  Total contributors: >= 1
 </li>
</ol>


*(+++tool disclaimer+++)*

#### Disclaimer: this is an auto-generated README.md file, committed by the [all_repos_readme](https://github.com/uryyakir/all-repos-readme) tool at 13/09/2021.
To update repo stats, re-run the tool :)
