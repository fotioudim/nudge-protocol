import customtkinter as ctk

# ==========================================
# PopUp window for alerts & errors
# ==========================================
class AlertWindow(ctk.CTkToplevel):
    def __init__(self, parent, title, message, mode="error"):
        super().__init__(parent)

        self.attributes("-alpha", 0.0)
        self.transient(parent)
        self.title(title)
        self.geometry("350x180")
        self.resizable(False, False)

        x = parent.winfo_x() + (parent.winfo_width() - 350) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 180) // 2 - 50  
        self.geometry(f"+{x}+{y}")
 
        color = "#e74c3c" if mode == "error" else "#f1c40f"
        icon_text = "✕" if mode == "error" else "⚠"

        accent = ctk.CTkFrame(self, width=10, fg_color=color, corner_radius=0)
        accent.pack(side="left", fill="y")

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=20, pady=20)

        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(header, text=icon_text, text_color=color, font=ctk.CTkFont(size=24, weight="bold")).pack(side="left")
        ctk.CTkLabel(header, text=title.upper(), font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=10)

        ctk.CTkLabel(content, text=message, wraplength=250, justify="left").pack(anchor="w")
        ctk.CTkButton(content, text="OK", width=80, height=28, fg_color=color, command=self.destroy).pack(side="bottom", anchor="e", pady=(10, 0))
        
        self.after(150, self.reveal)

    def reveal(self):
        self.attributes("-alpha", 1.0)
        self.lift()
        self.focus_force()
        self.grab_set()
