# Contributing guidelines

## Before contributing

Welcome to commitgpt! Before sending your pull requests, make sure that you **read the whole guidelines**. If you have any doubt on the contributing guide, please feel free to [state it clearly in an issue](https://github.com/0x6flab/gptcommit/issues/new).

## Contributing

### Contributor

We are very happy that you are considering contributing to this project! Being one of our contributors, you agree and confirm that:

- Your work will be distributed under [GNU GENERAL PUBLIC LICENSE](LICENSE.md) once your pull request is merged
- Your submitted work fulfils or mostly fulfils our styles and standards

**Improving comments** and **writing proper tests** are also highly welcome.

### Contribution

We appreciate any contribution, from fixing a grammar mistake in a comment to implementing complex algorithms. Please read this section if you are contributing your work.

Your contribution will be tested by our [automated testing on GitHub Actions](https://github.com/0x6flab/gptcommit/actions) to save time and mental energy. After you have submitted your pull request, you should see the GitHub Actions tests start to run at the bottom of your submission page. If those tests fail, then click on the **_details_** button try to read through the GitHub Actions output to understand the failure. If you do not understand, please leave a comment on your submission page.

If you are interested in resolving an [open issue](https://github.com/0x6flab/gptcommit/issues), simply make a pull request with your proposed fix. **We do not assign issues in this repo** so please do not ask for permission to work on an issue.

Please help us keep our issue list small by adding `Fixes #{$ISSUE_NUMBER}` to the description of pull requests that resolve open issues.
For example, if your pull request fixes issue #10, then please add the following to its description:

```git
Fixes #10
```

GitHub will use this tag to [auto-close the issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) if and when the PR is merged.

#### What is an commitgpt?

Commitgpt is a api wrapper around git and LLMs to generate commit messages.

#### Pre-commit plugin

Use [pre-commit](https://pre-commit.com/#installation) to automatically format your code to match our coding style:

```bash
pip install pre-commit  # only required the first time
pre-commit install
```

That's it! The plugin will run every time you commit any changes. If there are any errors found during the run, fix them and commit those changes. You can even run the plugin manually on all files:

```bash
pre-commit run --all-files --show-diff-on-failure
```

#### Coding Style

We want our work to be readable by others; therefore, we encourage you to note the following:

- Please write in Python 3.11+. For instance: `print()` is a function in Python 3 so `print "Hello"` will _not_ work but `print("Hello")` will.
- Please focus hard on the naming of functions, classes, and variables. Help your reader by using **descriptive names** that can help you to remove redundant comments.
- Single letter variable names are _old school_ so please avoid them unless their life only spans a few lines.
- Expand acronyms because `gcd()` is hard to understand but `greatest_common_divisor()` is not.
- Please follow the [Python Naming Conventions](https://pep8.org/#prescriptive-naming-conventions) so variable_names and function_names should be lower_case, CONSTANTS in UPPERCASE, ClassNames should be CamelCase, etc.
- We encourage the use of Python [f-strings](https://realpython.com/python-f-strings/#f-strings-a-new-and-improved-way-to-format-strings-in-python) where they make the code easier to read.
- Please consider running [ruff](https://beta.ruff.rs/docs/tutorial/) on your code to check for common errors and to enforce our coding style:

  ```bash
  pip install ruff  # only required the first time
  ruff .
  ```

- All submissions will need to pass the test `ruff .` before they will be accepted so if possible, try this test locally on your Python file(s) before submitting your pull request.
- Original code submission require docstrings or comments to describe your work.
- More on docstrings and comments:

  If you used a Wikipedia article or some other source material, please add the URL in a docstring or comment to help your reader.

  We encourage you to put docstrings inside your functions but please pay attention to the indentation of docstrings. The following is a good example:

  ```python
  def sum_ab(a, b):
      """
      Return the sum of two integers a and b.
      """
      return a + b
  ```

- Write tests (especially [**doctests**](https://docs.python.org/3/library/doctest.html)) to illustrate and verify your work. We highly encourage the use of _doctests on all functions_.

  ```python
  def sum_ab(a, b):
      """
      Return the sum of two integers a and b
      >>> sum_ab(2, 2)
      4
      >>> sum_ab(-2, 3)
      1
      >>> sum_ab(4.9, 5.1)
      10.0
      """
      return a + b
  ```

- These doctests will be run by pytest as part of our automated testing so please try to run your doctests locally and make sure that they are found and pass:

  ```bash
  python3 -m doctest -v my_submission.py
  ```

- The use of [Python type hints](https://docs.python.org/3/library/typing.html) is encouraged for function parameters and return values. Our automated testing will run [mypy](http://mypy-lang.org) so run that locally before making your submission.

  ```python
  def sum_ab(a: int, b: int) -> int:
      return a + b
  ```

  Instructions on how to install mypy can be found [here](https://github.com/python/mypy). Please use the command `mypy --ignore-missing-imports .` to test all files or `mypy --ignore-missing-imports path/to/file.py` to test a specific file.

- If you need a third-party module that is not in the file **pyproject.toml**, please add it to that file as part of your submission.

#### Other Requirements for Submissions

- Strictly use snake_case (underscore_separated) in your file_name, as it will be easy to parse in future using scripts.
- Please avoid creating new directories if at all possible. Try to fit your work into the existing directory structure.
- If possible, follow the standard _within_ the folder you are submitting to.
- If you have modified/added code work, make sure the code compiles before submitting.
- If you have modified/added documentation work, ensure your language is concise and contains no grammar errors.
- All submissions will be tested with [**mypy**](http://www.mypy-lang.org) so we encourage you to add [**Python type hints**](https://docs.python.org/3/library/typing.html) where it makes sense to do so.

- Most importantly,
  - **Be consistent in the use of these guidelines when submitting.**
  - Happy coding!
