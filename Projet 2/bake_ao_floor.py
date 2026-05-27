import os
from PIL import Image, ImageDraw
import math

# Settings
SIZE = 256
MAX_ALPHA = 100  # Slightly higher to make the exponential curve feel meaty
P = 2.5          # Exponential curve power
WIDTH_RATIO = 0.3
GRAD_LEN = int(SIZE * WIDTH_RATIO)

def create_base_canvas():
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))

def save_tex(img, name):
    if not os.path.exists('textures'): os.makedirs('textures')
    img.save(f"textures/{name}.png")
    print(f"Generated: textures/{name}.png")

def generate_textures():
    # --- 1. CARDINAL SIDES (N, S, E, W) ---
    directions = {
        'grad_n': lambda x, y: y / GRAD_LEN,
        'grad_s': lambda x, y: (SIZE - 1 - y) / GRAD_LEN,
        'grad_w': lambda x, y: x / GRAD_LEN,
        'grad_e': lambda x, y: (SIZE - 1 - x) / GRAD_LEN
    }

    for name, logic in directions.items():
        img = create_base_canvas()
        pixels = img.load()
        for y in range(SIZE):
            for x in range(SIZE):
                ratio = logic(x, y)
                if 0 <= ratio <= 1:
                    # Exponential falloff: (1 - ratio)^p
                    alpha = int(math.pow(1 - ratio, P) * MAX_ALPHA)
                    pixels[x, y] = (0, 0, 0, alpha)
        save_tex(img, name)

    # --- 2. CORNER RADIALS (NW, NE, SW, SE) ---
    # Logic: distance from corner / GRAD_LEN
    corners = {
        'grad_nw': (0, 0),
        'grad_ne': (SIZE - 1, 0),
        'grad_sw': (0, SIZE - 1),
        'grad_se': (SIZE - 1, SIZE - 1)
    }

    for name, (cx, cy) in corners.items():
        img = create_base_canvas()
        pixels = img.load()
        for y in range(SIZE):
            for x in range(SIZE):
                # Euclidean distance for radial look
                dist = math.sqrt((x - cx)**2 + (y - cy)**2)
                ratio = dist / GRAD_LEN
                if ratio <= 1:
                    alpha = int(math.pow(1 - ratio, P) * MAX_ALPHA)
                    pixels[x, y] = (0, 0, 0, alpha)
        save_tex(img, name)

    # --- 3. THE PLAIN FLOOR ---
    # Just a dummy placeholder or solid color if you need it generated
    plain = Image.new("RGBA", (SIZE, SIZE), (255, 255, 255, 255))
    save_tex(plain, "floor_plain")

if __name__ == "__main__":
    generate_textures()