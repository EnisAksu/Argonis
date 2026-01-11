import sys
import subprocess
import os
import threading
import hashlib
import tkinter as tk
from tkinter import ttk

# ----------------- AUTO INSTALL -----------------

def ensure_dependency(pkg):
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

ensure_dependency("tkinterdnd2")
from tkinterdnd2 import TkinterDnD, DND_FILES

# ----------------- HASHING -----------------

def calculate_hashes(filepath):
    hashes = {
        "MD5": hashlib.md5(),
        "SHA1": hashlib.sha1(),
        "SHA256": hashlib.sha256()
    }
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            for h in hashes.values():
                h.update(chunk)
    return {k: v.hexdigest() for k, v in hashes.items()}

# ----------------- TOAST -----------------

class Toast(tk.Toplevel):
    def __init__(self, master, text):
        super().__init__(master)
        self.overrideredirect(True)
        self.configure(bg="#2d2d2d")

        label = tk.Label(
            self,
            text=text,
            bg="#2d2d2d",
            fg="#9cdcfe",
            font=("Segoe UI", 10),
            padx=14,
            pady=8
        )
        label.pack()

        self.update_idletasks()
        x = master.winfo_x() + master.winfo_width() - self.winfo_width() - 20
        y = master.winfo_y() + master.winfo_height() - self.winfo_height() - 20
        self.geometry(f"+{x}+{y}")

        self.after(1600, self.destroy)

# ----------------- APP -----------------

class HashApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Argonis Hash Calculator")
        self.geometry("950x550")
        self.configure(bg="#1e1e1e")

        self._setup_style()
        self._build_ui()

    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("default")

        style.configure("Treeview",
                        background="#252526",
                        foreground="white",
                        fieldbackground="#252526",
                        rowheight=30)

        style.configure("Treeview.Heading",
                        background="#1e1e1e",
                        foreground="white")

        style.map("Treeview",
                  background=[("selected", "#094771")])

        style.configure("Copy.Treeview",
                        borderwidth=2,
                        relief="solid")

    def _build_ui(self):
        tk.Label(
            self,
            text="Drag & Drop Files Here",
            bg="#1e1e1e",
            fg="#9cdcfe",
            font=("Segoe UI", 14)
        ).pack(pady=10)

        self.tree = ttk.Treeview(
            self,
            columns=("Algo", "Hash", "Copy"),
            show="tree headings"
        )

        self.tree.heading("#0", text="File / Hash")
        self.tree.heading("Algo", text="Algorithm")
        self.tree.heading("Hash", text="Hash Value")
        self.tree.heading("Copy", text="")

        self.tree.column("#0", width=260)
        self.tree.column("Algo", width=100, anchor="center")
        self.tree.column("Hash", width=460)
        self.tree.column("Copy", width=90, anchor="center")

        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Fake rounded button look
        self.tree.tag_configure(
            "copy_btn",
            foreground="#4FC1FF",
            background="#2b2b2b"
        )

        self.tree.drop_target_register(DND_FILES)
        self.tree.dnd_bind("<<Drop>>", self._on_drop)

        self.tree.bind("<Button-1>", self._handle_click)
        self.tree.bind("<Button-3>", self._right_click_menu)

        self.menu = tk.Menu(self, tearoff=0, bg="#2d2d2d", fg="white")

    # ----------------- EVENTS -----------------

    def _on_drop(self, event):
        for file in self.tk.splitlist(event.data):
            if os.path.isfile(file):
                threading.Thread(
                    target=self._process_file,
                    args=(file,),
                    daemon=True
                ).start()

    def _process_file(self, filepath):
        parent = self.tree.insert("", "end",
                                  text=os.path.basename(filepath),
                                  open=True)

        for algo, value in calculate_hashes(filepath).items():
            self.tree.insert(
                parent,
                "end",
                text="",
                values=(algo, value, " COPY "),
                tags=("copy_btn",)
            )

    def _handle_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        column = self.tree.identify_column(event.x)
        row = self.tree.identify_row(event.y)

        if region == "cell" and column == "#3" and row:
            value = self.tree.item(row, "values")[1]
            self._copy(value)

    def _right_click_menu(self, event):
        row = self.tree.identify_row(event.y)
        if not row:
            return

        parent = self.tree.parent(row) or row
        hashes = {
            self.tree.item(c, "values")[0]: self.tree.item(c, "values")[1]
            for c in self.tree.get_children(parent)
        }

        self.menu.delete(0, "end")
        for algo in ["MD5", "SHA1", "SHA256"]:
            if algo in hashes:
                self.menu.add_command(
                    label=f"Copy {algo}",
                    command=lambda v=hashes[algo]: self._copy(v)
                )

        self.menu.tk_popup(event.x_root, event.y_root)

    # ----------------- CLIPBOARD -----------------

    def _copy(self, value):
        self.clipboard_clear()
        self.clipboard_append(value)
        self.update()
        Toast(self, "Copied to clipboard")

# ----------------- RUN -----------------

if __name__ == "__main__":
    HashApp().mainloop()
