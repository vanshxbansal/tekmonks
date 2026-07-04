"""Generate a README screenshot from test_all.py output."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from test_all import build_output

OUTPUT_PATH = Path(__file__).parent / "output_screenshot.png"
BG_COLOR = "#1e1e2e"
TEXT_COLOR = "#cdd6f4"
ACCENT_COLOR = "#89b4fa"
MUTED_COLOR = "#6c7086"
PADDING = 32
LINE_HEIGHT = 22


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/cour.ttf",
        "C:/Windows/Fonts/lucon.ttf",
    ]
    if bold:
        candidates = ["C:/Windows/Fonts/consolab.ttf", *candidates]

    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def colorize_line(line: str) -> str:
    return line


def render_screenshot(text: str, output_path: Path) -> None:
    font = load_font(15)
    font_bold = load_font(16, bold=True)

    lines = text.splitlines()
    widths = []
    for line in lines:
        current_font = font_bold if (
            "CLASSIC INTERVIEW" in line
            or line.strip().startswith(tuple("1234"))
            or line.strip().startswith("▸")
            or line.strip().startswith("All test")
        ) else font
        widths.append(current_font.getlength(line))
    max_width = max(widths, default=400)
    img_width = int(max_width) + PADDING * 2 + 20
    img_height = len(lines) * LINE_HEIGHT + PADDING * 2

    image = Image.new("RGB", (img_width, img_height), BG_COLOR)
    draw = ImageDraw.Draw(image)

    y = PADDING
    for line in lines:
        if line.startswith("═"):
            draw.line(
                [(PADDING, y + 10), (img_width - PADDING, y + 10)],
                fill=ACCENT_COLOR,
                width=1,
            )
        elif "CLASSIC INTERVIEW" in line or line.strip().startswith(tuple("1234")):
            draw.text((PADDING, y), line, font=font_bold, fill=ACCENT_COLOR)
        elif line.strip().startswith("▸"):
            draw.text((PADDING, y), line, font=font_bold, fill="#a6e3a1")
        elif "Problem" in line or "Approach" in line or "Formula" in line or "Graph type" in line:
            draw.text((PADDING, y), line, font=font, fill="#f9e2af")
        elif line.strip().startswith("All test"):
            draw.text((PADDING, y), line, font=font_bold, fill="#a6e3a1")
        else:
            draw.text((PADDING, y), line, font=font, fill=TEXT_COLOR)
        y += LINE_HEIGHT

    image.save(output_path)
    print(f"Screenshot saved to {output_path}")


def main() -> None:
    output_text = build_output()
    render_screenshot(output_text, OUTPUT_PATH)


if __name__ == "__main__":
    main()
