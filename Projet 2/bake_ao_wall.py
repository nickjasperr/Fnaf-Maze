from PIL import Image, ImageDraw
import math

def bake_ao_to_texture(image_path, output_path, left=False, right=False, bottom=False):
    try:
        base = Image.open(image_path).convert("RGBA")
        width, height = base.size
        overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        max_alpha = 120 # Bumped slightly since exponential falloff is thinner
        # Increase 'p' to make the shadow tighter to the edge
        # p = 1.0 is linear, p = 2.0 is quadratic, p = 3.0+ is very sharp
        p = 2.5 

        # --- BOTTOM ---
        if bottom:
            grad_h = int(height * 0.5) # Made slightly larger to accommodate falloff
            start_y = height - grad_h
            for y in range(grad_h):
                # Exponential: (ratio)^p
                ratio = y / grad_h
                alpha = int(math.pow(ratio, p) * max_alpha)
                draw.line([(0, start_y + y), (width, start_y + y)], fill=(0, 0, 0, alpha))
            
        # --- LEFT ---
        if left:
            grad_w_left = int(width * 0.3)
            for x in range(grad_w_left):
                # Reverse exponential: (1 - ratio)^p
                ratio = x / grad_w_left
                alpha = int(math.pow(1 - ratio, p) * max_alpha)
                draw.line([(x, 0), (x, height)], fill=(0, 0, 0, alpha))

        # --- RIGHT ---
        if right:
            grad_w_right = int(width * 0.3)
            start_x = width - grad_w_right
            for x in range(grad_w_right):
                ratio = x / grad_w_right
                alpha = int(math.pow(ratio, p) * max_alpha)
                draw.line([(start_x + x, 0), (start_x + x, height)], fill=(0, 0, 0, alpha))
            
        combined = Image.alpha_composite(base, overlay)
        combined.convert("RGB").save(output_path)
        print(f"Baking successful (Exponential): {output_path}")

    except FileNotFoundError:
        print(f"Error: Could not find {image_path}")

name = "tresorBoite";

bake_ao_to_texture(
    image_path= name + ".jpg", 
    output_path= name + "_ao.jpg", 
    left=False, 
    right=False, 
    bottom=True
)