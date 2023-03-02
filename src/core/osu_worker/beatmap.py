def change_version(lines, start_i, postfix):
    i = skip_to_version(lines, start_i)
    version_line = lines[i]
    del lines[i]

    version = f"{version_line.split(':')[-1]} {postfix}"
    lines.insert(i, f"Version:{version}")

    return i, version


def parse_slider_multiplier(lines, start_i):
    i = skip_to_slider_multiplier(lines, start_i)
    slider_multiplier = float(lines[i].split("SliderMultiplier:")[1])
    return i, slider_multiplier


def skip_to_slider_multiplier(lines, start_i):
    i = start_i
    while not ("SliderMultiplier:" in lines[i] and "ApproachRate:" in lines[i - 1]):
        i += 1
    return i


def skip_to_version(lines, start_i):
    i = start_i
    while not ("Version:" in lines[i] and "Creator:" in lines[i - 1]):
        i += 1
    return i


def skip_to_timings(lines, start_i):
    i = start_i
    while not ("[TimingPoints]" in lines[i-1] and not lines[i-2]):
        i += 1
    return i


def skip_to_hit_objs(lines, start_i):
    i = start_i
    while not ("[HitObjects]" in lines[i-1] and not lines[i-2]):
        i += 1
    return i
