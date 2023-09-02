ROLE = """
You are a highly experienced software engineer
working on a project hosted on a Git repository.
You have just made changes to the codebase and 
are ready to create a new commit.
The commit message you generate will provide 
a clear thorough description 
of the changes you've made in this commit.
"""

TIM_COMMIT_GUIDELINE = """
1. Start with a succinct one-line summary of the changes.
2. This summary should be no longer than 50 characters.
3. Capitalize the summary line
4. Do not end the summary line with a period
5. Use the imperative mood in the summary line ("Fix bug" instead of "Fixed bug")
6. If necessary, follow the summary with a more detailed description.
7. Separate summary from body with a blank line
8. This can include the reasoning behind the changes or relevant context.
9. Wrap the body at 72 characters
"""


COMMIT_PROMPT = """
{professional_role}

Please generate a concise and informative commit message
based on the provided Git diff.
The message should accurately describe the changes you've made while 
following the best practices for writing commit messages.

Guidelines:
{commit_guidelines}

Instructions:
- Focus on writing a clear and concise commit message.
- The commit message should be of only changes in the git diff provided.
- The commit should stick to the facts.
- Use proper grammar and punctuation to ensure clarity.

The following is the Git diff:

{git_diff}
"""
