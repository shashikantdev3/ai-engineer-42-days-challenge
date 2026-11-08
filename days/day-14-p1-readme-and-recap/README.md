# Day 14 · P1 GitHub pe + Week 2 recap

**Week 2 · LLM basics + Project 1** · [← Day 13](../day-13-p1-ticket-summarizer) · [Day 15 →](../day-15-embeddings) · [Roadmap](../day-01-roadmap)

> Chaddha sir: *"Rahul! Client ko demo pasand aaya, ab GitHub link chahiye, ek ghante mein!"*

Code ready hai. README khaali hai. Today you fix that, and you push Project 1 (Ticket Summarizer) to your own GitHub, **without your API key**.

## The idea: README = dukaan ka board

A shop's board tells you what it sells and how to come in. Board nahi, customer nahi.
Your README is the board of your project. Someone opening your repo should understand it in about 30 seconds.

| On the board | In your README | Example for P1 |
|---|---|---|
| **Naam** | `# Title` on top | `# Ticket Summarizer` |
| **Kya milta hai** | 1 line: what it does | 20 sample tickets → `report.json` |
| **Photo in the window** | Screenshot of the output | `![output](output.png)` |
| **Kaise aana hai** | `## Run`: 3 commands | install, make `.env`, run |
| **Dukaandaar ki baat** | `## Kya seekha`: what you learned | 2 or 3 honest lines |

A ready template is in [README_TEMPLATE.md](README_TEMPLATE.md), or let [write_readme.py](write_readme.py) fill it in for you.

## The 3 Run commands

```
pip install google-genai
cp .env.example .env
python summarizer.py
```

- `pip install google-genai` is the same package you used on Day 9.
- `cp .env.example .env` copies a **key-free** template file. The person who runs your project then opens `.env` and pastes **their own** key.
- Windows (Command Prompt): use `copy .env.example .env` instead of `cp`. PowerShell accepts `cp`.

## The trap: `git add .` sends your key too

`git add .` means "add everything in this folder". If `.env` is in the folder, your API key goes to GitHub with it. Public repo = anyone can see it.

**Day 9 rule:** put `.env` in `.gitignore`. Then Git skips it, and your key never goes to GitHub.

```
# .gitignore
.env
```

A full sample is in [sample.gitignore](sample.gitignore). Copy it into your P1 folder and rename it to `.gitignore`.

**Already pushed a key by mistake?** Deleting the file is not enough, because Git keeps the old commits. Go to the page where you made the key, delete that key and make a new one. Then add `.env` to `.gitignore` and push again.

## Aaj ka kaam (about 45 minutes)

Do this in your **P1 folder** (the Day 13 project), on your own laptop and your own accounts.

1. **Write the README.**
   ```
   python write_readme.py
   ```
   It asks a few questions and writes `README.md` (or `README_new.md` if you already have one, so nothing gets overwritten). Or copy [README_TEMPLATE.md](README_TEMPLATE.md) by hand.
2. **Take the screenshot.** Run `python summarizer.py`, then take a screenshot of the output:
   - Windows: `Win + Shift + S`
   - Mac: `Cmd + Shift + 4`

   Save it in the P1 folder as `output.png`. Check it shows no key and no real company data.
3. **Add the 2 safety files.**
   - `.gitignore` with `.env` inside (copy [sample.gitignore](sample.gitignore) and rename it).
   - `.env.example` with a placeholder, no real key (copy [.env.example](.env.example)).
4. **Check before you push.** Copy [check_before_push.py](check_before_push.py) into the P1 folder and run:
   ```
   python check_before_push.py
   ```
   It checks the 4 README parts, the `.gitignore`, and looks for anything that looks like a key. Fix every `[FIX]` line first.
5. **Push only your own files.** Create a new public repo on GitHub (for example `ticket-summarizer`), then in the P1 folder:
   ```
   git init
   git add README.md *.py *.png .gitignore .env.example tickets.json
   git status
   git commit -m "P1"
   git branch -M main
   git remote add origin https://github.com/<your-username>/ticket-summarizer.git
   git push -u origin main
   ```
   The reel shows the short version (`git add`, `git commit`, `git push`). The extra lines are only for the very first push of a new repo. Before `commit`, read `git status`: if you see `.env` in the list, stop and fix `.gitignore`.
6. **Open your repo link.** Does the README show the name, the 1 line, the screenshot and the Run commands? Agar haan, link ready.

**First time using Git?** Git asks who you are: `git config --global user.name "Your Name"` and `git config --global user.email "you@example.com"`.

**Browser upload instead of Git?** Fine, but drag the files one by one and **never** drag `.env`.

## Week 2 recap

| Idea | Desi version | What it means |
|---|---|---|
| **API** | Waiter | You give the order, the waiter brings it to the kitchen (the model) and brings the answer back. |
| **Tokens** | Paisa | Every bit of text you send and get back is counted in tokens. Fewer tokens, less spend. |
| **Prompt + FORM** | Clear order slip | A prompt written with this week's FORM recipe gets you the answer in the shape you want. |
| **Project 1** | First dukaan open | Ticket Summarizer: 20 sample tickets in, a report out. Now on your GitHub. ✓ |

## Honesty corner

- Sample data only (`tickets.json` from this repo). Never company tickets, not even "just for the demo".
- The client and the 1-hour deadline are a fictional story. A GitHub repo is proof of work, not a job guarantee.

## Files in this folder

| File | What it is |
|---|---|
| [README_TEMPLATE.md](README_TEMPLATE.md) | A fill-in README for P1 with the 4 board parts |
| [write_readme.py](write_readme.py) | Asks a few questions and writes the README for you |
| [check_before_push.py](check_before_push.py) | Checks README parts, `.gitignore` and leaked-key patterns before you push |
| [sample.gitignore](sample.gitignore) | Rename to `.gitignore`: keeps `.env` and Python junk off GitHub |
| [.env.example](.env.example) | Key-free template. Copy to `.env` and paste your own key there |

**Pushed?** Comment **GITHUB** on the Day 14 reel. Tomorrow, Day 15: Week 3 starts with embeddings, mohalle ka address.
