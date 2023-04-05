<div align="center">

## `H a p d o c`
autodoc CLI tool written in Python with :heart:

![Python](https://img.shields.io/badge/Python%203.10-35497E?style=for-the-badge&logo=python&logoColor=FFF077)
![FastAPI](https://img.shields.io/badge/FastAPI-35497E?style=for-the-badge&logo=fastapi&logoColor=FFF077)

![Version](https://img.shields.io/pypi/v/hapdoc?label=hapdoc&style=for-the-badge)
[![wakatime](https://wakatime.com/badge/user/eaf11f95-5e2a-4b60-ae6a-38cd01ed317b/project/f4dc9f08-796d-42b1-9065-363e5a347ecf.svg?style=for-the-badge)](https://wakatime.com/badge/user/eaf11f95-5e2a-4b60-ae6a-38cd01ed317b/project/f4dc9f08-796d-42b1-9065-363e5a347ecf)

[![CodeFactor](https://www.codefactor.io/repository/github/hapticx/hapdoc/badge?style=for-the-badge)](https://www.codefactor.io/repository/github/hapticx/hapdoc)

</div>

## Why Hapdoc? 💁‍♀️
- `Easy to use`: Hapdoc is designed to be simple and user-friendly, making it easy for programmers to create documentation without having to spend a lot of time learning how to use it.
- `Markdown support`: Hapdoc supports Markdown syntax, which is a popular markup language used by many developers. This means that programmers can write documentation using the same tools they use to write code, making the process more familiar and efficient.
- `Customizable themes`: Hapdoc supports different themes, allowing programmers to choose a look and feel that matches their project or organization's branding. Additionally, programmers can create their own themes if they want to customize the look of their documentation further.

### Features :sparkles:
- Supported projects:
  - `Python`
  - `FastAPI`
  - `JavaScript`
- Generate Markdown docs via `gen` command.
- Build docs into HTML via `build` command.
- Serve generated docs at your server via `serve` command.
- Create your own templates via `tmpl-new` command.

## Installing 📥
via `pypi` 📦
```bash
pip install hapdoc --upgrade
```
via `git` 💾
```bash
pip install https://github.com/hapticx/hapdoc
```

## Usage ⚡
Help message
```bash
hapdoc --help
```
Generate and serve docs via FastAPI:
```bash
hapdoc gen path/to/project
hapdoc serve docs/hapdoc -h 127.0.0.1 -p 5000
```
Build HTML docs:
```bash
hapdoc build path/to/project
```

## What's Next? 💡
We planned to add some other project types! Check more in [issues:doc_rules](https://github.com/HapticX/hapdoc/labels/doc%20rules)

## Contributing :dizzy:
You can help us and create PR with project type ✌
