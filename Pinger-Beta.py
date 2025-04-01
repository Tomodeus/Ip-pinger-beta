#!/usr/bin/env python3
import subprocess
import platform
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class IPPingerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CyberPinger Pro")
        self.root.geometry("600x500")
        
        # Style & Theme (Dark/Light)
        self.style = ttk.Style(theme="cyborg")  # Try: "cosmo", "minty", "darkly"
        
        # Variablen
        self.ping_running = False
        self.stop_ping = False
        
        # GUI-Elemente erstellen
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        self.header = ttk.Label(
            self.root,
            text="⚡ CYBERPINGER PRO ⚡",
            font=("Helvetica", 16, "bold"),
            bootstyle="primary"
        )
        self.header.pack(pady=10)
        
        # Eingabe-Frame
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(input_frame, text="IP/Host:").pack(side="left", padx=5)
        self.ip_entry = ttk.Entry(input_frame, width=30)
        self.ip_entry.pack(side="left", padx=5)
        self.ip_entry.insert(0, "google.com")  # Default-Wert
        
        # Button-Frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.start_btn = ttk.Button(
            button_frame,
            text="Start Ping",
            command=self.start_ping,
            bootstyle="success-outline"
        )
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = ttk.Button(
            button_frame,
            text="Stop Ping",
            command=self.stop_ping,
            bootstyle="danger-outline",
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=5)
        
        # Ergebnis-Anzeige (Textbox mit Scrollbar)
        result_frame = ttk.Frame(self.root)
        result_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.result_text = tk.Text(
            result_frame,
            wrap="word",
            height=15,
            font=("Consolas", 10)
        )
        self.result_text.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(
            result_frame,
            orient="vertical",
            command=self.result_text.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        # Statusleiste
        self.status_var = tk.StringVar()
        self.status_var.set("Bereit zum Ping")
        
        self.status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w",
            bootstyle="secondary"
        )
        self.status_bar.pack(fill="x", padx=5, pady=5)
    
    def ping(self, host):
        try:
            # OS-spezifischer Ping-Befehl
            param = "-n" if platform.system().lower() == "windows" else "-c"
            command = ["ping", param, "1", host]
            
            output = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )
            
            if output.returncode == 0:
                return True, output.stdout
            else:
                return False, output.stderr
        except Exception as e:
            return False, str(e)
    
    def update_result(self, success, response):
        if success:
            self.result_text.insert("end", f"✅ {response}\n", "success")
            self.status_var.set("Online - Ping erfolgreich")
        else:
            self.result_text.insert("end", f"❌ Fehler: {response}\n", "error")
            self.status_var.set("Offline - Keine Antwort")
        
        self.result_text.see("end")  # Automatisch scrollen
    
    def ping_loop(self):
        host = self.ip_entry.get().strip()
        
        if not host:
            messagebox.showerror("Fehler", "Bitte eine IP/Host eingeben!")
            return
        
        self.ping_running = True
        self.stop_ping = False
        
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        
        while self.ping_running and not self.stop_ping:
            success, response = self.ping(host)
            self.root.after(0, self.update_result, success, response)
            
            if not self.stop_ping:
                threading.Event().wait(1)  # 1 Sekunde warten
        
        self.ping_running = False
        self.root.after(0, self.reset_buttons)
    
    def start_ping(self):
        if not self.ping_running:
            threading.Thread(target=self.ping_loop, daemon=True).start()
    
    def stop_ping(self):
        self.stop_ping = True
        self.status_var.set("Ping gestoppt")
    
    def reset_buttons(self):
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

if __name__ == "__main__":
    root = ttk.Window(themename="cyborg")  # Theme: "darkly", "solar", "minty"
    app = IPPingerGUI(root)
    root.mainloop()
