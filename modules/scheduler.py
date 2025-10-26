"""
Workflow Scheduler
Manages scheduled workflow execution based on weekly schedule
"""

from datetime import datetime, time as dt_time
import time
import threading
from typing import Callable, Dict
from .utils import safe_print


class WorkflowScheduler:
    """Schedules and manages automated workflow execution"""
    
    def __init__(self, schedule: Dict[str, str], workflow_callback: Callable):
        """
        Initialize scheduler
        
        Args:
            schedule: Dict mapping day names to time strings (HH:MM)
                     e.g., {"Monday": "09:00", "Friday": "14:30"}
            workflow_callback: Function to call when scheduled time is reached
        """
        self.schedule = schedule
        self.workflow_callback = workflow_callback
        self.running = False
        self.check_interval = 60  # Check every 60 seconds
    
    def update_schedule(self, schedule: Dict[str, str]):
        """Update the schedule"""
        self.schedule = schedule
    
    def start(self):
        """Start the scheduler"""
        self.running = True
        self.run()
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
    
    def run(self):
        """Main scheduler loop"""
        while self.running:
            self.check_and_execute()
            time.sleep(self.check_interval)
    
    def check_and_execute(self):
        """Check if current time matches any scheduled time"""
        now = datetime.now()
        current_day = now.strftime('%A')  # Monday, Tuesday, etc.
        current_time = now.strftime('%H:%M')
        
        # Check if today is in the schedule
        if current_day in self.schedule:
            scheduled_time = self.schedule[current_day]
            
            # Check if current time matches scheduled time (within 1 minute)
            if self.is_time_match(current_time, scheduled_time):
                safe_print(f"Scheduled time reached: {current_day} at {scheduled_time}")
                
                # Execute workflow callback
                try:
                    self.workflow_callback(current_day)
                except Exception as e:
                    safe_print(f"Error executing scheduled workflow: {e}")
    
    def is_time_match(self, current_time: str, scheduled_time: str) -> bool:
        """
        Check if current time matches scheduled time (within 1 minute)
        
        Args:
            current_time: Current time in HH:MM format
            scheduled_time: Scheduled time in HH:MM format
            
        Returns:
            True if times match within 1 minute
        """
        try:
            curr_parts = current_time.split(':')
            sched_parts = scheduled_time.split(':')
            
            curr_hour, curr_min = int(curr_parts[0]), int(curr_parts[1])
            sched_hour, sched_min = int(sched_parts[0]), int(sched_parts[1])
            
            # Check if hour matches and minute is within range
            if curr_hour == sched_hour:
                # Allow execution within the same minute or next minute
                return abs(curr_min - sched_min) <= 1
            
            return False
            
        except Exception as e:
            safe_print(f"Error comparing times: {e}")
            return False
    
    def get_next_scheduled_run(self) -> str:
        """
        Get the next scheduled run time
        
        Returns:
            Human-readable string of next scheduled time
        """
        if not self.schedule:
            return "No schedule configured"
        
        now = datetime.now()
        current_day_index = now.weekday()  # 0 = Monday, 6 = Sunday
        current_time = now.time()
        
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Check remaining scheduled times today
        today_name = days_order[current_day_index]
        if today_name in self.schedule:
            scheduled_time_str = self.schedule[today_name]
            scheduled_time = self.parse_time(scheduled_time_str)
            
            if scheduled_time and current_time < scheduled_time:
                return f"Today ({today_name}) at {scheduled_time_str}"
        
        # Check upcoming days
        for i in range(1, 8):
            next_day_index = (current_day_index + i) % 7
            next_day_name = days_order[next_day_index]
            
            if next_day_name in self.schedule:
                scheduled_time = self.schedule[next_day_name]
                days_ahead = i
                return f"{next_day_name} ({days_ahead} day{'s' if days_ahead > 1 else ''}) at {scheduled_time}"
        
        return "No upcoming scheduled runs"
    
    def parse_time(self, time_str: str) -> dt_time:
        """Parse time string (HH:MM) to time object"""
        try:
            parts = time_str.split(':')
            return dt_time(int(parts[0]), int(parts[1]))
        except:
            return None

