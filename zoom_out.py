import os
import random
import time

initial_zoom = my_zoom = (-0.7494430777229307, -0.04039854268783832, -0.7494430777228285, -0.04039854268773604)
target_zoom = (-2.5, -2, 1.5, 2)
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

zooms: list[tuple[int, list[float]]] = []

while (my_zoom[0] - my_zoom[2])**2 + (my_zoom[1] - my_zoom[3])**2 < 25:
    zooms.append((frame, my_zoom))
    #s.fill((0, 0, 0))
    #mbrot.draw(my_zoom, s)

    #pygame.image.save(s, f"frames/{frame:03}.png")

    frame += 1
    #diff = normalize([target_zoom[i] - my_zoom[i] for i in range(4)])
    #print(f"{diff=}")
    print(f"{my_zoom=}")
    my_zoom = interp_multi(initial_zoom, target_zoom, ((frame/600)**16) / 20)#[my_zoom[i]+(diff[i] * 0.00000000000001/(abs(0.01*sum(my_zoom))**2)) for i in range(4)]
    #print(f"{my_zoom=}")

print(f"Generating {len(zooms)} frames...")

#complete_count = 0

def generate_frames(frame_set: list[tuple[int, list[float]]]):
    id_ = ""
    #global complete_count
    import mbrot
    import pygame
    pygame.init()
    s = pygame.Surface((800, 800))
    for frame_id, z in frame_set:
        print(f"{id_} generating frame {frame_id}")
        s.fill((0, 0, 0))
        print(f"{id_} filled frame {frame_id}")
        mbrot.draw(z, s)
        print(f"{id_} generated frame {frame_id}")
        pygame.image.save(s, f"frames/{frame_id:03}.png")
    print(f"Quitting {id_}")
    pygame.quit()
    #complete_count += 1

#threads = []
thread_count = 128
pools: list[list[tuple[int, list[float]]]] = [list() for _ in range(thread_count)]

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

os.system(r'cd frames && ffmpeg -framerate 30 -pattern_type glob -i "*.png" -c:v libx264 -pix_fmt yuv420p out.mp4 && cd ..')

print("Done")