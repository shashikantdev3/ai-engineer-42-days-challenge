# Day 6: the for loop, explained with mummy ki rotiyan.
# "Har roti ke liye: belo, seko, palto" is exactly what a for loop says.

def belo(roti):
    print(f"Roti {roti}: beli")

def seko(roti):
    print(f"Roti {roti}: seki")

def palto(roti):
    print(f"Roti {roti}: palti, ready!")

rotiyan = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]   # 10 rotiyan (example)

for roti in rotiyan:      # har roti ke liye...
    belo(roti)            # ...4 spaces andar: yeh kaam har roti pe chalega
    seko(roti)
    palto(roti)

print("Sab", len(rotiyan), "rotiyan ready.")
