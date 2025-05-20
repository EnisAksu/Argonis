import re
import subprocess
import sys

try:
    import tkinter as tk
    from tkinter import messagebox, scrolledtext
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tk"])
    import tkinter as tk
    from tkinter import messagebox, scrolledtext


def extract_and_decode():
    input_text = input_box.get("1.0", tk.END)

    # Extract alphabet (e.g. set UB=...)
    alphabet_match = re.search(r'set\s+\w+=(["\']?)([^"\']+?)\1(?:&|&&)', input_text)
    if not alphabet_match:
        messagebox.showerror("Error", "Could not find the alphabet in the input.")
        return
    alphabet = alphabet_match.group(2)

    # Extract all numeric values from the for-loop
    values_match = re.search(r'for %\w+ in \(([^)]+)\)', input_text)
    if not values_match:
        messagebox.showerror("Error", "Could not find the encoded values.")
        return

    values_str = values_match.group(1)
    delimiter = ';' if ';' in values_str else ','  # handle both ";" and "," separated
    try:
        values = list(map(int, values_str.split(delimiter)))
    except ValueError:
        messagebox.showerror("Error", "Invalid number sequence.")
        return

    # Decode
    code = ''
    outputs = []
    for pos in values:
        if pos > len(alphabet) - 1:
            outputs.append(code[-852:])  # trigger point
        else:
            code += alphabet[pos:pos + 1]

    decoded_output = "\n".join(outputs) if outputs else code
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, decoded_output)


# GUI setup
root = tk.Tk()
root.title("Batch Decoder GUI")
root.geometry("700x600")

tk.Label(root, text="Paste your batch code below:").pack(pady=5)

input_box = scrolledtext.ScrolledText(root, height=15, wrap=tk.WORD)
input_box.pack(fill=tk.BOTH, expand=True, padx=10)

tk.Button(root, text="Decode", command=extract_and_decode, height=2, bg="lightblue").pack(pady=10)

tk.Label(root, text="Decoded Output:").pack(pady=5)

output_box = scrolledtext.ScrolledText(root, height=15, wrap=tk.WORD)
output_box.pack(fill=tk.BOTH, expand=True, padx=10)

root.mainloop()
