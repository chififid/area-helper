from termcolor import colored


def get_num(desc, several=False, n_range=False, another_converter=None):
    converter = int
    if another_converter:
        converter = another_converter

    inf = input(desc)
    try:
        if several:
            res = list(map(converter, inf.split(" ")))
        else:
            res = converter(inf)
            if n_range and res not in n_range:
                print(colored(f"This num isn't in the {n_range}", "red"))
                return get_num(desc, several, n_range)
        return res
    except ValueError:
        return get_num(desc, several, n_range)
