# Day 4 · Python ka bahi khata: variables

**Week 1 · Python basics** · [← Day 3](../day-03-setup-python-vscode-github) · [Day 5 →](../day-05-lists-and-dicts) · [Roadmap](../day-01-roadmap)

> Chaddha sir: *"Variable?... Variable pay is saal bhi 0 hai."*
> Rahul: *"Sir, jo har saal 0 rahe... wo variable nahi, constant hai."*

## The idea: variable = a khaana in the bahi khata

Forget the school x and y. Think of a shopkeeper's bahi khata. Every khaana (box) has a **label** on top and a **value** inside. That is a variable.

```python
naam = "Rahul"
```

`naam` is the label. `"Rahul"` is the value. The `=` means "put this value in this khaana". It is not maths.

## The 4 types of entry

| Type | In the khata | Example | What it holds |
|---|---|---|---|
| **str** (string) | Text entry | `naam = "Rahul"` | Words and letters, always inside quotes |
| **int** (integer) | Whole number | `saal = 5` | Numbers without a decimal point |
| **float** | Decimal number | `rating = 4.5` | Numbers with a decimal point |
| **bool** (boolean) | Haan-na | `ai_seekh_raha = True` | Only `True` or `False` |

All values here are examples. Use your own.

Want to know what type a value is? Ask Python:

```python
rating = 4.5
print(type(rating))
```

Output:

```
<class 'float'>
```

## Aaj ka kaam (about 20 minutes)

1. **Run the reel's example.** Copy [bahi_khata.py](bahi_khata.py) into your repo folder, open it in VS Code and run it:
   ```
   python bahi_khata.py
   ```
   (Mac / Linux: `python3 bahi_khata.py`.) You will see each value and its type.
2. **Make your own 4 variables.** Open [my_job.py](my_job.py). Change the 4 sample values to your own job, one of each type:
   - `role`: a str, like `"L2 Support"`
   - `saal`: an int, like `5`
   - `rating`: a float, like `4.5`
   - `ai_seekh_raha`: a bool, `True`
3. **Run it.**
   ```
   python my_job.py
   ```
   It prints every type and tells you if each one is the right type.
4. **Push it to GitHub.** Same as Day 3: on your repo page, **Add file → Upload files**, drop `my_job.py`, then **Commit changes**. Your bahi khata now has its second entry.

## Common galtiyan (mistakes)

| You wrote | What happens | Fix |
|---|---|---|
| `naam = Rahul` | `NameError`: Python looks for a variable called Rahul | Text needs quotes: `"Rahul"` |
| `ai_seekh_raha = true` | `NameError`: lowercase `true` does not exist | Capital T: `True` |
| `ai_seekh_raha = "True"` | Works, but it is a **str**, not a bool | Remove the quotes |
| `saal = "5"` | Works, but it is a **str**, not an int | Remove the quotes |
| `my role = "L2"` | `SyntaxError`: no spaces in a label | Use underscore: `my_role` |
| `2role = "L2"` | `SyntaxError`: a label can't start with a number | `role2` is fine |

Also: labels are case-sensitive. `Rating` and `rating` are two different khaane.

## Bonus: Rahul's constant joke, in real Python

Python has no locked "constant" type. By convention, a name in ALL CAPS means "this value should not change":

```python
VARIABLE_PAY = 0   # caps = please don't change it
```

Python will still let you change it. The caps are a promise between programmers, not a rule Python checks. (Chaddha sir follows this convention very strictly.)

## Files in this folder

| File | What it is |
|---|---|
| [bahi_khata.py](bahi_khata.py) | The reel's example: 4 sample variables, one of each type, with their types printed |
| [my_job.py](my_job.py) | Your homework: put your own job in 4 variables and check each type |

**Done?** Comment **TRUE** on the Day 4 reel. Tomorrow, Day 5: 100 tickets ke liye 100 variables? Nahi. Ek list.
