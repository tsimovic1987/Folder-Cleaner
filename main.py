import os
import shutil
import customtkinter as ctk
from pathlib import Path


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class FolderCleanerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Moderner Folder Cleaner")
        self.geometry("550x500")

        self.base_path = Path(__file__).parent.resolve()
        self.selected_folder = None

        # UI
        self.label = ctk.CTkLabel(self, text="Choose Dictonary", font=("Helvetica", 16))
        self.label.pack(pady=10)

        # Dropdown Menu (OptionMenu)
        self.folders = self.get_folders()
        self.option_menu = ctk.CTkOptionMenu(
            self, 
            values=["-- Bitte wählen --"] + self.folders,
            command=self.folder_selected
        )
        self.option_menu.pack(pady=10)

        # Cleaning Button
        self.clean_button = ctk.CTkButton(
            self, 
            text="Cleaning", 
            state="disabled", 
            command=self.clean_folder,
            fg_color="gray",
            font=("Helvetica", 14, "bold")
        )
        self.clean_button.pack(pady=20)

        # Info Box (Scrollable Text Area)
        self.info_label = ctk.CTkLabel(self, text="Status / Info:", font=("Helvetica", 12))
        self.info_label.pack(pady=(20, 0))
        
        self.info_box = ctk.CTkTextbox(self, width=500, height=150, state="disabled")
        self.info_box.pack(pady=10)

    def get_folders(self):
        """Listet alle Ordner im Basis-Pfad auf."""
        try:
            return [f.name for f in self.base_path.iterdir() if f.is_dir()]
        except Exception as e:
            return [f"Fehler beim Laden: {str(e)}"]

    def folder_selected(self, choice):
        """Wird aufgerufen, wenn ein Ordner ausgewählt wurde."""
        if choice != "-- Bitte wählen --":
            self.selected_folder = self.base_path / choice
            self.clean_button.configure(state="normal", fg_color="#1f538d")
        else:
            self.selected_folder = None
            self.clean_button.configure(state="disabled", fg_color="gray")

    def log_info(self, text):
        """Schreibt Informationen in die Info-Box."""
        self.info_box.configure(state="normal")
        self.info_box.delete("1.0", ctk.END)
        self.info_box.insert("1.0", text)
        self.info_box.configure(state="disabled")

    def clean_folder(self):
        """Sortiert Dateien im ausgewählten Ordner nach Endungen."""
        if not self.selected_folder:
            return

        files = [f for f in self.selected_folder.iterdir() if f.is_file()]
        stats = {}

        if not files:
            self.log_info("Dieser Ordner ist bereits leer oder enthält nur Unterordner.")
            return

        for file in files:
            ext = file.suffix.lower() if file.suffix else "No Extension"
            target_dir = self.selected_folder / ext.replace(".", "").upper()
            
            if not target_dir.exists():
                target_dir.mkdir()

            try:
                shutil.move(str(file), str(target_dir / file.name))
                stats[ext] = stats.get(ext, 0) + 1
            except Exception as e:
                self.log_info(f"Fehler beim Verschieben von {file.name}: {e}")
                return


        info_text = f"Reinigung abgeschlossen für: {self.selected_folder.name}\n\n"
        info_text += "Sortierte Dateien:\n"
        for ext, count in stats.items():
            info_text += f"- {ext if ext != 'No Extension' else 'Ohne Endung'}: {count} Dateien\n"
        
        total_files = sum(stats.values())
        info_text += f"\nGesamt: {total_files} Dateien wurden sortiert."
        
        self.log_info(info_text)

if __name__ == "__main__":
    app = FolderCleanerApp()
    app.mainloop()