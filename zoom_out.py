import os
import random
import time

"""
(-0.7494430777229307, -0.04039854268783832, -0.7494430777228285, -0.04039854268773604)
(-1.1526604028060814, -0.30695505685455265, -1.1526604028056786, -0.3069550568541498)
(-0.1528374138507328, -1.0400350850739863, -0.15283741385027563, -1.0400350850735292)
(-1.8112662371017072, -2.3424589762138185e-10, -1.8112662366795607, 1.8790057629187405e-10)
(-0.7746269311970281, 0.12415248501499525, -0.7746269311875639, 0.1241524850244594)
"""

initial_zoom = my_zoom = (-0.7746269311970281, 0.12415248501499525, -0.7746269311875639, 0.1241524850244594)
initial_escape = my_escape = 10_000
target_zoom = (-2.5, -2, 1.5, 2)
target_escape = 1_000
from multiprocessing import Pool


def normalize(x):
    avg = sum(x) / len(x)
    return [v / avg for v in x]

def interp(a, b, factor):
    return (b * factor) + (a * (1-factor))

def interp_multi(a, b, factor):
    assert len(a) == len(b)
    return [interp(a[i], b[i], factor) for i in range(len(a))]

frame = 0

existing = set()
for fname in os.listdir("frames"):
    if ".png" in fname:
        existing.add(int(fname.replace(".png", "")))

zooms: list[tuple[int, list[float], int]] = []

while (my_zoom[0] - my_zoom[2])**2 + (my_zoom[1] - my_zoom[3])**2 < 25:
    if frame not in existing:
        zooms.append((frame, my_zoom, my_escape))
    #s.fill((0, 0, 0))
    #mbrot.draw(my_zoom, s)

    #pygame.image.save(s, f"frames/{frame:03}.png")

    frame += 1
    #diff = normalize([target_zoom[i] - my_zoom[i] for i in range(4)])
    #print(f"{diff=}")
    print(f"{my_zoom=}")
    interp_factor = ((frame/600)**16) / 20
    my_zoom = interp_multi(initial_zoom, target_zoom, interp_factor)#[my_zoom[i]+(diff[i] * 0.00000000000001/(abs(0.01*sum(my_zoom))**2)) for i in range(4)]
    my_escape = int(interp(initial_escape, target_escape, min(1.0, interp_factor*1.2)))
    #print(f"{my_zoom=}")

print(f"Generating {len(zooms)} frames...")

#complete_count = 0

def generate_frames(frame_set: list[tuple[int, list[float], int]]):
    id_ = ""
    #global complete_count
    import mbrot
    import pygame
    pygame.init()
    s = pygame.Surface((800, 800))
    for frame_id, z, escape_time in frame_set:
        print(f"{id_} generating frame {frame_id} with {escape_time=}")
        s.fill((0, 0, 0))
        print(f"{id_} filled frame {frame_id} with {escape_time=}")
        mbrot.draw(z, s, escape=escape_time)
        print(f"{id_} generated frame {frame_id} with {escape_time=}")
        pygame.image.save(s, f"frames/{frame_id:03}.png")
    print(f"Quitting {id_}")
    pygame.quit()
    #complete_count += 1

#threads = []
thread_count = 8
pools: list[list[tuple[int, list[float], int]]] = [list() for _ in range(thread_count)]

print("\n\n\n")

while len(zooms) > 0:
    random.choice(pools).append(zooms.pop())

print(pools)

print("Setup pools")
print("Starting threads")
#while len(pools) > 0:
#    thread = threading.Thread(target=generate_frames(pools.pop(), len(threads)))
#    threads.append(thread)
#    thread.start()

#while complete_count < thread_count:
#    print(complete_count)
#    time.sleep(1)

with Pool(thread_count) as p:
    p.map(generate_frames, pools)

print("Threads finished")
print("Generating video")

os.system(f'cd frames && ffmpeg -framerate 30 -pattern_type glob -i "*.png" -c:v libx264 -pix_fmt yuv420p "{time.time()}.mp4" && mv *.mp4 ../outputs/ && cd ..')

print("Done")