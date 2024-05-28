import os, sys

def clear_screen():
    os.system('cls')
def Hide_cursor():
    print("\033[?25l", end="")
def Show_cursor():
    print("\033[?25h", end="")
def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios    #for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)