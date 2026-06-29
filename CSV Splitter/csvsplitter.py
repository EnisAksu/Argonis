import os
import sys
import csv
import math
import subprocess

# ------------------------------------------------------------
# Install dependencies automatically
# ------------------------------------------------------------
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import customtkinter as ctk
except ImportError:
    install("customtkinter")
    import customtkinter as ctk

from tkinter import filedialog, messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class CSVSplitter:

    def __init__(self):

        self.root = ctk.CTk()
        self.root.title("CSV Splitter")
        self.root.geometry("520x430")
        self.root.resizable(False, False)

        self.csv_file = None

        title = ctk.CTkLabel(
            self.root,
            text="CSV Splitter",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self.root,
            text="Split large CSV files while preserving headers.",
            font=("Segoe UI", 14)
        )
        subtitle.pack(pady=(0, 20))

        self.file_label = ctk.CTkLabel(
            self.root,
            text="No CSV selected"
        )
        self.file_label.pack()

        browse = ctk.CTkButton(
            self.root,
            text="Browse CSV",
            command=self.browse_file,
            width=180
        )
        browse.pack(pady=15)

        self.mode = ctk.StringVar(value="size")

        frame = ctk.CTkFrame(self.root)
        frame.pack(fill="x", padx=20)

        ctk.CTkRadioButton(
            frame,
            text="Split by Size",
            variable=self.mode,
            value="size",
            command=self.refresh_options
        ).pack(anchor="w", padx=20, pady=10)

        ctk.CTkRadioButton(
            frame,
            text="Split into Pieces",
            variable=self.mode,
            value="pieces",
            command=self.refresh_options
        ).pack(anchor="w", padx=20)

        self.option = ctk.StringVar()

        self.option_menu = ctk.CTkOptionMenu(
            self.root,
            variable=self.option,
            values=["50 MB", "100 MB", "200 MB", "300 MB", "500 MB"]
        )

        self.option_menu.pack(pady=20)

        split = ctk.CTkButton(
            self.root,
            text="Split CSV",
            height=40,
            command=self.start_split
        )

        split.pack(pady=20)

        self.status = ctk.CTkLabel(
            self.root,
            text=""
        )

        self.status.pack()

        self.root.mainloop()

    def browse_file(self):

        file = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv")]
        )

        if file:
            self.csv_file = file
            self.file_label.configure(
                text=os.path.basename(file)
            )

    def refresh_options(self):

        if self.mode.get() == "size":
            values = [
                "50 MB",
                "100 MB",
                "200 MB",
                "300 MB",
                "500 MB"
            ]
        else:
            values = [str(i) for i in range(2, 11)]

        self.option_menu.configure(values=values)
        self.option.set(values[0])

    def count_rows(self):

        with open(self.csv_file, newline="", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f) - 1

    def split_by_pieces(self, pieces):

        total_rows = self.count_rows()

        rows_per_file = math.ceil(total_rows / pieces)

        self.split_rows(rows_per_file)

    def split_by_size(self, target_mb):

        target_bytes = target_mb * 1024 * 1024

        directory = os.path.dirname(self.csv_file)
        base = os.path.splitext(os.path.basename(self.csv_file))[0]

        with open(self.csv_file, newline="", encoding="utf-8", errors="ignore") as infile:

            reader = csv.reader(infile)

            header = next(reader)

            chunk = 1

            outfile = open(
                os.path.join(directory, f"{base}_chunk{chunk}.csv"),
                "w",
                newline="",
                encoding="utf-8"
            )

            writer = csv.writer(outfile)
            writer.writerow(header)

            current_size = outfile.tell()

            for row in reader:

                writer.writerow(row)

                if outfile.tell() >= target_bytes:

                    outfile.close()

                    chunk += 1

                    outfile = open(
                        os.path.join(directory, f"{base}_chunk{chunk}.csv"),
                        "w",
                        newline="",
                        encoding="utf-8"
                    )

                    writer = csv.writer(outfile)
                    writer.writerow(header)

            outfile.close()

    def split_rows(self, rows_per_file):

        directory = os.path.dirname(self.csv_file)
        base = os.path.splitext(os.path.basename(self.csv_file))[0]

        with open(self.csv_file, newline="", encoding="utf-8", errors="ignore") as infile:

            reader = csv.reader(infile)

            header = next(reader)

            chunk = 1
            row_count = 0

            outfile = open(
                os.path.join(directory, f"{base}_chunk{chunk}.csv"),
                "w",
                newline="",
                encoding="utf-8"
            )

            writer = csv.writer(outfile)
            writer.writerow(header)

            for row in reader:

                if row_count >= rows_per_file:

                    outfile.close()

                    chunk += 1
                    row_count = 0

                    outfile = open(
                        os.path.join(directory, f"{base}_chunk{chunk}.csv"),
                        "w",
                        newline="",
                        encoding="utf-8"
                    )

                    writer = csv.writer(outfile)
                    writer.writerow(header)

                writer.writerow(row)
                row_count += 1

            outfile.close()

    def start_split(self):

        if not self.csv_file:
            messagebox.showerror(
                "Error",
                "Please select a CSV file."
            )
            return

        self.status.configure(text="Splitting... Please wait.")
        self.root.update()

        try:

            if self.mode.get() == "size":

                size = int(self.option.get().split()[0])

                self.split_by_size(size)

            else:

                pieces = int(self.option.get())

                self.split_by_pieces(pieces)

            self.status.configure(text="Finished!")

            messagebox.showinfo(
                "Done",
                "CSV successfully split."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

            self.status.configure(text="")


if __name__ == "__main__":
    CSVSplitter()