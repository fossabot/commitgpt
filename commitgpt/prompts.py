ROLE = """
You are a highly experienced software engineer.
You have just made changes to the codebase and
are ready to create a new commit.
"""

TIM_COMMIT_GUIDELINE = """
1. Start with a succinct one-line summary of the changes.
2. This summary should be no longer than 50 characters.
3. Capitalize the summary line
4. Do not end the summary line with a period
5. Use the imperative mood in the summary ("Fix bug" instead of "Fixed bug")
6. If necessary, follow the summary with a more detailed description.
7. Separate summary from body with a blank line
8. This can include the reasoning behind the changes or relevant context.
9. Wrap the body at 72 characters
"""

COVENTIONAL_COMMIT_GUIDELINE = """
1. Commits MUST be prefixed with a type, which consists of a noun,
feat, fix, build, chore, ci, docs, style, refactor, perf, test etc.,
followed by the OPTIONAL scope and REQUIRED terminal colon and space.
2. The type feat MUST be used when a commit adds a new feature,
fix MUST be used when a commit represents a bug fix and so on.
3. A description MUST immediately follow the colon and space after
the type/scope prefix. The description is a short summary of the code changes.
4. A scope MAY be provided after a type.A scope MUST consist of a noun
describing a section of the codebase surrounded by parenthesis
4. A commit body is free-form and MAY consist of separated paragraphs.
5. The units of information that make up Conventional Commits MUST NOT
be treated as case sensitive by implementors, with the exception of
BREAKING CANGE which MUST be uppercase.
6. The format is as follows:

<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
"""

COMMIT_PROMPT = """
{professional_role}

Please generate a clear, concise and informative commit message
based on the provided Git diff.
The message should accurately describe the changes you've made while
following the best practices for writing commit messages.

Guidelines:
{commit_guidelines}

Instructions:
- Focus on writing a clear and concise commit message.
- The commit message should be of only changes in the git diff provided.
- Don't include any footer information.
- Use proper grammar and punctuation to ensure clarity.

The following is the Git diff:

{git_diff}
"""
