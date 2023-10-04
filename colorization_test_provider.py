import colorsys
import math
import colormath.color_conversions
import colormath.color_objects


avg_i = None
def draw_averaging(dim: int, pygame, screen, y_x: list[list[tuple[int, float, float]]]):
    global avg_i
    if avg_i is None:
        avg_i = 0
        avg_c = 0
        for y in range(dim):
            for x in range(dim):
                it, _, _ = y_x[y][x]
                if it != -1:
                    avg_i += it
                    avg_c += 1
        avg_i /= avg_c
    for y in range(dim):
        pygame.display.update()
        for x in range(dim):
            data = y_x[y][x]
            screen.set_at((x, y), color(*data, x, y, avg_i))
    pygame.display.update()

def draw(dim: int, pygame, screen, y_x: list[list[tuple[int, float, float]]], display_update: bool = False, max_iters: int = 1_000):
    counts = {}
    '''for y in range(dim):
        for x in range(dim):
            it, _, _ = y_x[y][x]
            if it != -1:
                if it not in counts:
                    counts[it] = 0
                counts[it] += 1'''
    total = 0
    '''for count in counts.values():
        total += count'''

    for y in range(dim):
        if display_update and y%10==0:
            pygame.display.update()
        for x in range(dim):
            data = y_x[y][x]
            screen.set_at((x, y), color_counts(*data, x, y, counts, total, max_iters))
    if display_update:
        pygame.display.update()

def _clean(c: tuple[int|float, int|float, int|float]) -> tuple[int, int, int]:
    # noinspection PyTypeChecker
    return tuple(max(0, min(int(n), 255)) for n in c)

def _to_255(c: tuple[float, float, float]) -> tuple[int, int, int]:
    # noinspection PyTypeChecker
    return tuple(n*255 for n in c)

# averaging colorization
def color(iters: int, fx: float, fy: float, x: int, y: int, avg_iters: float) -> tuple[int, int, int]:
    if iters == -1:
        return 0, 0, 0
    #try:
    #    return _clean(_to_255(colorsys.hls_to_rgb(math.log2(iters*iters*iters) / max(0.00001, (x*x + y*y)**2), 0.5, 1)))#fx/15+0.5)))
    #except ValueError:
    #    return 255, 0, 0
    #return _clean(_to_255(colorsys.hls_to_rgb((fx*fx + fy*fy)/15, 0.5, 1)))
    try:
        return _clean(_to_255(colorsys.hls_to_rgb(iters/avg_iters, 0.5, 1)))
    except ValueError:
        return (255, 0, 0)

def _lerp(a: tuple[float, float, float], b: tuple[float, float, float], x: float) -> tuple[float, float, float]:
    return tuple([(a[i] * (1-x)) + (b[i]*x) for i in range(3)])


MAX_I = 1_000_000
_cache: dict[tuple[int, int], tuple[int, int, int]] = {}
def iters_to_color(iters: int, max_iters: int) -> tuple[int, int, int]:
    key = (iters, max_iters)
    if key in _cache:
        return _cache[key]
    z = 0.26
    si = (iters / max_iters) ** z
    cos_tmp = math.cos(math.pi * si)
    v = 1.0 - cos_tmp * cos_tmp

    L = 75 - (75 * v)
    C = 28 + L
    H = ((360 * si) ** 1.5) % 360

    rgb_col: colormath.color_objects.sRGBColor = colormath.color_conversions.convert_color(
        colormath.color_conversions.LCHabColor(L, C, H), colormath.color_objects.sRGBColor)
    ret = _clean(_to_255(rgb_col.get_value_tuple()))

    _cache[key] = ret
    return ret

if MAX_I <= 10_000:
    print("Precaching colors")
    for cache_count in range(MAX_I+1):
        iters_to_color(cache_count, MAX_I)
    print("Done precaching")

log_2 = math.log(2)
def color_counts(iters: int, fx: float, fy: float, x: int, y: int, counts: dict[int, int], total_count: int, max_iters: int) -> tuple[int, int, int]:
    if iters == -1:
        return 0, 0, 0

    if True: # histogram mode
        '''SIZE = 360
        hue = 0
        for i in range(iters):
            if i in counts:
                hue += counts[i] / total_count
        hue *= SIZE'''
        if iters < max_iters:
            try:
                log_zn = math.log(fx*fx + fy*fy) / 2
            except ValueError:
                log_zn = 0.5
                print(f"log_zn value error when {fx=} and {fy=}")
            try:
                nu = math.log(abs(log_zn) / log_2) / log_2
            except ValueError:
                nu = 0.5
                print(f"value error when {log_zn=} and {log_2=}")
            iters = iters + 1 - nu
        '''if hue < 0:
            hue = 0
        if type(hue) == complex:
            print(f"{hue} is complex!")
            hue = hue.real'''
        try:
            #a = math.floor(hue)
            #b = math.floor(hue) + 1
            #x = hue % 1
            #interp = (b*x) + (a * (1-x))

            return _clean(_lerp(iters_to_color(math.floor(iters), max_iters), iters_to_color(math.floor(iters)+1, max_iters), iters % 1))
#            return _clean(_to_255(colorsys.hls_to_rgb( (interp/SIZE)**1.5 , 0.5, 1)))
        except ValueError:
            return 255, 255, 255
        #except TypeError as e:
        #    print(e)
        #    return 255, 255, 255
    else:
        if iters < 1000:
            log_zn = math.log(fx*fx + fy*fy) / 2
            nu = math.log(log_zn / log_2) / log_2
            iters = iters + 1 - nu

        color1 = colorsys.hls_to_rgb(math.floor(iters) / 1000, 0.5, 1)
        color2 = colorsys.hls_to_rgb((math.floor(iters) + 1) / 1000, 0.5, 1)
        return _clean(_to_255(_lerp(color1, color2, iters % 1)))

def color_counts_old(iters: int, fx: float, fy: float, x: int, y: int, counts: dict[int, int], max_c: int) -> tuple[int, int, int]:
    PAL_SIZE = 5000
    if iters == -1:
        return 0, 0, 0

    histogram_count = counts[iters]
    try:
        return _clean(_to_255(colorsys.hls_to_rgb((histogram_count % PAL_SIZE) / PAL_SIZE, 0.5, 1)))
    except ValueError:
        return 255, 0, 0