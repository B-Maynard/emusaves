import os
import json
import dropbox
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Constants
CONFIG_FOLDER = "configs"
GLOBAL_CONFIG_FILE = "global_config.json"

def load_configs():
    if not os.path.exists(CONFIG_FOLDER):
        os.makedirs(CONFIG_FOLDER)
    configs = {}
    for file in os.listdir(CONFIG_FOLDER):
        if file.endswith(".json"):
            with open(os.path.join(CONFIG_FOLDER, file), 'r') as f:
                configs[file[:-5]] = json.load(f)
    return configs

def load_global_config():
    if os.path.exists(GLOBAL_CONFIG_FILE):
        with open(GLOBAL_CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_global_config(global_config):
    with open(GLOBAL_CONFIG_FILE, 'w') as f:
        json.dump(global_config, f, indent=4)

def save_config(name, config):
    if not os.path.exists(CONFIG_FOLDER):
        os.makedirs(CONFIG_FOLDER)
    with open(os.path.join(CONFIG_FOLDER, f"{name}.json"), 'w') as f:
        json.dump(config, f, indent=4)

class SaveBackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Save Backup")
        self.configs = load_configs()
        self.global_config = load_global_config()
        self.current_config_name = None
        self.base_folder = self.global_config.get("base_folder")
        self.dbx = None

        # Main GUI layout
        self.setup_gui()
        if not self.base_folder:
            self.initialize_base_folder()

    def setup_gui(self):
        # Config Selection Section
        ttk.Label(self.root, text="Select Configuration:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.config_var = tk.StringVar()
        self.config_menu = ttk.Combobox(self.root, textvariable=self.config_var, values=list(self.configs.keys()), state="readonly")
        self.config_menu.grid(row=0, column=1, padx=10, pady=5)
        self.config_menu.bind("<<ComboboxSelected>>", self.load_selected_config)

        # Dropbox Token Section
        ttk.Label(self.root, text="Dropbox Access Token:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.token_entry = ttk.Entry(self.root, width=40)
        self.token_entry.grid(row=1, column=1, padx=10, pady=5)
        self.token_entry.insert(0, self.global_config.get("dropbox_token", ""))
        ttk.Button(self.root, text="Save Token", command=self.save_global_token).grid(row=1, column=2, padx=10, pady=5)

        # Game Save Path Section
        ttk.Label(self.root, text="Game Save Path:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.path_entry = ttk.Entry(self.root, width=40)
        self.path_entry.grid(row=2, column=1, padx=10, pady=5)
        ttk.Button(self.root, text="Browse", command=self.browse_path).grid(row=2, column=2, padx=10, pady=5)

        # Config Save Section
        ttk.Label(self.root, text="Configuration Name:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.config_name_entry = ttk.Entry(self.root, width=40)
        self.config_name_entry.grid(row=3, column=1, padx=10, pady=5)
        ttk.Button(self.root, text="Save Config", command=self.save_current_config).grid(row=3, column=2, padx=10, pady=5)

        # Buttons for Upload and Download
        ttk.Button(self.root, text="Upload Save", command=self.upload_save).grid(row=4, column=0, padx=10, pady=10)
        ttk.Button(self.root, text="Download Save", command=self.download_save).grid(row=4, column=1, padx=10, pady=10)

    def initialize_base_folder(self):
        token = self.global_config.get("dropbox_token", "").strip()
        if not token:
            messagebox.showerror("Error", "Dropbox token not configured globally!")
            return

        self.dbx = dropbox.Dropbox(token)

        try:
            entries = self.dbx.files_list_folder('').entries
            folder_names = [entry.name for entry in entries if isinstance(entry, dropbox.files.FolderMetadata)]
            choice = messagebox.askyesno("Base Folder", "Do you want to create a new base folder for game saves?")
            if choice:
                new_folder_name = "GameSaves"
                self.dbx.files_create_folder_v2(f"/{new_folder_name}")
                self.base_folder = new_folder_name
                self.global_config["base_folder"] = new_folder_name
                save_global_config(self.global_config)
            else:
                folder_choice = tk.simpledialog.askstring("Choose Folder", f"Available Folders: {', '.join(folder_names)}\nEnter folder name:")
                if folder_choice and folder_choice in folder_names:
                    self.base_folder = folder_choice
                    self.global_config["base_folder"] = folder_choice
                    save_global_config(self.global_config)
                else:
                    messagebox.showerror("Error", "Invalid folder choice!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize base folder: {e}")

    def load_selected_config(self, event):
        config_name = self.config_var.get()
        if config_name in self.configs:
            self.current_config_name = config_name
            config = self.configs[config_name]
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, config.get("save_path", ""))

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def save_global_token(self):
        token = self.token_entry.get().strip()
        if not token:
            messagebox.showwarning("Warning", "Dropbox token cannot be empty!")
            return
        self.global_config["dropbox_token"] = token
        save_global_config(self.global_config)
        messagebox.showinfo("Success", "Dropbox token saved globally!")

    def save_current_config(self):
        config_name = self.config_name_entry.get().strip()
        if not config_name:
            messagebox.showwarning("Warning", "Configuration name cannot be empty!")
            return

        if not self.base_folder:
            messagebox.showerror("Error", "Base folder not initialized!")
            return

        token = self.global_config.get("dropbox_token", "").strip()
        if not token:
            messagebox.showerror("Error", "Dropbox token not configured globally!")
            return

        self.dbx = dropbox.Dropbox(token)

        try:
            entries = self.dbx.files_list_folder(f"/{self.base_folder}").entries
            existing_folders = [entry.name for entry in entries if isinstance(entry, dropbox.files.FolderMetadata)]

            if config_name in existing_folders:
                use_existing = messagebox.askyesno("Folder Exists", f"A folder named '{config_name}' already exists in Dropbox. Use it as the configuration folder?")
                if not use_existing:
                    messagebox.showinfo("Cancelled", "Configuration not saved.")
                    return
            else:
                self.dbx.files_create_folder_v2(f"/{self.base_folder}/{config_name}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to check or create folder: {e}")
            return

        config = {
            "save_path": self.path_entry.get().strip()
        }

        save_config(config_name, config)
        self.configs[config_name] = config
        self.config_menu["values"] = list(self.configs.keys())
        messagebox.showinfo("Success", "Configuration saved!")

    def upload_save(self):
        save_path = self.path_entry.get().strip()
        if not save_path or not os.path.exists(save_path):
            messagebox.showerror("Error", "Invalid save path!")
            return

        token = self.global_config.get("dropbox_token", "").strip()
        if not token:
            messagebox.showerror("Error", "Dropbox token not configured globally!")
            return

        self.dbx = dropbox.Dropbox(token)

        if not self.base_folder or not self.current_config_name:
            messagebox.showerror("Error", "Base folder or configuration not initialized!")
            return

        folder_path = f"/{self.base_folder}/{self.current_config_name}"

        try:
            for root, _, files in os.walk(save_path):
                for file in files:
                    local_path = os.path.join(root, file)
                    dropbox_path = f"{folder_path}/{os.path.relpath(local_path, save_path)}"
                    with open(local_path, 'rb') as f:
                        self.dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
            messagebox.showinfo("Success", "Save data uploaded to Dropbox!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload save data: {e}")

    def download_save(self):
        save_path = self.path_entry.get().strip()
        if not save_path:
            messagebox.showerror("Error", "Save path not configured!")
            return

        token = self.global_config.get("dropbox_token", "").strip()
        if not token:
            messagebox.showerror("Error", "Dropbox token not configured globally!")
            return

        self.dbx = dropbox.Dropbox(token)

        if not self.base_folder or not self.current_config_name:
            messagebox.showerror("Error", "Base folder or configuration not initialized!")
            return

        folder_path = f"/{self.base_folder}/{self.current_config_name}"

        try:
            entries = self.dbx.files_list_folder(folder_path).entries
            for entry in entries:
                local_path = os.path.join(save_path, entry.name)
                with open(local_path, 'wb') as f:
                    metadata, res = self.dbx.files_download(path=f"{folder_path}/{entry.name}")
                    f.write(res.content)
            messagebox.showinfo("Success", "Save data downloaded from Dropbox!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download save data: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SaveBackupApp(root)
    root.mainloop()
