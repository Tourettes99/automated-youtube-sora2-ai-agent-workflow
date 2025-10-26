"""
AI Agent GUI - Main Application
Automated workflow for Sora 2 video generation, watermark removal, and YouTube upload
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Setup console encoding FIRST (before any imports that might print)
from modules.utils import setup_console_encoding
setup_console_encoding()

from modules.settings_manager import SettingsManager
from modules.workflow_manager import WorkflowManager
from modules.logger import WorkflowLogger


class AIAgentGUI:
    """Main GUI Application for AI Agent Video Workflow"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AI Agent - Sora Video to YouTube Workflow")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Initialize managers
        self.settings_manager = SettingsManager()
        self.logger = WorkflowLogger()
        self.workflow_manager = WorkflowManager(
            self.settings_manager,
            self.logger,
            self.update_progress
        )
        
        # Setup UI
        self.setup_ui()
        
        # Start background scheduler check
        self.check_schedule_thread = threading.Thread(
            target=self.workflow_manager.start_scheduler,
            daemon=True
        )
        self.check_schedule_thread.start()
        
    def setup_ui(self):
        """Setup the main user interface"""
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_settings_tab()
        self.create_schedule_tab()
        self.create_logs_tab()
        
    def create_dashboard_tab(self):
        """Create the main dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Title
        title_label = tk.Label(
            dashboard_frame,
            text="AI Agent Workflow Dashboard",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Workflow visualization
        viz_frame = ttk.LabelFrame(dashboard_frame, text="Workflow Progress", padding=10)
        viz_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Workflow steps
        self.workflow_steps = [
            "AI Agent Planning",
            "Sora 2 Video Generation",
            "Watermark Removal (KLing)",
            "Video Enhancement",
            "YouTube Upload"
        ]
        
        self.step_labels = {}
        self.step_progress = {}
        
        for i, step in enumerate(self.workflow_steps):
            step_frame = ttk.Frame(viz_frame)
            step_frame.pack(fill="x", pady=5)
            
            # Step number and name
            label = tk.Label(
                step_frame,
                text=f"{i+1}. {step}",
                font=("Arial", 10),
                width=30,
                anchor="w"
            )
            label.pack(side="left", padx=5)
            self.step_labels[step] = label
            
            # Progress bar
            progress = ttk.Progressbar(
                step_frame,
                mode='determinate',
                length=300
            )
            progress.pack(side="left", padx=5)
            self.step_progress[step] = progress
            
            # Status
            status = tk.Label(step_frame, text="Pending", width=15, anchor="w")
            status.pack(side="left", padx=5)
            self.step_labels[f"{step}_status"] = status
        
        # Overall status
        status_frame = ttk.Frame(dashboard_frame)
        status_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(status_frame, text="Overall Status:", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        self.overall_status = tk.Label(status_frame, text="Idle", font=("Arial", 10))
        self.overall_status.pack(side="left", padx=5)
        
        # Control buttons
        button_frame = ttk.Frame(dashboard_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        self.run_now_btn = tk.Button(
            button_frame,
            text="Run Workflow Now",
            command=self.run_workflow_manually,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=10
        )
        self.run_now_btn.pack(side="left", padx=5)
        
        self.stop_btn = tk.Button(
            button_frame,
            text="Stop Workflow",
            command=self.stop_workflow,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=10,
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=5)
        
        # Next scheduled run
        schedule_info = ttk.Frame(dashboard_frame)
        schedule_info.pack(fill="x", padx=10, pady=5)
        
        tk.Label(schedule_info, text="Next Scheduled Run:", font=("Arial", 9)).pack(side="left", padx=5)
        self.next_run_label = tk.Label(schedule_info, text="Not configured", font=("Arial", 9, "italic"))
        self.next_run_label.pack(side="left", padx=5)
        
    def create_settings_tab(self):
        """Create the settings configuration tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Create scrollable frame
        canvas = tk.Canvas(settings_frame)
        scrollbar = ttk.Scrollbar(settings_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # API Settings
        api_frame = ttk.LabelFrame(scrollable_frame, text="API Configuration", padding=10)
        api_frame.pack(fill="x", padx=10, pady=5)
        
        # OpenAI API Key
        tk.Label(api_frame, text="OpenAI API Key (for Sora 2):").grid(row=0, column=0, sticky="w", pady=5)
        self.openai_key_entry = ttk.Entry(api_frame, width=50, show="*")
        self.openai_key_entry.grid(row=0, column=1, pady=5, padx=5)
        self.openai_key_entry.insert(0, self.settings_manager.get("openai_api_key", ""))
        
        # Google Gemini API Key
        tk.Label(api_frame, text="Google Gemini API Key:").grid(row=1, column=0, sticky="w", pady=5)
        self.gemini_key_entry = ttk.Entry(api_frame, width=50, show="*")
        self.gemini_key_entry.grid(row=1, column=1, pady=5, padx=5)
        self.gemini_key_entry.insert(0, self.settings_manager.get("gemini_api_key", ""))
        
        # YouTube API Settings
        youtube_frame = ttk.LabelFrame(scrollable_frame, text="YouTube Configuration", padding=10)
        youtube_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(youtube_frame, text="YouTube API Key:").grid(row=0, column=0, sticky="w", pady=5)
        self.youtube_key_entry = ttk.Entry(youtube_frame, width=50, show="*")
        self.youtube_key_entry.grid(row=0, column=1, pady=5, padx=5)
        self.youtube_key_entry.insert(0, self.settings_manager.get("youtube_api_key", ""))
        
        tk.Label(youtube_frame, text="YouTube Client Secrets File:").grid(row=1, column=0, sticky="w", pady=5)
        self.youtube_secrets_entry = ttk.Entry(youtube_frame, width=50)
        self.youtube_secrets_entry.grid(row=1, column=1, pady=5, padx=5)
        self.youtube_secrets_entry.insert(0, self.settings_manager.get("youtube_client_secrets", "client_secrets.json"))
        
        # AI Agent Instructions
        agent_frame = ttk.LabelFrame(scrollable_frame, text="AI Agent Custom Instructions", padding=10)
        agent_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        tk.Label(agent_frame, text="Custom Instructions for Video Generation:").pack(anchor="w", pady=5)
        self.agent_instructions = scrolledtext.ScrolledText(agent_frame, height=8, width=70)
        self.agent_instructions.pack(fill="both", expand=True, pady=5)
        default_instructions = self.settings_manager.get(
            "agent_instructions",
            "Generate engaging, high-quality videos suitable for YouTube. "
            "Focus on trending topics, educational content, or entertainment. "
            "Keep videos between 30-60 seconds."
        )
        self.agent_instructions.insert("1.0", default_instructions)
        
        # Video Settings
        video_frame = ttk.LabelFrame(scrollable_frame, text="Video Settings", padding=10)
        video_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(video_frame, text="Video Duration (seconds):").grid(row=0, column=0, sticky="w", pady=5)
        self.video_duration = ttk.Entry(video_frame, width=20)
        self.video_duration.grid(row=0, column=1, pady=5, padx=5)
        self.video_duration.insert(0, str(self.settings_manager.get("video_duration", 30)))
        
        tk.Label(video_frame, text="Video Resolution:").grid(row=1, column=0, sticky="w", pady=5)
        self.video_resolution = ttk.Combobox(
            video_frame,
            values=["1080p", "720p", "480p"],
            width=18
        )
        self.video_resolution.grid(row=1, column=1, pady=5, padx=5)
        self.video_resolution.set(self.settings_manager.get("video_resolution", "1080p"))
        
        # Save button
        save_btn = tk.Button(
            scrollable_frame,
            text="Save Settings",
            command=self.save_settings,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=10
        )
        save_btn.pack(pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_schedule_tab(self):
        """Create the schedule configuration tab"""
        schedule_frame = ttk.Frame(self.notebook)
        self.notebook.add(schedule_frame, text="Schedule")
        
        # Title
        tk.Label(
            schedule_frame,
            text="Weekly Upload Schedule",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        tk.Label(
            schedule_frame,
            text="Select days and times for automatic video uploads:",
            font=("Arial", 10)
        ).pack(pady=5)
        
        # Schedule configuration
        schedule_config_frame = ttk.LabelFrame(schedule_frame, text="Schedule Configuration", padding=10)
        schedule_config_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        self.day_checkboxes = {}
        self.time_entries = {}
        
        current_schedule = self.settings_manager.get("weekly_schedule", {})
        
        for i, day in enumerate(days):
            day_frame = ttk.Frame(schedule_config_frame)
            day_frame.pack(fill="x", pady=5)
            
            # Checkbox for day
            var = tk.BooleanVar(value=day in current_schedule)
            checkbox = tk.Checkbutton(
                day_frame,
                text=day,
                variable=var,
                font=("Arial", 10),
                width=15,
                anchor="w"
            )
            checkbox.pack(side="left", padx=5)
            self.day_checkboxes[day] = var
            
            # Time entry
            tk.Label(day_frame, text="Time (HH:MM):").pack(side="left", padx=5)
            time_entry = ttk.Entry(day_frame, width=10)
            time_entry.pack(side="left", padx=5)
            if day in current_schedule:
                time_entry.insert(0, current_schedule[day])
            else:
                time_entry.insert(0, "09:00")
            self.time_entries[day] = time_entry
        
        # Save schedule button
        save_schedule_btn = tk.Button(
            schedule_frame,
            text="Save Schedule",
            command=self.save_schedule,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=10
        )
        save_schedule_btn.pack(pady=10)
        
    def create_logs_tab(self):
        """Create the logs viewing tab"""
        logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(logs_frame, text="Logs")
        
        # Title
        tk.Label(
            logs_frame,
            text="Workflow Logs",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        # Log display
        self.log_display = scrolledtext.ScrolledText(
            logs_frame,
            height=25,
            width=100,
            font=("Courier", 9)
        )
        self.log_display.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Refresh button
        refresh_btn = tk.Button(
            logs_frame,
            text="Refresh Logs",
            command=self.refresh_logs,
            bg="#2196F3",
            fg="white",
            font=("Arial", 9),
            padx=15,
            pady=5
        )
        refresh_btn.pack(pady=5)
        
        # Load initial logs
        self.refresh_logs()
        
    def save_settings(self):
        """Save all settings"""
        try:
            settings = {
                "openai_api_key": self.openai_key_entry.get(),
                "gemini_api_key": self.gemini_key_entry.get(),
                "youtube_api_key": self.youtube_key_entry.get(),
                "youtube_client_secrets": self.youtube_secrets_entry.get(),
                "agent_instructions": self.agent_instructions.get("1.0", "end-1c"),
                "video_duration": int(self.video_duration.get()),
                "video_resolution": self.video_resolution.get()
            }
            
            self.settings_manager.update(settings)
            messagebox.showinfo("Success", "Settings saved successfully!")
            self.logger.log("Settings updated successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
            self.logger.log(f"Error saving settings: {str(e)}", level="ERROR")
    
    def save_schedule(self):
        """Save the weekly schedule"""
        try:
            schedule = {}
            for day, var in self.day_checkboxes.items():
                if var.get():
                    time = self.time_entries[day].get()
                    # Validate time format
                    if not self.validate_time(time):
                        raise ValueError(f"Invalid time format for {day}. Use HH:MM format.")
                    schedule[day] = time
            
            self.settings_manager.update({"weekly_schedule": schedule})
            messagebox.showinfo("Success", "Schedule saved successfully!")
            self.logger.log(f"Schedule updated: {schedule}")
            self.update_next_run_display()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save schedule: {str(e)}")
            self.logger.log(f"Error saving schedule: {str(e)}", level="ERROR")
    
    def validate_time(self, time_str):
        """Validate time format HH:MM"""
        try:
            parts = time_str.split(":")
            if len(parts) != 2:
                return False
            hour, minute = int(parts[0]), int(parts[1])
            return 0 <= hour <= 23 and 0 <= minute <= 59
        except:
            return False
    
    def update_next_run_display(self):
        """Update the next scheduled run display"""
        next_run = self.workflow_manager.get_next_scheduled_run()
        if next_run:
            self.next_run_label.config(text=next_run)
        else:
            self.next_run_label.config(text="No schedule configured")
    
    def run_workflow_manually(self):
        """Run the workflow manually"""
        self.run_now_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.overall_status.config(text="Running...")
        
        # Run workflow in separate thread
        workflow_thread = threading.Thread(
            target=self.workflow_manager.run_workflow,
            daemon=True
        )
        workflow_thread.start()
    
    def stop_workflow(self):
        """Stop the current workflow"""
        self.workflow_manager.stop_workflow()
        self.run_now_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.overall_status.config(text="Stopped")
    
    def update_progress(self, step, progress, status):
        """Update the progress display"""
        def update():
            if step in self.step_progress:
                self.step_progress[step]["value"] = progress
                self.step_labels[f"{step}_status"].config(text=status)
            
            if status == "Completed":
                self.step_labels[f"{step}_status"].config(fg="green")
            elif status == "Error":
                self.step_labels[f"{step}_status"].config(fg="red")
            elif status == "Running":
                self.step_labels[f"{step}_status"].config(fg="blue")
            
            # Update overall status
            if step == self.workflow_steps[-1] and status == "Completed":
                self.overall_status.config(text="Workflow Completed Successfully!", fg="green")
                self.run_now_btn.config(state="normal")
                self.stop_btn.config(state="disabled")
            elif status == "Error":
                self.overall_status.config(text="Workflow Error - Check Logs", fg="red")
                self.run_now_btn.config(state="normal")
                self.stop_btn.config(state="disabled")
        
        self.root.after(0, update)
    
    def refresh_logs(self):
        """Refresh the log display"""
        self.log_display.delete("1.0", tk.END)
        logs = self.logger.get_recent_logs(100)
        self.log_display.insert("1.0", logs)
        self.log_display.see(tk.END)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = AIAgentGUI(root)
    
    # Update next run display
    app.update_next_run_display()
    
    root.mainloop()


if __name__ == "__main__":
    main()

