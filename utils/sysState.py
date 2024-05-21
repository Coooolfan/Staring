import subprocess
import time


def is_locked():
    """
    Check if the computer is locked.\n
    This function is unreliable, \n
    see https://learn.microsoft.com/en-gb/windows/win32/api/winuser/nf-winuser-lockworkstation#:~:text=There%20is%20no%20function%20you%20can%20call%20to%20determine%20whether%20the%20workstation%20is%20locked.

    :returns: True if the computer is locked, False otherwise
    """
    process_name = 'LogonUI.exe'
    callall = 'TASKLIST'
    outputall = subprocess.check_output(callall)
    outputstringall = str(outputall)
    if process_name in outputstringall:
        return True
    else:
        return False

def lock():
    """
    Lock the computer
    """
    subprocess.run("rundll32.exe user32.dll,LockWorkStation")


if __name__ == '__main__':
    time.sleep(5)
    if is_locked():
        print("The computer is locked.")
    else:
        print("The computer is not locked.")
