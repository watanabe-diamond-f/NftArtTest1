from curses import start_color
from PIL import Image, ImageDraw, ImageChops
import random
import colorsys

def generate_art(path: str):
    print("test")
    target_size_px = 128
    scale_factor = 2
    image_size_px = target_size_px * scale_factor
    padding_px = 12 * scale_factor
    image_bg_color = (0, 0, 0)
    start_color = random_color()
    end_color = random_color()
    image = Image.new("RGB", size=(image_size_px, image_size_px), color=image_bg_color)

    draw = ImageDraw.Draw(image)
    points = []

    # 描画範囲処理
    # 線を増減したい場合はrangeの中を減らしてください。最小数は2です
    for _ in range(10):
        random_point = (
            random.randint(padding_px, image_size_px - padding_px),
            random.randint(padding_px, image_size_px - padding_px)
        )
        points.append(random_point)

    # 枠作成処理
    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])
    # draw.rectangle((min_x, min_y, max_x, max_y), outline=(255, 0, 0))

    # 中央描画処理
    delta_x = min_x - (image_size_px - max_x)
    delta_y = min_y - (image_size_px - max_y)
    for i, point in enumerate(points):
        points[i] = (point[0] - delta_x // 2, point[1] - delta_y // 2)

    # 描画処理
    thickness = 0
    n_points = len(points) - 1
    for i, point in enumerate(points):

        # Overlay cancas
        overlay_image = Image.new("RGB", size=(image_size_px, image_size_px), color=image_bg_color)
        overlay_draw = ImageDraw.Draw(overlay_image)

        p1 = point

        if i == n_points:
            p2 = points[0]
        else:
            p2 = points[i + 1]

        line_xy = (p1, p2)
        color_factor = i / n_points
        line_color = interpolate(start_color, end_color, color_factor)
        thickness += scale_factor
        overlay_draw.line(line_xy, fill=line_color, width=thickness)
        image = ImageChops.add(image, overlay_image)

    image = image.resize((target_size_px, target_size_px), resample=Image.ANTIALIAS)
    image.save(path)

def random_color():
    h = random.random()
    s = 1
    v = 1

    float_rgb = colorsys.hsv_to_rgb(h, s, v)
    rgb = [int(x * 255) for x in float_rgb]

    return tuple(rgb)

def interpolate(start_color, end_color, factor: float):
    recip = 1 - factor
    return (
        int(start_color[0] * recip + end_color[0] * factor),
        int(start_color[1] * recip + end_color[1] * factor),
        int(start_color[2] * recip + end_color[2] * factor),
    )

if __name__ == "__main__":
    # 描画ファイルを増減したい場合はrangeの中を変更してください
    for i in range(10):
        generate_art(f"test_image_{i}.png")