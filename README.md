# commitgpt

commitgpt assists developers in generating high-quality commit messages for their version control systems, such as git.

## Features

- Generate commit messages from OpenAI's GPT-3 API based on the changes in the diff
- Configurable commit message guidelines
- Configurable OpenAI GPT-3 agent role

## Prerequisites

- An OpenAI API key
- Python 3.6 or higher
- Pip
- Git

## Installation

```bash
pip install commitgpt
```

## Usage

```bash
commitgpt setup
```

## Example

Make a change to a file, then run `git diff` to see the changes. Then, run `commitgpt` to generate a commit message.

```bash
commitgpt
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

[GNU GENERAL PUBLIC LICENSE](LICENSE)
