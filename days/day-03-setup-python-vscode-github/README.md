# Day 3 · Dukaan kholne se pehle: setup

**Week 1 · Python basics** · [← Day 2](../day-02-ai-engineer-kya-karta-hai) · [Day 4 →](../day-04-python-variables) · [Roadmap](../day-01-roadmap)

> Rahul: *"3 YouTube videos dekhe... abhi tak Python install nahi hua!"*

## The idea: 3 things before the shop opens

| Tool | In the dukaan | What it does |
|---|---|---|
| **Python** | Shutter | Runs your code. Without it, the shop never opens. |
| **VS Code** | Counter | Where you write code. Free editor. |
| **GitHub** | Bahi khata | Where your work lives in public. This is your proof. |

## Aaj ka kaam (about 45 minutes)

1. **Python.** Download it from [python.org/downloads](https://www.python.org/downloads/) and install it. Then open a terminal and check:
   - Windows: `python --version`
   - Mac / Linux: `python3 --version`

   Windows and `python` doesn't work? Close the terminal, open a new one and try again, or try `py --version`.
2. **VS Code.** Install it from [code.visualstudio.com](https://code.visualstudio.com/). Open Extensions, search **Python** and install the one by Microsoft.
3. **GitHub.** Make a free account on [github.com](https://github.com/) and create a public repo, for example `ai-engineer-42-days`.
4. **hello.py.** Copy [hello.py](hello.py) into a folder, open the folder in VS Code and run it:
   ```
   python hello.py
   ```
   You should see `Hello, Lala Infotech!` and your Python version.
5. **Put it on GitHub.** On your repo page: **Add file → Upload files**, drop `hello.py`, then **Commit changes**. Done. Your bahi khata has its first entry.

**Not sure everything is ready?** Run [check_setup.py](check_setup.py). It only looks at your computer and tells you what is missing:
```
python check_setup.py
```

## One rule: office laptop pe nahi

Use your own laptop and your own accounts. Office laptops have company policies, and this repo is your proof, so it should belong to you.

## Pro way (optional): push with Git

Browser upload is enough for today. If you already have [Git](https://git-scm.com/) installed:

```
git clone https://github.com/<your-username>/ai-engineer-42-days.git
cd ai-engineer-42-days
# copy hello.py into this folder, then:
git add hello.py
git commit -m "Day 3: hello.py"
git push
```

The first time, Git asks who you are: `git config --global user.name "Your Name"` and `git config --global user.email "you@example.com"`.

## Files in this folder

| File | What it is |
|---|---|
| [hello.py](hello.py) | Your first Python file: prints a hello and your Python version |
| [check_setup.py](check_setup.py) | Checks Python, the VS Code `code` command and Git |

**Setup done?** Comment **DONE** on the Day 3 reel. Tomorrow, Day 4: variables, without the maths darr.
