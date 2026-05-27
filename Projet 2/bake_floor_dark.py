from PIL import Image

img = Image.open("floor.jpg").convert("RGBA")
overlay = Image.new("RGBA", img.size, (0, 0, 0, 100))
result = Image.alpha_composite(img, overlay)
result.save("floor_darkened.png")