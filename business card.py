from PIL import Image, ImageDraw, ImageFont
import qrcode
import os
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox


def build_instagram_url(insta_input: str):
    """Normalize various Instagram inputs into a full URL that QR scanners will open."""
    if not insta_input:
        return None

    s = insta_input.strip()

    # If already full URL
    if s.startswith("http://") or s.startswith("https://"):
        return s

    # If contains instagram.com but missing http
    if "instagram.com" in s:
        if s.startswith("//"):
            return "https:" + s
        return "https://" + s.lstrip("/")

    # If starts with @, remove it
    if s.startswith("@"):
        s = s[1:]

    return f"https://instagram.com/{s}"


def generate_business_card(name, title, phone, email, website, instagram_input,
                           background_path=None, photo_path=None):
    try:
        if not name:
            messagebox.showerror("Input Error", "Name is required.")
            return None

        instagram_url = build_instagram_url(instagram_input)
        if not instagram_url:
            messagebox.showerror("Input Error", "Instagram link or handle is required.")
            return None

        # Output folder
        output_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        os.makedirs(output_dir, exist_ok=True)

        # Card size
        card_width, card_height = 800, 400
        card = Image.new("RGBA", (card_width, card_height), (255, 255, 255, 255))

        # Load background image
        if background_path:
            try:
                bg = Image.open(background_path).convert("RGBA")
                bg = bg.resize((card_width, card_height), Image.LANCZOS)
                card.paste(bg, (0, 0))   # No transparency – user sees full background
            except Exception as e:
                messagebox.showwarning("Background Error", f"Could not load background:\n{e}")

        draw = ImageDraw.Draw(card)

        # Load fonts
        try:
            font_large = ImageFont.truetype("arial.ttf", 40)
            font_small = ImageFont.truetype("arial.ttf", 22)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

        text_x = 50
        y = 50
        text_color = (0, 0, 0)  # Black text (change if needed)

        # Write text directly on background
        draw.text((text_x, y), name, font=font_large, fill=text_color)
        y += 60

        if title:
            draw.text((text_x, y), title, font=font_small, fill=text_color)
            y += 40
        if phone:
            draw.text((text_x, y), f"Phone: {phone}", font=font_small, fill=text_color)
            y += 30
        if email:
            draw.text((text_x, y), f"Email: {email}", font=font_small, fill=text_color)
            y += 30
        if website:
            draw.text((text_x, y), f"Website: {website}", font=font_small, fill=text_color)
            y += 30
        if instagram_input:
            draw.text((text_x, y), f"Instagram: {instagram_input}", font=font_small, fill=text_color)
            y += 30

        # Generate QR code
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=4, border=2)
        qr.add_data(instagram_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

        qr_size = 160
        qr_img = qr_img.resize((qr_size, qr_size), Image.NEAREST)
        qr_x = card_width - qr_size - 40
        qr_y = card_height - qr_size - 40

        # Paste profile photo above QR
        if photo_path:
            try:
                photo = Image.open(photo_path).convert("RGBA")
                photo.thumbnail((qr_size, 120), Image.LANCZOS)
                photo_x = qr_x
                photo_y = qr_y - photo.height - 12
                card.paste(photo, (photo_x, photo_y), photo)
            except Exception as e:
                messagebox.showwarning("Photo Error", f"Could not load photo:\n{e}")

        # Paste QR code
        card.paste(qr_img, (qr_x, qr_y), qr_img)

        # Save card
        filename = f"{name.replace(' ', '_')}_card.png"
        save_path = os.path.join(output_dir, filename)
        card.save(save_path)

        messagebox.showinfo("Success", f"Business card saved at:\n{save_path}\n\nScan QR to open Instagram!")
        return save_path

    except Exception as ex:
        messagebox.showerror("Error", f"Unexpected error:\n{ex}")
        return None


def main():
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo("Digital Business Card", "Select a background image (optional).")

    background_path = filedialog.askopenfilename(
        title="Select background image",
        filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*")]
    )
    if background_path == "":
        background_path = None

    name = simpledialog.askstring("Input", "Enter your name:")
    title = simpledialog.askstring("Input", "Enter your title (optional):")
    phone = simpledialog.askstring("Input", "Enter your phone number (optional):")
    email = simpledialog.askstring("Input", "Enter your email (optional):")
    website = simpledialog.askstring("Input", "Enter your website (optional):")
    instagram = simpledialog.askstring("Input", "Enter Instagram handle or URL:")

    photo_path = filedialog.askopenfilename(
        title="Select photo (optional)",
        filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*")]
    )
    if photo_path == "":
        photo_path = None

    generate_business_card(name, title, phone, email, website, instagram, background_path, photo_path)


if __name__ == "__main__":
    main()

