from PIL import Image, ImageDraw, ImageFont

def contains_arabic(text):
    return any('\u0600' <= c <= '\u06FF' for c in text)

def add_name_to_gif(input_gif_path, output_gif_path, name_text, eng_font_path="Poppins.ttf", ar_font_path="Janna.ttf", font_size=40):
    gif = Image.open(input_gif_path)
    frames = []
    duration = gif.info.get('duration', 100)

    font_path = ar_font_path if contains_arabic(name_text) else eng_font_path

    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Warning: Font not found! Using default font.")
        font = ImageFont.load_default()

    button_color = (142, 91, 250, 255)

    try:
        while True:
            frame = gif.copy().convert("RGBA")
            draw = ImageDraw.Draw(frame)

            width, height = frame.size
            bbox = draw.textbbox((0, 0), name_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            button_width = text_width + 120
            button_height = text_height + 50
            button_x0 = (width - button_width) / 2
            button_y0 = height - button_height - 60
            button_x1 = button_x0 + button_width
            button_y1 = button_y0 + button_height

            draw.rounded_rectangle(
                [(button_x0 + 3, button_y0 + 3), (button_x1 + 3, button_y1 + 3)],
                radius=button_height / 2,
                fill=(0, 0, 0, 80)
            )

            draw.rounded_rectangle(
                [(button_x0, button_y0), (button_x1, button_y1)],
                radius=button_height / 2,
                fill=button_color
            )

            text_x = button_x0 + (button_width - text_width) / 2
            text_y = button_y0 + (button_height - text_height) / 2 - bbox[1] - 4
            draw.text((text_x, text_y), name_text, font=font, fill="white")

            frames.append(frame.convert("P"))
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    frames[0].save(
        output_gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0
    )
