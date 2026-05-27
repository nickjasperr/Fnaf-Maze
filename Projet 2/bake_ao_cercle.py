from PIL import Image
import math

SIZE = 512

CENTER_X = SIZE / 2
CENTER_Y = SIZE / 2

# Your radii in image-space:
# center to edge = 0.5
SOLID_RADIUS = 0.3
OUTER_RADIUS = 0.5

MAX_ALPHA = 100

img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
pixels = img.load()

for y in range(SIZE):
    for x in range(SIZE):

        dx = x - CENTER_X
        dy = y - CENTER_Y

        # Normalize using full image size
        dist = math.sqrt(dx * dx + dy * dy) / SIZE

        alpha = 0

        if dist <= SOLID_RADIUS:
            # Solid center
            alpha = MAX_ALPHA

        elif dist <= OUTER_RADIUS:
            # Exponential fade
            t = (dist - SOLID_RADIUS) / (OUTER_RADIUS - SOLID_RADIUS)

            fade = math.exp(-5 * t)

            # Normalize exponential to hit 0 exactly at edge
            edge_val = math.exp(-5)
            fade = (fade - edge_val) / (1 - edge_val)

            alpha = int(MAX_ALPHA * fade)

        pixels[x, y] = (0, 0, 0, alpha)

img.save("gradient_circle.png")
print("Saved gradient_circle.png")