from termcolor import colored
from alive_progress import alive_bar


def create_bar(count):
    return alive_bar(
        count,
        spinner="waves",
        stats=False,
        spinner_length=10,
        calibrate=10,
        enrich_print=False,
    )


def set_bar_text(bar, text):
    bar.text(text)


def item_done(bar, error_msg=None):
    if error_msg:
        print(colored(error_msg, "yellow"))
    bar()
