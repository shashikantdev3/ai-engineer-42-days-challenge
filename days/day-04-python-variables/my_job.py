# Day 4 homework: your job in 4 variables, one of each type.
# Step 1: change the 4 sample values below to your own.
# Step 2: run it: python meri_job.py
# Step 3: upload this file to your GitHub repo.

role = "L2 Support"     # str: your role, inside quotes
saal = 5                # int: years in your job, no quotes
rating = 4.5            # float: your last rating, with a decimal point
ai_seekh_raha = True    # bool: True or False, no quotes

# ---- You don't need to change anything below this line ----

# What type each khaana should have
expected = [
    ("role", role, str),
    ("saal", saal, int),
    ("rating", rating, float),
    ("ai_seekh_raha", ai_seekh_raha, bool),
]

print("Meri job ka bahi khata")
print("----------------------")

all_ok = True
for label, value, want in expected:
    got = type(value)
    # We compare the exact type. (Small Python fact: True also counts as
    # an int if you use isinstance, so we check type() directly here.)
    if got is want:
        status = "OK"
    else:
        status = "Check this: expected " + want.__name__ + ", got " + got.__name__
        all_ok = False
    print(f"{label:<14} = {value!r:<14} {got}  {status}")

print()
if all_ok:
    print("Sab sahi! 4 variables, har type ka 1.")
    print("Now comment TRUE on the Day 4 reel.")
else:
    print("Kuch types galat hain. Tips:")
    print('- Text needs quotes: "L2 Support"')
    print("- Numbers have no quotes: 5 or 4.5")
    print("- A float needs a decimal point: 4.0, not 4")
    print("- A bool is True or False with a capital letter and no quotes")
