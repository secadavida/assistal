import pyfiglet

FIGLET_BIG = pyfiglet.Figlet(font='slant')
FIGLET_MINI = pyfiglet.Figlet(font='mini')

def print_text_ascii(message: str, use_mini: bool = True) -> None:

    message = " ".join(message)

    text = FIGLET_MINI.renderText(message) if use_mini else FIGLET_BIG.renderText(message)
    
    print(text)
