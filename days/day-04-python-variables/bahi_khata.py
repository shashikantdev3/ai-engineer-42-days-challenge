# Day 4: Python ka bahi khata
# A variable is a khaana (box) with a label on top and a value inside.
# All values below are sample values. Run: python bahi_khata.py

# label = value
naam = "Rahul"          # str: text, always inside quotes
saal = 5                # int: a whole number
rating = 4.5            # float: a number with a decimal point
ai_seekh_raha = True    # bool: only True or False (capital T, capital F)

print("Bahi khata (example entries)")
print("-----------------------------")
print("naam          =", naam)
print("saal          =", saal)
print("rating        =", rating)
print("ai_seekh_raha =", ai_seekh_raha)
print()

# type() tells you what kind of value is inside the khaana
print("Type check:")
print("naam          ->", type(naam))
print("saal          ->", type(saal))
print("rating        ->", type(rating))
print("ai_seekh_raha ->", type(ai_seekh_raha))
print()

# The exact line from the reel. It shows: <class 'float'>
print(type(rating))
print()

# Bonus: quotes change the type
saal_text = "5"
print('saal = 5   ->', type(saal))
print('saal = "5" ->', type(saal_text), "(quotes make it text)")
print()

# Bonus: ALL CAPS name means "please don't change this" (only a convention)
VARIABLE_PAY = 0
print("VARIABLE_PAY =", VARIABLE_PAY, "(Rahul says: this one is a constant)")
