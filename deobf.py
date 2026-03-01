import base64
import tkinter as tk
from tkinter import messagebox

def atbash_cipher(text):
    res = ""
    for char in text:
        if 'a' <= char <= 'z':
            res += chr(ord('a') + (ord('z') - ord(char)))
        elif 'A' <= char <= 'Z':
            res += chr(ord('A') + (ord('Z') - ord(char)))
        else:
            res += char
    return res

def caesar_cipher(text, shift=13):
    res = ""
    for char in text:
        if 'a' <= char <= 'z':
            res += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        elif 'A' <= char <= 'Z':
            res += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        else:
            res += char
    return res

MAPPINGS = {
    "Norwegian": {'\u00e6':'0', '\u00f8':'1', '\u00e5':'2', '\u00c6':'3', '\u00d8':'4', '\u00c5':'5', 'n':'6', 'o':'7', 'r':'8', 'g':'9', 'e':'A', 't':'B'}
}

def translate_back(text, lang):
    map_dict = MAPPINGS[lang]
    return "".join(map_dict.get(c, c) for c in text)

def base12_decode(b12_str):
    chars = "0123456789AB"
    res_hex = ""
    for i in range(0, len(b12_str), 2):
        pair = b12_str[i:i+2]
        decimal = chars.index(pair[0]) * 12 + chars.index(pair[1])
        res_hex += hex(decimal)[2:].zfill(2)
    return res_hex

def process_deobfuscation():
    user_input = input_text.get("1.0", tk.END).strip()
    if not user_input:
        messagebox.showwarning("Warning", "Please enter the obfuscated text!")
        return
    
    try:
        s8_text = translate_back(user_input, "Norwegian")
        s5_hex = base12_decode(s8_text)
        s4_b85_bytes = bytes.fromhex(s5_hex)
        s3_caesar = base64.b85decode(s4_b85_bytes).decode()
        s2_atbash = caesar_cipher(s3_caesar, 13)
        s1_b64 = atbash_cipher(s2_atbash)
        original_text = base64.b64decode(s1_b64).decode()
        
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, original_text)
    except Exception as e:
        messagebox.showerror("Error", f"Deobfuscation failed: {e}")

root = tk.Tk()
root.title("Nordic Deobfuscator")
root.geometry("500x500")

label_in = tk.Label(root, text="Enter Text to Deobfuscate:")
label_in.pack(pady=5)

input_text = tk.Text(root, height=10, width=50)
input_text.pack(pady=5)

btn = tk.Button(root, text="Deobfuscate Now", command=process_deobfuscation, bg="#2196F3", fg="white")
btn.pack(pady=10)

label_out = tk.Label(root, text="Original Message:")
label_out.pack(pady=5)

output_text = tk.Text(root, height=5, width=50)
output_text.pack(pady=5)

root.mainloop()