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
            res += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        elif 'A' <= char <= 'Z':
            res += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        else:
            res += char
    return res

def base12_encode(n):
    chars = "0123456789AB"
    if n == 0: return "00"
    res = ""
    while n:
        res = chars[n % 12] + res
        n //= 12
    return res.zfill(2)

MAPPINGS = {
    "Icelandic": {'0':'\u00e1', '1':'\u00f0', '2':'\u00e9', '3':'\u00ed', '4':'\u00f3', '5':'\u00fa', '6':'\u00fd', '7':'\u00fe', '8':'\u00e6', '9':'\u00f6', 'a':'A', 'b':'B', 'c':'C', 'd':'D', 'e':'E', 'f':'F'},
    "Swedish":   {'0':'\u00e5', '1':'\u00e4', '2':'\u00f6', '3':'\u00c5', '4':'\u00c4', '5':'\u00d6', '6':'s', '7':'w', '8':'e', '9':'d', 'a':'i', 'b':'s', 'c':'h', 'd':'k', 'e':'u', 'f':'l'},
    "Norwegian": {'0':'\u00e6', '1':'\u00f8', '2':'\u00e5', '3':'\u00c6', '4':'\u00d8', '5':'\u00c5', '6':'n', '7':'o', '8':'r', '9':'g', 'a':'e', 'b':'t', 'c':'u', 'd':'v', 'e':'i', 'f':'k'}
}

def translate_layer(text, lang):
    map_dict = MAPPINGS[lang]
    return "".join(map_dict.get(c, c) for c in text)

def process_obfuscation():
    user_input = input_text.get("1.0", tk.END).strip()
    if not user_input:
        messagebox.showwarning("Warning", "Please enter some text!")
        return
    
    try:
        s1 = base64.b64encode(user_input.encode()).decode()
        s2 = atbash_cipher(s1)
        s3 = caesar_cipher(s2, 13)
        s4 = base64.b85encode(s3.encode()).decode()
        s5 = s4.encode().hex()
        s8 = "".join(base12_encode(int(s5[i:i+2], 16)) for i in range(0, len(s5), 2))
        s9 = translate_layer(s8, "Norwegian")
        
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, s9)
    except Exception as e:
        messagebox.showerror("Error", f"Failed: {e}")

root = tk.Tk()
root.title("Nordic Obfuscator v2")
root.geometry("500x500")

tk.Label(root, text="Enter Text to Obfuscate:").pack(pady=5)
input_text = tk.Text(root, height=5, width=50)
input_text.pack(pady=5)

tk.Button(root, text="Obfuscate Now", command=process_obfuscation, bg="#4CAF50", fg="white").pack(pady=10)

tk.Label(root, text="Result:").pack(pady=5)
output_text = tk.Text(root, height=10, width=50)
output_text.pack(pady=5)

root.mainloop()