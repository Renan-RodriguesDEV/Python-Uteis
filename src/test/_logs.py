from colorama import Fore, Back, Style


def log_green(text):
    print(f"{Style.BRIGHT}{Fore.GREEN}{text}{Style.RESET_ALL}")


def log_blue(text):
    print(f"{Style.BRIGHT}{Fore.BLUE}{text}{Style.RESET_ALL}")


def log_red(text):
    print(f"{Style.BRIGHT}{Fore.RED}{text}{Style.RESET_ALL}")
