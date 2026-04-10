import customtkinter as ctk
import platform

from helper.alert_window import AlertWindow
from helper.sound_manager import SoundManager
from nudge.scanner import Scanner
from nudge.listener import Listener
from nudge.pinger import Pinger


# ==========================================
# NUDGER: The App 
# ==========================================
class NudgeApp:
    def __init__(self, root):
        self.root = root
        self.sound_manager = SoundManager(self.root)

        self.root.title("NUDGER - Nudge your LAN buddies")
        self.root.geometry("500x700")
        self.root.resizable(False, False)

        # Logic State
        self.pinger = Pinger()
        self.scanner = Scanner(self.add_device_to_list)
        self.listener = Listener(
            name_provider=lambda: self.entry_name.get().strip() or platform.node(),
            nudge_callback=self.on_nudge_received,
            scan_callback=self.scanner.register
        )

        self.setup_ui()
        self.toggle_listener() # Start listening by default

    def setup_ui(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0) 
        self.root.grid_rowconfigure(2, weight=1)

        # --- SENDER SECTION ---
        frame_send = ctk.CTkFrame(self.root, corner_radius=10)
        frame_send.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
        
        ctk.CTkLabel(frame_send, text="Send a Nudge", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 15), sticky="w")

        # Name Input
        ctk.CTkLabel(frame_send, text="Your Name:").grid(row=1, column=0, padx=15, pady=5, sticky="w")
        self.entry_name = ctk.CTkEntry(frame_send, width=200, placeholder_text="Enter your name...")
        self.entry_name.insert(0, platform.node())
        self.entry_name.grid(row=1, column=1, padx=15, pady=5, sticky="e")

        # Target Mode
        self.target_mode = ctk.StringVar(value="broadcast")
        ctk.CTkRadioButton(frame_send, text="Broadcast", variable=self.target_mode, value="broadcast", command=self.update_ui_state).grid(row=2, column=0, padx=15, pady=5, sticky="w")
        ctk.CTkRadioButton(frame_send, text="Specific IP(s)", variable=self.target_mode, value="custom", command=self.update_ui_state).grid(row=2, column=1, padx=15, pady=5, sticky="w")

        self.entry_ip = ctk.CTkEntry(frame_send, width=370, placeholder_text="Enter IPs or select from list below...")
        self.entry_ip.grid(row=3, column=0, columnspan=2, padx=15, pady=10)
        self.entry_ip.configure(state="disabled")

        self.btn_send = ctk.CTkButton(frame_send, text="SEND NUDGE", command=self.send_nudge, font=ctk.CTkFont(weight="bold"), height=40)
        self.btn_send.grid(row=4, column=0, columnspan=2, padx=15, pady=(5, 15), sticky="we")

        # --- SCANNER SECTION ---
        frame_scan = ctk.CTkFrame(self.root, corner_radius=10)
        frame_scan.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(frame_scan, text="Online Users", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.btn_scan = ctk.CTkButton(frame_scan, text="Scan LAN", width=80, height=24, command=self.start_discovery)
        self.btn_scan.grid(row=0, column=1, padx=10, pady=5, sticky="e")

        self.device_list = ctk.CTkScrollableFrame(frame_scan, height=50)
        self.device_list.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        frame_scan.grid_columnconfigure(0, weight=1)

        # --- LOG SECTION ---
        self.text_log = ctk.CTkTextbox(self.root, height=100, corner_radius=10, state='disabled')
        self.text_log.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # --- STATUS & TOGGLE (Bottom Row) ---
        self.lbl_status = ctk.CTkLabel(self.root, text="Status: Offline", text_color="gray")
        self.lbl_status.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="w")

        self.btn_listen = ctk.CTkButton(self.root, text="Start Listening", width=100, height=24, 
                                        command=self.toggle_listener, fg_color="#2ecc71", hover_color="#27ae60")
        self.btn_listen.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="e")

    # --- ACTION METHODS ---
    def toggle_listener(self):
        if self.listener.running:
            self.listener.stop()
            self.lbl_status.configure(text="Status: Offline", text_color="gray")
            self.btn_listen.configure(text="Start Listening", fg_color="#2ecc71", hover_color="#27ae60")
            self.log_message("[*] Listener Stopped.")
        else:
            self.listener.start()
            self.lbl_status.configure(text="Status: Listening...", text_color="#2ecc71")
            self.btn_listen.configure(text="Stop Listening", fg_color="#e74c3c", hover_color="#c0392b")
            self.log_message("[*] Listener Started.")

    def update_ui_state(self):
        state = "disabled" if self.target_mode.get() == "broadcast" else "normal"
        self.entry_ip.configure(state=state)

    def log_message(self, message):
        self.text_log.configure(state='normal')
        self.text_log.insert(ctk.END, message + "\n")
        self.text_log.configure(state='disabled')
        self.text_log.see(ctk.END)

    def on_nudge_received(self, name, ip):
        self.root.after(0, self.log_message, f"🔔 NUDGE from {name} ({ip})")
        self.sound_manager.play_nudge()

    def start_discovery(self):
        self.btn_scan.configure(state="disabled", text="Scanning...")
        for widget in self.device_list.winfo_children(): widget.destroy()
        self.scanner.broadcast_search()
        self.root.after(2000, lambda: self.btn_scan.configure(state="normal", text="Scan LAN"))

    def add_device_to_list(self, ip, name):
        btn = ctk.CTkButton(self.device_list, text=f"{name} ({ip})", fg_color="transparent", 
                            text_color="white", anchor="w", command=lambda: self.select_device(ip))
        btn.pack(fill="x", padx=5, pady=2)

    def select_device(self, ip):
        self.target_mode.set("custom")
        self.update_ui_state()
        current = self.entry_ip.get().strip()
        if ip not in current:
            new_val = f"{current} {ip}".strip()
            self.entry_ip.delete(0, 'end')
            self.entry_ip.insert(0, new_val)

    def send_nudge(self):
        sender = self.entry_name.get().strip() or platform.node()
        targets = ["255.255.255.255"] if self.target_mode.get() == "broadcast" else self.entry_ip.get().split()
        
        if not targets and self.target_mode.get() == "custom":
            AlertWindow(self.root, "Error", "No IP addresses specified.")
            return

        success, err = self.pinger.send(targets, sender)
        if success:
            for ip in targets: self.log_message(f"-> Nudge sent to {ip}")
        else:
            AlertWindow(self.root, "Error", f"Failed to send: {err}")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    app = NudgeApp(root)
    root.mainloop()