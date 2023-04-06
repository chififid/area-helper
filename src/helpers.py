from termcolor import colored


def get_num(desc, several=False, count=None, n_range=None, another_converter=None):
    args = locals()

    converter = int
    if another_converter:
        converter = another_converter

    inf = input(desc)
    try:
        if several:
            res = list(map(converter, inf.split(" ")))
            if count and count != len(res):
                print(colored(f"You must write only {count} params", "red"))
                return get_num(**args)
        else:
            res = converter(inf)
            if n_range and res not in n_range:
                print(colored(f"This num isn't in the {n_range}", "red"))
                return get_num(**args)
        return res
    except ValueError:
        print(colored(f"Can't handle this num", "red"))
        return get_num(**args)
