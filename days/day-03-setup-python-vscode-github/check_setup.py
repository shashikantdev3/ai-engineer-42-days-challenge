"""Day 3 setup check: is the dukaan ready?
Run it:  python check_setup.py      (Mac/Linux: python3 check_setup.py)
It only looks at your computer. It does not install or change anything."""
import shutil
import sys


def show(label, good, tip):
    print(("[OK]  " if good else "[--]  ") + label + ("" if good else "\n      -> " + tip))
    return good


v = sys.version_info
python_ok = show(f"Python {v.major}.{v.minor} (shutter)", v >= (3, 10),
                 "Install Python 3.10 or newer from python.org, then open a new terminal.")
show("VS Code 'code' command (counter)", shutil.which("code") is not None,
     "Optional. Windows: re-run the VS Code installer with 'Add to PATH' ticked. "
     "Mac: in VS Code press Cmd+Shift+P and run \"Shell Command: Install 'code' command in PATH\".")
show("Git (for pushing to GitHub from the terminal)", shutil.which("git") is not None,
     "Optional today (browser upload works). Install it from git-scm.com when you are ready.")

print()
print("Dukaan ready hai! Ab hello.py GitHub pe daalo." if python_ok else "Shutter abhi band hai: pehle Python theek karo.")
