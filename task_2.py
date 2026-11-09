import argparse
import math


def draw_tree(x, y, length, angle, depth, segments):
    end_x = x + length * math.cos(angle)
    end_y = y + length * math.sin(angle)
    segments.append((x, y, end_x, end_y))
    if depth > 0:
        branch_length = length / math.sqrt(2)
        draw_tree(end_x, end_y, branch_length, angle + math.pi / 4, depth - 1, segments)
        draw_tree(end_x, end_y, branch_length, angle - math.pi / 4, depth - 1, segments)


def draw_line(canvas, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        return
    if abs(dx) > 2 * abs(dy):
        symbol = "-"
    elif abs(dy) > 2 * abs(dx):
        symbol = "|"
    else:
        symbol = "\\" if dx * dy > 0 else "/"
    for step in range(steps + 1):
        x = round(x1 + dx * step / steps)
        y = round(y1 + dy * step / steps)
        old = canvas[y][x]
        canvas[y][x] = symbol if old in (" ", symbol) else "+"


def render_tree(depth, width=100, height=40):
    if not 0 <= depth <= 10:
        raise ValueError("Рівень рекурсії має бути від 0 до 10")
    if width < 10 or height < 5:
        raise ValueError("Розмір полотна замалий")

    segments = []
    draw_tree(0, 0, 100, -math.pi / 2, depth, segments)
    min_x = min(min(x1, x2) for x1, _, x2, _ in segments)
    max_x = max(max(x1, x2) for x1, _, x2, _ in segments)
    min_y = min(min(y1, y2) for _, y1, _, y2 in segments)
    max_y = max(max(y1, y2) for _, y1, _, y2 in segments)

    # Символи консолі вищі за свою ширину, тому вісь Y стискаємо вдвічі.
    scale = min((width - 3) / max(max_x - min_x, 1),
                2 * (height - 3) / max(max_y - min_y, 1))
    offset_x = (width - (max_x - min_x) * scale) / 2
    offset_y = (height - (max_y - min_y) * scale / 2) / 2

    def point(x, y):
        return (round(offset_x + (x - min_x) * scale),
                round(offset_y + (y - min_y) * scale / 2))

    canvas = [[" "] * width for _ in range(height)]
    for x1, y1, x2, y2 in segments:
        draw_line(canvas, *point(x1, y1), *point(x2, y2))
    return "\n".join("".join(row).rstrip() for row in canvas).strip("\n")


def main():
    parser = argparse.ArgumentParser(description="Намалювати дерево Піфагора в консолі")
    parser.add_argument("depth", type=int, nargs="?", help="рівень рекурсії від 0 до 10")
    parser.add_argument("--width", type=int, default=100, help="ширина в символах (типово 100)")
    parser.add_argument("--height", type=int, default=40, help="висота в рядках (типово 40)")
    args = parser.parse_args()
    try:
        depth = args.depth if args.depth is not None else int(input("Вкажіть рівень рекурсії (0–10): "))
        print(render_tree(depth, args.width, args.height))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
