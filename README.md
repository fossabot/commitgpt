# commitgpt

[![Coverage Status](https://coveralls.io/repos/github/0x6flab/commitgpt/badge.svg?branch=tests)](https://coveralls.io/github/0x6flab/commitgpt?branch=tests)
[![Continuous Integration](https://github.com/0x6flab/commitgpt/actions/workflows/ci.yaml/badge.svg)](https://github.com/0x6flab/commitgpt/actions/workflows/ci.yaml)
[![Continuous Deployment](https://github.com/0x6flab/commitgpt/actions/workflows/cd.yaml/badge.svg)](https://github.com/0x6flab/commitgpt/actions/workflows/cd.yaml)

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

[![asciicast](https://asciinema.org/a/606115.svg)](https://asciinema.org/a/606115)

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
