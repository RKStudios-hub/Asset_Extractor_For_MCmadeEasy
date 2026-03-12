import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import os
import json
import threading
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

def get_next_extract_folder():
    extract_dir = os.path.join(BASE_DIR, "Extracted")
    os.makedirs(extract_dir, exist_ok=True)
    
    existing = [d for d in os.listdir(extract_dir) if d.startswith("Extract_")]
    if not existing:
        new_folder = os.path.join(extract_dir, "Extract_1")
    else:
        nums = [int(d.split("_")[1]) for d in existing if d.split("_")[1].isdigit()]
        new_num = max(nums) + 1 if nums else 1
        new_folder = os.path.join(extract_dir, f"Extract_{new_num}")
    
    os.makedirs(new_folder, exist_ok=True)
    os.makedirs(os.path.join(new_folder, "Extracted_PNGs"), exist_ok=True)
    return new_folder

PNG_DIR = "Extracted_PNGs"

items = set()
biomes = set()
structures = set()
entities = set()
block_items = set()

def get_modid(jar, fallback_name):
    modid = fallback_name.replace(".jar", "").lower().replace("-", "_").replace(" ", "_")
    
    try:
        file_list = jar.namelist()
        
        for file in file_list:
            if file.endswith("pack.mcmeta"):
                try:
                    content = json.loads(jar.read(file).decode("utf-8"))
                    if "pack" in content and "pack_name" in content["pack"]:
                        modid = content["pack"]["pack_name"].lower()
                        return modid
                except:
                    pass
                    
            if "META-INF/mods.toml" in file:
                try:
                    content = jar.read(file).decode("utf-8")
                    for line in content.split("\n"):
                        if "modId=" in line:
                            modid = line.split("modId=")[1].strip().strip('"').lower()
                            return modid
                except:
                    pass
                    
            if "META-INF/MANIFEST.MF" in file:
                try:
                    content = jar.read(file).decode("utf-8")
                    for line in content.split("\n"):
                        if "Implementation-Name:" in line:
                            modid = line.split("Implementation-Name:")[1].strip().lower().replace(" ", "_")
                            return modid
                except:
                    pass
        
        for file in file_list:
            if file.startswith("assets/") and "/" in file:
                parts = file.split("/")
                if len(parts) >= 2:
                    potential_modid = parts[1].lower()
                    if potential_modid not in ["minecraft", "realms", ""]:
                        return potential_modid
                        
    except Exception as e:
        print(f"Error getting modid: {e}")
    
    return modid

def process_jar(path, status_callback, options, extract_folder):
    try:
        with zipfile.ZipFile(path, 'r') as jar:
            modid = get_modid(jar, os.path.basename(path))
            
            if not modid or modid == "":
                modid = os.path.basename(path).replace(".jar", "").lower().replace("-", "_")
            
            file_list = [f for f in jar.namelist()]
            total_files = len(file_list)
            
            png_dir = os.path.join(extract_folder, "Extracted_PNGs")
            
            for idx, file in enumerate(file_list):
                status_callback(modid, file, idx, total_files)
                
                if options["pngs"] and file.endswith(".png") and ("textures/item" in file or "textures/items" in file):
                    name = os.path.basename(file)
                    if name:
                        newname = f"{modid}_{name}"
                        with open(os.path.join(png_dir, newname), "wb") as f:
                            f.write(jar.read(file))

                if options["items"] and file.startswith("assets/") and "models/item/" in file and file.endswith(".json"):
                    item_name = os.path.basename(file).replace(".json","")
                    items.add(f"{modid}:{item_name}")
                    
                if options["items"] and file.startswith("assets/") and "models/block/" in file and file.endswith(".json"):
                    block_name = os.path.basename(file).replace(".json","")
                    block_items.add(f"{modid}:{block_name}")

                if options["biomes"] and "worldgen/biome/" in file and file.endswith(".json"):
                    biome_name = os.path.basename(file).replace(".json","")
                    biomes.add(f"{modid}:{biome_name}")

                if options["structures"] and "worldgen/structure/" in file and file.endswith(".json"):
                    struct_name = os.path.basename(file).replace(".json","")
                    structures.add(f"{modid}:{struct_name}")

                if options["entities"] and "lang/en_us.json" in file:
                    data = json.loads(jar.read(file).decode("utf-8"))
                    for key in data.keys():
                        if key.startswith("entity."):
                            parts = key.split(".")
                            if len(parts) >= 3:
                                entity_modid = parts[1].lower()
                                entity_name = parts[2].lower()
                                entities.add(f"{entity_modid}:{entity_name}")

                if options["items"] and "tags/item/" in file and file.endswith(".json"):
                    try:
                        data = json.loads(jar.read(file).decode("utf-8"))
                        if "values" in data:
                            for val in data["values"]:
                                if ":" in val:
                                    items.add(val)
                                else:
                                    items.add(f"{modid}:{val}")
                    except:
                        pass
                    
                if options["items"] and "tags/block/" in file and file.endswith(".json"):
                    try:
                        data = json.loads(jar.read(file).decode("utf-8"))
                        if "values" in data:
                            for val in data["values"]:
                                if ":" in val:
                                    block_items.add(val)
                                else:
                                    block_items.add(f"{modid}:{val}")
                    except:
                        pass

    except Exception as e:
        print("Error:", e)

def save_lists(options, extract_folder):
    if options["items"]:
        with open(os.path.join(extract_folder, "items.txt"),"w") as f:
            for i in sorted(items):
                f.write(f"{i}\n")
        
        with open(os.path.join(extract_folder, "blocks.txt"),"w") as f:
            for i in sorted(block_items):
                f.write(f"{i}\n")
                
        with open(os.path.join(extract_folder, "all_items_blocks.txt"),"w") as f:
            for i in sorted(items | block_items):
                f.write(f"{i}\n")

    if options["biomes"]:
        with open(os.path.join(extract_folder, "biomes.txt"),"w") as f:
            for i in sorted(biomes):
                f.write(f"{i}\n")

    if options["structures"]:
        with open(os.path.join(extract_folder, "structures.txt"),"w") as f:
            for i in sorted(structures):
                f.write(f"{i}\n")

    if options["entities"]:
        with open(os.path.join(extract_folder, "entities.txt"),"w") as f:
            for i in sorted(entities):
                f.write(f"{i}\n")

class CustomCheckbutton(tk.Frame):
    def __init__(self, parent, text, emoji, color, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.var = tk.BooleanVar(value=True)
        self.emoji = emoji
        self.color = color
        self.text = text
        
        self.configure(bg="#1e293b", cursor="hand2")
        
        self.checkbox = tk.Checkbutton(self, variable=self.var, 
                                       font=("Segoe UI", 11),
                                       bg="#1e293b", fg=color,
                                       activebackground="#1e293b",
                                       selectcolor="#1e293b",
                                       bd=0, highlightthickness=0)
        self.checkbox.pack(side=tk.LEFT, padx=(0, 8))
        
        self.label = tk.Label(self, text=f"{emoji} {text}", 
                              font=("Segoe UI", 11, "bold"),
                              bg="#1e293b", fg="#e2e8f0")
        self.label.pack(side=tk.LEFT)
        
        self.bind("<Button-1>", self.toggle)
        self.checkbox.bind("<Button-1>", self.toggle)
        self.label.bind("<Button-1>", self.toggle)
        
    def toggle(self, event=None):
        self.var.set(not self.var.get())
        
    def get(self):
        return self.var.get()

class ModExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mod Data Extractor")
        self.root.geometry("600x520")
        self.root.resizable(False, False)
        
        colors = {
            "bg": "#0f172a",
            "card": "#1e293b",
            "accent": "#4ade80",
            "highlight": "#4ade80",
            "text": "#e2e8f0",
            "text_dim": "#64748b"
        }
        
        self.root.configure(bg=colors["bg"])
        
        main_frame = tk.Frame(root, bg=colors["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
        
        header = tk.Frame(main_frame, bg=colors["bg"])
        header.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header, text="MC", font=("Segoe UI", 24, "bold"), 
                bg=colors["bg"], fg=colors["accent"]).pack(side=tk.LEFT)
        
        title = tk.Label(header, text="Mod Data Extractor", 
                        font=("Segoe UI", 18, "bold"), bg=colors["bg"], 
                        fg=colors["text"])
        title.pack(side=tk.LEFT, padx=(10, 0))
        
        subtitle = tk.Label(main_frame, text="Extract mod data for AI command generation", 
                           font=("Segoe UI", 10), bg=colors["bg"], fg=colors["text_dim"])
        subtitle.pack(pady=(0, 20))
        
        extract_card = tk.Frame(main_frame, bg=colors["card"], bd=0)
        extract_card.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(extract_card, text="Select Data to Extract", 
                font=("Segoe UI", 12, "bold"), bg=colors["card"], 
                fg=colors["text"]).pack(anchor="w", padx=15, pady=(15, 10))
        
        options_frame = tk.Frame(extract_card, bg=colors["card"])
        options_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.chk_items = CustomCheckbutton(options_frame, "Items", "items", "#3b82f6")
        self.chk_items.pack(side=tk.LEFT, padx=(0, 20))
        
        self.chk_entities = CustomCheckbutton(options_frame, "Entities", "mobs", "#f59e0b")
        self.chk_entities.pack(side=tk.LEFT, padx=(0, 20))
        
        self.chk_biomes = CustomCheckbutton(options_frame, "Biomes", "biomes", "#10b981")
        self.chk_biomes.pack(side=tk.LEFT, padx=(0, 20))
        
        self.chk_structures = CustomCheckbutton(options_frame, "Structures", "ruins", "#8b5cf6")
        self.chk_structures.pack(side=tk.LEFT, padx=(0, 20))
        
        self.chk_pngs = CustomCheckbutton(options_frame, "Textures", "textures", "#ec4899")
        self.chk_pngs.pack(side=tk.LEFT)
        
        self.upload_btn = tk.Button(main_frame, text="Select Mod JAR Files", 
                                   font=("Segoe UI", 12, "bold"), 
                                   bg=colors["accent"], fg=colors["bg"],
                                   activebackground="#22c55e",
                                   bd=0, padx=30, pady=14,
                                   command=self.start_extraction)
        self.upload_btn.pack(pady=(0, 15))
        
        self.status_card = tk.Frame(main_frame, bg=colors["card"], bd=0)
        self.status_card.pack(fill=tk.X)
        
        self.status_card.pack_propagate(False)
        self.status_card.configure(height=100)
        
        self.status_label = tk.Label(self.status_card, text="Ready to extract", 
                                     font=("Segoe UI", 11), bg=colors["card"], 
                                     fg=colors["text"], anchor="w")
        self.status_label.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        self.file_label = tk.Label(self.status_card, text="", 
                                   font=("Segoe UI", 9), bg=colors["card"], 
                                   fg=colors["text_dim"], anchor="w")
        self.file_label.pack(fill=tk.X, padx=15, pady=(0, 5))
        
        self.progress = tk.Frame(self.status_card, bg="#0f172a", height=6)
        self.progress.pack(fill=tk.X, padx=15, pady=(5, 15))
        
        self.progress_fill = tk.Frame(self.progress, bg=colors["accent"], width=0, height=6)
        self.progress_fill.pack(fill=tk.Y, side=tk.LEFT)
        
        self.stats_card = tk.Frame(main_frame, bg=colors["card"], bd=0)
        self.stats_card.pack(fill=tk.X, pady=(15, 0))
        
        self.stats_card.pack_propagate(False)
        self.stats_card.configure(height=70)
        
        self.stats_inner = tk.Frame(self.stats_card, bg=colors["card"])
        self.stats_inner.pack(fill=tk.BOTH, expand=True)
        
        self.stat_labels = {}
        stats = [("Items", "#3b82f6"), ("Entities", "#f59e0b"), 
                 ("Biomes", "#10b981"), ("Structures", "#8b5cf6")]
        
        for i, (name, color) in enumerate(stats):
            frame = tk.Frame(self.stats_inner, bg=colors["card"])
            frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
            
            count_label = tk.Label(frame, text="0", font=("Segoe UI", 18, "bold"),
                                   bg=colors["card"], fg=color)
            count_label.pack(pady=(10, 0))
            
            tk.Label(frame, text=name, font=("Segoe UI", 9),
                    bg=colors["card"], fg=colors["text_dim"]).pack()
            
            self.stat_labels[name] = count_label
        
        self.is_extracting = False
        
    def get_options(self):
        return {
            "items": self.chk_items.get(),
            "entities": self.chk_entities.get(),
            "biomes": self.chk_biomes.get(),
            "structures": self.chk_structures.get(),
            "pngs": self.chk_pngs.get()
        }
        
    def update_status(self, mod_name, file_name, progress, total):
        percent = int((progress / total) * 100) if total > 0 else 0
        self.status_label.configure(text=f"Extracting: {mod_name}")
        self.file_label.configure(text=f"Processing: {file_name[:50]}... | ModID: {mod_name}")
        self.progress_fill.configure(width=percent * 5.7)
        self.root.update()
        
    def start_extraction(self):
        if self.is_extracting:
            return
        
        options = self.get_options()
        if not any(options.values()):
            messagebox.showwarning("No Selection", "Please select at least one option to extract!")
            return
            
        files = filedialog.askopenfilenames(
            title="Select Mod or Plugin JAR files",
            filetypes=[("Jar files", "*.jar")]
        )
        
        if not files:
            return
            
        self.is_extracting = True
        self.upload_btn.configure(state=tk.DISABLED, text="Extracting...")
        
        global items, biomes, structures, entities, block_items
        items = set()
        biomes = set()
        structures = set()
        entities = set()
        block_items = set()
        
        self.stat_labels["Items"].configure(text="0")
        self.stat_labels["Entities"].configure(text="0")
        self.stat_labels["Biomes"].configure(text="0")
        self.stat_labels["Structures"].configure(text="0")
        
        def run_extraction():
            extract_folder = get_next_extract_folder()
            
            for file in files:
                process_jar(file, self.update_status, options, extract_folder)
            
            save_lists(options, extract_folder)
            self.update_stats()
            
            self.status_label.configure(text="Complete!")
            self.file_label.configure(text=f"Extracted to: {os.path.basename(extract_folder)}")
            self.progress_fill.configure(width=570)
            
            output_info = f"Extracted to:\n{extract_folder}"
            
            self.root.after(0, lambda: messagebox.showinfo("Done", 
                f"Extraction Complete!\n\n{output_info}"))
            self.root.after(0, self.reset_ui)
            
        thread = threading.Thread(target=run_extraction)
        thread.start()
        
    def update_stats(self):
        self.root.after(0, lambda: self.stat_labels["Items"].configure(text=str(len(items) + len(block_items))))
        self.root.after(0, lambda: self.stat_labels["Entities"].configure(text=str(len(entities))))
        self.root.after(0, lambda: self.stat_labels["Biomes"].configure(text=str(len(biomes))))
        self.root.after(0, lambda: self.stat_labels["Structures"].configure(text=str(len(structures))))
        
    def reset_ui(self):
        self.is_extracting = False
        self.upload_btn.configure(state=tk.NORMAL, text="Select Mod JAR Files")

if __name__ == "__main__":
    root = tk.Tk()
    
    # Set icon if available
    icon_path = os.path.join(BASE_DIR, "icon.png")
    if os.path.exists(icon_path) and PIL_AVAILABLE:
        try:
            img = Image.open(icon_path)
            img = img.resize((64, 64), Image.Resampling.LANCZOS)
            icon = ImageTk.PhotoImage(img)
            root.iconphoto(False, icon)
        except Exception as e:
            print(f"Could not load icon: {e}")
    
    app = ModExtractorApp(root)
    root.mainloop()
