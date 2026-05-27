from PIL import Image
import math

# ==========================
# SETTINGS
# ==========================
SIZE = 256
MAX_ALPHA = 100

# Exponential curve strength
EXP_POWER = 2.2

# Normalized positions
# (0.0 = start of texture, 1.0 = end)

# Vertical edge gradients (left/right)
LEFT_START = -0.05
LEFT_END = 0.15

RIGHT_START = 1.05
RIGHT_END = 0.85

VERT_Y_START = 0.30
VERT_Y_END = 0.70


# Horizontal edge gradients (top/bottom)
TOP_START = 0.10
TOP_END = 0.30

BOTTOM_START = 0.90
BOTTOM_END = 0.70

HORZ_X_START = 0.15
HORZ_X_END = 0.85


# ==========================
# HELPERS
# ==========================
def clamp(v, a, b):
    return max(a, min(v, b))


def exp_gradient(t):
    """
    Exponential gradient:
    0 -> 0 alpha
    1 -> MAX_ALPHA
    """
    t = clamp(t, 0.0, 1.0)
    return (t ** EXP_POWER) * MAX_ALPHA


def norm_to_px(v):
    return v * SIZE


# Convert to pixels
left0 = norm_to_px(LEFT_START)
left1 = norm_to_px(LEFT_END)

right0 = norm_to_px(RIGHT_START)
right1 = norm_to_px(RIGHT_END)

top0 = norm_to_px(TOP_START)
top1 = norm_to_px(TOP_END)

bottom0 = norm_to_px(BOTTOM_START)
bottom1 = norm_to_px(BOTTOM_END)

vert_y0 = norm_to_px(VERT_Y_START)
vert_y1 = norm_to_px(VERT_Y_END)

horz_x0 = norm_to_px(HORZ_X_START)
horz_x1 = norm_to_px(HORZ_X_END)


# Corner centers
corner_radius = left1 - left0

corner_centers = [
    (left1, top1),         # top-left
    (right1, top1),        # top-right
    (left1, bottom1),      # bottom-left
    (right1, bottom1),     # bottom-right
]


# ==========================
# CREATE IMAGE
# ==========================
img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
pixels = img.load()

for y in range(SIZE):
    for x in range(SIZE):

        alpha = 0

        # =====================================
        # CENTER FILLED RECTANGLE
        # =====================================
        if (
            horz_x0 <= x <= horz_x1 and
            top1 <= y <= bottom1
        ):
            alpha = MAX_ALPHA

        # =====================================
        # LEFT GRADIENT
        # =====================================
        if vert_y0 <= y <= vert_y1:
            if left0 <= x <= left1:
                t = (x - left0) / (left1 - left0)
                alpha = max(alpha, exp_gradient(t))

        # =====================================
        # RIGHT GRADIENT
        # =====================================
        if vert_y0 <= y <= vert_y1:
            if right1 <= x <= right0:
                t = (right0 - x) / (right0 - right1)
                alpha = max(alpha, exp_gradient(t))

        # =====================================
        # TOP GRADIENT
        # =====================================
        if horz_x0 <= x <= horz_x1:
            if top0 <= y <= top1:
                t = (y - top0) / (top1 - top0)
                alpha = max(alpha, exp_gradient(t))

        # =====================================
        # BOTTOM GRADIENT
        # =====================================
        if horz_x0 <= x <= horz_x1:
            if bottom1 <= y <= bottom0:
                t = (bottom0 - y) / (bottom0 - bottom1)
                alpha = max(alpha, exp_gradient(t))

        # =====================================
        # CORNER RADIALS
        # =====================================
        for cx, cy in corner_centers:

            dx = x - cx
            dy = y - cy

            dist = math.sqrt(dx * dx + dy * dy)

            if dist <= corner_radius:

                # only draw into outer quadrant
                if (
                    (x <= cx and y <= cy) or
                    (x >= cx and y <= cy) or
                    (x <= cx and y >= cy) or
                    (x >= cx and y >= cy)
                ):

                    t = 1.0 - (dist / corner_radius)
                    alpha = max(alpha, exp_gradient(t))

        pixels[x, y] = (0, 0, 0, int(alpha))

# Save
img.save("rounded_gradient_mask.png")

print("Done: rounded_gradient_mask.png")