from colorama import Fore, Style

def red_text(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}"

# que l'on peut utiliser comme ceci
message = "def"
print(f"abc{red_text(message)}ghi")