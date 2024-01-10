import pygame
pygame.init()

inp_orig = pygame.image.load("input.png")
# get square subsection of input image (dynamically based on width and height)
size = min(inp_orig.get_width(), inp_orig.get_height())
inp = pygame.Surface((size, size))
inp.blit(inp_orig, (0, 0), (0, 0, size, size))

OUT_SCALE = 4 * 4 # must be pow2 at least 4
HALF_SIZE = size * OUT_SCALE / 2
QUARTER_SIZE = HALF_SIZE / 2
inp = pygame.transform.scale(inp, (HALF_SIZE, HALF_SIZE))

out = pygame.Surface((size * OUT_SCALE, size * OUT_SCALE), pygame.SRCALPHA)
out.fill((0, 0, 0, 0))

# draw the first 'triangle'
for _ in range(5):
    out.fill((0, 0, 0, 0))
    out.blit(inp, (QUARTER_SIZE, 0))
    out.blit(inp, (0, HALF_SIZE))
    out.blit(inp, (HALF_SIZE, HALF_SIZE))

    inp = pygame.transform.scale(out, (HALF_SIZE, HALF_SIZE))

pygame.image.save(out, "output.png")