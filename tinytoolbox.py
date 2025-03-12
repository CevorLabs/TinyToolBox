import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, scrolledtext
import os
import shutil
import hashlib
import json
import requests
import random
import string
from PIL import Image, ImageTk
import qrcode
from cryptography.fernet import Fernet
import time
import psutil

def text_to_uppercase(text):
    return text.upper()

def text_to_lowercase(text):
    return text.lower()

def text_to_titlecase(text):
    return text.title()

def text_to_leetspeak(text):
    leet_dict = {"a": "4", "e": "3", "i": "1", "o": "0", "s": "5", "t": "7"}
    return "".join(leet_dict.get(char.lower(), char) for char in text)

def text_to_morse(text):
    morse_dict = {"a": ".-", "b": "-...", "c": "-.-.", "d": "-..", "e": ".", "f": "..-.",
                  "g": "--.", "h": "....", "i": "..", "j": ".---", "k": "-.-", "l": ".-..",
                  "m": "--", "n": "-.", "o": "---", "p": ".--.", "q": "--.-", "r": ".-.",
                  "s": "...", "t": "-", "u": "..-", "v": "...-", "w": ".--", "x": "-..-",
                  "y": "-.--", "z": "--.."}
    return " ".join(morse_dict.get(char.lower(), "") for char in text)

def reverse_text(text):
    return text[::-1]

def count_words(text):
    return len(text.split())

def count_characters(text):
    return len(text)

def generate_random_text(style="lorem"):
    lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    quotes = ["Be the change you wish to see in the world.", "Stay hungry, stay foolish."]
    return lorem if style == "lorem" else random.choice(quotes)

def rename_files_in_folder(folder_path, prefix):
    for count, filename in enumerate(os.listdir(folder_path)):
        dst = f"{prefix}_{str(count + 1)}.{filename.split('.')[-1]}"
        src = os.path.join(folder_path, filename)
        dst = os.path.join(folder_path, dst)
        os.rename(src, dst)
    return f"Renamed {count + 1} files."

def find_and_delete_duplicates(folder_path):
    unique_files = {}
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_hash = hashlib.md5(open(file_path, "rb").read()).hexdigest()
            if file_hash in unique_files:
                os.remove(file_path)
                print(f"Deleted duplicate: {filename}")
            else:
                unique_files[file_hash] = filename
    return "Duplicate files deleted."

def get_system_info():
    info = {
        "OS": os.name,
        "CPU": psutil.cpu_percent(),
        "RAM": psutil.virtual_memory().percent,
        "Disk": psutil.disk_usage("/").percent
    }
    return info

def ping_website(url):
    try:
        response = requests.get(url)
        return f"Website is online. Status code: {response.status_code}"
    except requests.exceptions.RequestException:
        return "Website is offline."

def get_ip_info():
    response = requests.get("https://ipinfo.io")
    return response.json()

def shorten_url(url):
    response = requests.get(f"http://tinyurl.com/api-create.php?url={url}")
    return response.text

def expand_url(short_url):
    response = requests.get(short_url)
    return response.url

def generate_password(length=12, use_symbols=True):
    chars = string.ascii_letters + string.digits
    if use_symbols:
        chars += string.punctuation
    return "".join(random.choice(chars) for _ in range(length))

def encrypt_text(text, key):
    cipher = Fernet(key)
    return cipher.encrypt(text.encode()).decode()

def decrypt_text(encrypted_text, key):
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_text.encode()).decode()

def hash_file(file_path, algorithm="sha256"):
    hasher = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def convert_image(input_path, output_format):
    img = Image.open(input_path)
    output_path = os.path.splitext(input_path)[0] + f".{output_format}"
    img.save(output_path)
    return f"Image saved as {output_path}"

def convert_units(value, from_unit, to_unit):
    conversions = {
        "length": {"m": 1, "ft": 3.28084},
        "weight": {"kg": 1, "lb": 2.20462},
        "temperature": {"c": lambda x: x * 9/5 + 32, "f": lambda x: (x - 32) * 5/9}
    }
    if from_unit in conversions["length"] and to_unit in conversions["length"]:
        return value * conversions["length"][to_unit] / conversions["length"][from_unit]
    elif from_unit in conversions["weight"] and to_unit in conversions["weight"]:
        return value * conversions["weight"][to_unit] / conversions["weight"][from_unit]
    elif from_unit in conversions["temperature"] and to_unit in conversions["temperature"]:
        return conversions["temperature"][to_unit](value)
    else:
        return "Unsupported conversion."

def convert_number(value, from_base, to_base):
    bases = {"binary": 2, "decimal": 10, "hex": 16}
    return int(str(value), bases[from_base])

todo_list = []

def add_todo(task):
    todo_list.append(task)
    return f"Added: {task}"

def list_todos():
    return "\n".join(f"{i + 1}. {task}" for i, task in enumerate(todo_list))

def delete_todo(index):
    if 0 <= index < len(todo_list):
        deleted = todo_list.pop(index)
        return f"Deleted: {deleted}"
    else:
        return "Invalid index."

def generate_qr_code(data, output_path="qrcode.png"):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save(output_path)
    return f"QR code saved as {output_path}"

def roll_dice():
    return random.randint(1, 6)

def flip_coin():
    return random.choice(["Heads", "Tails"])

class TinyToolboxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TinyToolbox")
        self.root.geometry("800x600")

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        self.output_text = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, width=80, height=20)
        self.output_text.pack(pady=10)

        ttk.Button(self.main_frame, text="Text Utilities", command=self.open_text_utilities).pack(pady=5)
        ttk.Button(self.main_frame, text="File Utilities", command=self.open_file_utilities).pack(pady=5)
        ttk.Button(self.main_frame, text="Internet Tools", command=self.open_internet_tools).pack(pady=5)
        ttk.Button(self.main_frame, text="Security Tools", command=self.open_security_tools).pack(pady=5)
        ttk.Button(self.main_frame, text="Conversion Tools", command=self.open_conversion_tools).pack(pady=5)
        ttk.Button(self.main_frame, text="Miscellaneous", command=self.open_misc_tools).pack(pady=5)

    def display_result(self, result):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, result)

    def open_text_utilities(self):
        text_window = tk.Toplevel(self.root)
        text_window.title("Text Utilities")

        ttk.Label(text_window, text="Enter Text:").pack(pady=5)
        self.text_input = ttk.Entry(text_window, width=50)
        self.text_input.pack(pady=5)

        ttk.Button(text_window, text="Uppercase", command=lambda: self.display_result(text_to_uppercase(self.text_input.get()))).pack(pady=5)
        ttk.Button(text_window, text="Lowercase", command=lambda: self.display_result(text_to_lowercase(self.text_input.get()))).pack(pady=5)
        ttk.Button(text_window, text="Leetspeak", command=lambda: self.display_result(text_to_leetspeak(self.text_input.get()))).pack(pady=5)
        ttk.Button(text_window, text="Morse Code", command=lambda: self.display_result(text_to_morse(self.text_input.get()))).pack(pady=5)

    def open_file_utilities(self):
        file_window = tk.Toplevel(self.root)
        file_window.title("File Utilities")

        ttk.Button(file_window, text="Rename Files", command=self.rename_files).pack(pady=10)
        ttk.Button(file_window, text="Delete Duplicates", command=self.delete_duplicates).pack(pady=10)
        ttk.Button(file_window, text="System Info", command=lambda: self.display_result(str(get_system_info()))).pack(pady=10)

    def rename_files(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            prefix = simpledialog.askstring("Prefix", "Enter prefix for files:")
            if prefix:
                self.display_result(rename_files_in_folder(folder_path, prefix))

    def delete_duplicates(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.display_result(find_and_delete_duplicates(folder_path))

    def open_internet_tools(self):
        internet_window = tk.Toplevel(self.root)
        internet_window.title("Internet Tools")

        ttk.Button(internet_window, text="Ping Website", command=self.ping_website).pack(pady=10)
        ttk.Button(internet_window, text="Get IP Info", command=lambda: self.display_result(str(get_ip_info()))).pack(pady=10)
        ttk.Button(internet_window, text="Shorten URL", command=self.shorten_url).pack(pady=10)
        ttk.Button(internet_window, text="Expand URL", command=self.expand_url).pack(pady=10)

    def ping_website(self):
        url = simpledialog.askstring("Ping Website", "Enter URL:")
        if url:
            self.display_result(ping_website(url))

    def shorten_url(self):
        url = simpledialog.askstring("Shorten URL", "Enter URL:")
        if url:
            self.display_result(shorten_url(url))

    def expand_url(self):
        short_url = simpledialog.askstring("Expand URL", "Enter Short URL:")
        if short_url:
            self.display_result(expand_url(short_url))

    def open_security_tools(self):
        security_window = tk.Toplevel(self.root)
        security_window.title("Security Tools")

        ttk.Button(security_window, text="Generate Password", command=self.generate_password).pack(pady=10)
        ttk.Button(security_window, text="Encrypt Text", command=self.encrypt_text).pack(pady=10)
        ttk.Button(security_window, text="Decrypt Text", command=self.decrypt_text).pack(pady=10)
        ttk.Button(security_window, text="Hash File", command=self.hash_file).pack(pady=10)

    def generate_password(self):
        length = simpledialog.askinteger("Password Length", "Enter length:")
        if length:
            self.display_result(generate_password(length))

    def encrypt_text(self):
        text = simpledialog.askstring("Encrypt Text", "Enter text:")
        if text:
            key = Fernet.generate_key()
            self.display_result(f"Key: {key.decode()}\nEncrypted: {encrypt_text(text, key)}")

    def decrypt_text(self):
        encrypted_text = simpledialog.askstring("Decrypt Text", "Enter encrypted text:")
        if encrypted_text:
            key = simpledialog.askstring("Decryption Key", "Enter key:")
            if key:
                self.display_result(decrypt_text(encrypted_text, key))

    def hash_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.display_result(hash_file(file_path))

    def open_conversion_tools(self):
        conversion_window = tk.Toplevel(self.root)
        conversion_window.title("Conversion Tools")

        ttk.Button(conversion_window, text="Convert Image", command=self.convert_image).pack(pady=10)
        ttk.Button(conversion_window, text="Convert Units", command=self.convert_units).pack(pady=10)
        ttk.Button(conversion_window, text="Convert Number", command=self.convert_number).pack(pady=10)

    def convert_image(self):
        input_path = filedialog.askopenfilename()
        if input_path:
            output_format = simpledialog.askstring("Output Format", "Enter format (e.g., png):")
            if output_format:
                self.display_result(convert_image(input_path, output_format))

    def convert_units(self):
        value = simpledialog.askfloat("Value", "Enter value:")
        if value:
            from_unit = simpledialog.askstring("From Unit", "Enter from unit (e.g., m):")
            if from_unit:
                to_unit = simpledialog.askstring("To Unit", "Enter to unit (e.g., ft):")
                if to_unit:
                    self.display_result(convert_units(value, from_unit, to_unit))

    def convert_number(self):
        value = simpledialog.askstring("Value", "Enter value:")
        if value:
            from_base = simpledialog.askstring("From Base", "Enter from base (e.g., binary):")
            if from_base:
                to_base = simpledialog.askstring("To Base", "Enter to base (e.g., decimal):")
                if to_base:
                    self.display_result(convert_number(value, from_base, to_base))

    def open_misc_tools(self):
        misc_window = tk.Toplevel(self.root)
        misc_window.title("Miscellaneous")

        ttk.Button(misc_window, text="Add To-Do", command=self.add_todo).pack(pady=10)
        ttk.Button(misc_window, text="List To-Dos", command=lambda: self.display_result(list_todos())).pack(pady=10)
        ttk.Button(misc_window, text="Delete To-Do", command=self.delete_todo).pack(pady=10)
        ttk.Button(misc_window, text="Generate QR Code", command=self.generate_qr_code).pack(pady=10)
        ttk.Button(misc_window, text="Roll Dice", command=lambda: self.display_result(roll_dice())).pack(pady=10)
        ttk.Button(misc_window, text="Flip Coin", command=lambda: self.display_result(flip_coin())).pack(pady=10)

    def add_todo(self):
        task = simpledialog.askstring("Add To-Do", "Enter task:")
        if task:
            self.display_result(add_todo(task))

    def delete_todo(self):
        index = simpledialog.askinteger("Delete To-Do", "Enter index:")
        if index:
            self.display_result(delete_todo(index - 1))

    def generate_qr_code(self):
        data_types = ["Link", "Email", "Phone Number", "Discord", "Plain Text"]
        data_type = simpledialog.askstring("Data Type", "Choose data type (Link, Email, Phone Number, Discord, Plain Text):")
        if data_type and data_type.lower() in [dt.lower() for dt in data_types]:
            if data_type.lower() == "link":
                data = simpledialog.askstring("Link", "Enter URL:")
                if data:
                    self.display_result(generate_qr_code(data))
            elif data_type.lower() == "email":
                email = simpledialog.askstring("Email", "Enter email address:")
                if email:
                    self.display_result(generate_qr_code(f"mailto:{email}"))
            elif data_type.lower() == "phone number":
                phone = simpledialog.askstring("Phone Number", "Enter phone number:")
                if phone:
                    self.display_result(generate_qr_code(f"tel:{phone}"))
            elif data_type.lower() == "discord":
                discord = simpledialog.askstring("Discord", "Enter Discord invite code:")
                if discord:
                    self.display_result(generate_qr_code(f"https://discord.gg/{discord}"))
            elif data_type.lower() == "plain text":
                text = simpledialog.askstring("Plain Text", "Enter text:")
                if text:
                    self.display_result(generate_qr_code(text))
        else:
            self.display_result("Invalid data type selected.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TinyToolboxApp(root)
    root.mainloop()