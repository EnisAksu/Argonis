import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from datetime import datetime
import tkinterdnd2
from tkinterdnd2 import DND_FILES, TkinterDnD


class EnhancedMergergonis:
    def __init__(self):
        # Initialize main window using TkinterDnD
        self.root = TkinterDnD.Tk()
        self.root.title("Enhanced ScriptBlock Merger")
        self.root.geometry("800x600")
        self.root.configure(bg='black')
        
        # Variables
        self.evtx_path = tk.StringVar()
        self.filter_line = tk.StringVar()
        self.filter_id = tk.StringVar()
        self.filter_time = tk.StringVar()
        
        # Bind filter variables to callback
        self.filter_line.trace('w', self.filter_records)
        self.filter_id.trace('w', self.filter_records)
        self.filter_time.trace('w', self.filter_records)
        
        self.setup_gui()
        
    def setup_gui(self):
        # Drag and Drop Frame
        drop_frame = tk.Frame(self.root, bg='darkgray', height=50)
        drop_frame.pack(fill=tk.X, padx=10, pady=5)
        drop_label = tk.Label(drop_frame, text="Drag and Drop EVTX File Here", bg='darkgray', fg='white')
        drop_label.pack(expand=True, fill=tk.BOTH, pady=10)
        
        # Configure drop target
        drop_frame.drop_target_register(DND_FILES)
        drop_frame.dnd_bind('<<Drop>>', self.handle_drop)
        
        # Browse Button
        browse_button = tk.Button(self.root, text="Browse", command=self.browse_file, 
                                bg="gray", fg="white")
        browse_button.pack(pady=5)
        
        # File Label
        self.file_label = tk.Label(self.root, text="No file selected", bg="black", fg="white")
        self.file_label.pack()
        
        # Find ScriptBlocks Button
        self.find_button = tk.Button(self.root, text="Find ScriptBlocks", 
                                   command=self.find_scriptblocks, state=tk.DISABLED, 
                                   bg="gray", fg="white")
        self.find_button.pack(pady=5)
        
        # Filter Frame
        filter_frame = tk.Frame(self.root, bg='black')
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Filter entries
        tk.Label(filter_frame, text="Filter Line:", bg='black', fg='white').grid(row=0, column=0, padx=5)
        tk.Entry(filter_frame, textvariable=self.filter_line, bg='gray', fg='white').grid(row=0, column=1, padx=5)
        
        tk.Label(filter_frame, text="Filter ID:", bg='black', fg='white').grid(row=0, column=2, padx=5)
        tk.Entry(filter_frame, textvariable=self.filter_id, bg='gray', fg='white').grid(row=0, column=3, padx=5)
        
        tk.Label(filter_frame, text="Filter Time:", bg='black', fg='white').grid(row=0, column=4, padx=5)
        tk.Entry(filter_frame, textvariable=self.filter_time, bg='gray', fg='white').grid(row=0, column=5, padx=5)
        
        # Treeview
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=('checkbox', 'line', 'id', 'time'), 
                                show='headings', selectmode='none')
        
        # Configure treeview columns
        self.tree.heading('checkbox', text='✓')
        self.tree.heading('line', text='Line')
        self.tree.heading('id', text='ScriptBlock ID')
        self.tree.heading('time', text='Time')
        
        self.tree.column('checkbox', width=30, anchor='center')
        self.tree.column('line', width=50)
        self.tree.column('id', width=300)
        self.tree.column('time', width=150)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind click events
        self.tree.bind('<Button-1>', self.handle_click)
        
        # Create Scripts Button
        self.create_button = tk.Button(self.root, text="Create Scripts", 
                                     command=self.create_scripts, state=tk.DISABLED,
                                     bg="gray", fg="white")
        self.create_button.pack(pady=10)
        
        # Apply custom style
        style = ttk.Style()
        style.configure("Treeview", 
                       background="black",
                       foreground="white",
                       fieldbackground="black")
        style.configure("Treeview.Heading",
                       background="gray",
                       foreground="white")
        
    def handle_drop(self, event):
        file_path = event.data
        if file_path.lower().endswith('.evtx'):
            self.evtx_path.set(file_path.strip('{}'))
            self.file_label.config(text=f"File: {os.path.basename(self.evtx_path.get())}")
            self.find_button.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Error", "Please drop only EVTX files")
            
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("EVTX Files", "*.evtx")])
        if file_path:
            self.evtx_path.set(file_path)
            self.file_label.config(text=f"File: {os.path.basename(file_path)}")
            self.find_button.config(state=tk.NORMAL)
            
    def handle_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            item = self.tree.identify_row(event.y)
            if item:
                # Toggle checkbox state
                current_values = self.tree.item(item)['values']
                new_values = list(current_values)
                new_values[0] = '✓' if current_values[0] == '' else ''
                self.tree.item(item, values=new_values)
                
                # Enable/disable create button based on selections
                self.update_create_button_state()
                
    def update_create_button_state(self):
        # Enable create button if any items are checked
        has_checked = any(self.tree.item(item)['values'][0] == '✓' 
                         for item in self.tree.get_children())
        self.create_button.config(state=tk.NORMAL if has_checked else tk.DISABLED)
        
    def filter_records(self, *args):
        # Hide all items that don't match filter criteria
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            line_match = str(values[1]).lower().startswith(self.filter_line.get().lower())
            id_match = str(values[2]).lower().startswith(self.filter_id.get().lower())
            time_match = str(values[3]).lower().startswith(self.filter_time.get().lower())
            
            if line_match and id_match and time_match:
                self.tree.reattach(item, '', 'end')
            else:
                self.tree.detach(item)
                
    def find_scriptblocks(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        file_path = self.evtx_path.get()
        
        # PowerShell command to extract ScriptBlock IDs with timestamps
        powershell_command = f"""
        Get-WinEvent -Path "{file_path}" -FilterXPath "*[System/EventID=4104]" |
        Select-Object TimeCreated, Message |
        ForEach-Object {{
            $id = ($_.Message | Select-String -Pattern "ScriptBlock ID: (\\S+)").Matches.Groups[1].Value
            [PSCustomObject]@{{
                Time = $_.TimeCreated
                ID = $id
            }}
        }} | ConvertTo-Json
        """
        
        try:
            process = subprocess.run(
                ["powershell", "-Command", powershell_command],
                capture_output=True,
                text=True
            )
            
            import json
            results = json.loads(process.stdout)
            
            # Ensure results is a list
            if isinstance(results, dict):
                results = [results]
            
            # Add items to treeview
            for i, result in enumerate(results, 1):
                self.tree.insert('', 'end', values=(
                    '',  # checkbox
                    i,   # line number
                    result['ID'],
                    result['Time']
                ))
                
            if results:
                self.create_button.config(state=tk.NORMAL)
            else:
                messagebox.showinfo("No Results", "No ScriptBlock IDs found")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract ScriptBlock IDs.\n{e}")
            
    def create_scripts(self):
        # Get selected ScriptBlock IDs
        selected_ids = []
        for item in self.tree.get_children():
            if self.tree.item(item)['values'][0] == '✓':
                selected_ids.append(self.tree.item(item)['values'][2])
                
        if not selected_ids:
            messagebox.showerror("Error", "Please select at least one ScriptBlock ID")
            return
            
        file_path = self.evtx_path.get()
        output_path = f"{os.path.splitext(file_path)[0]}_MergedScript.ps1"
        
        try:
            # Create PowerShell script to merge selected scriptblocks
            conditions = " -or ".join([f"$_.Message -like '*{id}*'" for id in selected_ids])
            powershell_script = f"""
            $MergerCollector = Get-WinEvent -FilterHashtable @{{ Path="{file_path}"; ProviderName="Microsoft-Windows-PowerShell"; Id = 4104 }} | 
            Where-Object {{ {conditions} }}
            $Prepare = $MergerCollector | Sort-Object {{ $_.Properties[0].Value }}
            $GotchaScript = -join ($Prepare | ForEach-Object {{ $_.Properties[2].Value }})
            $GotchaScript | Out-File "{output_path}"
            """
            
            subprocess.run(["powershell", "-Command", powershell_script], check=True)
            messagebox.showinfo("Success", f"Script merged successfully and saved to:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge scripts.\n{e}")
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = EnhancedMergergonis()
    app.run()