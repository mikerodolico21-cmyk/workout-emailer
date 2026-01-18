import json
import random
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WorkoutEmailer:
    def __init__(self):
        self.exercises_file = "data/exercises.json"
        self.history_file = "data/history.json"
        self.muscle_schedule = {
            0: "back",      # Monday
            1: "biceps",    # Tuesday
            2: "triceps",   # Wednesday
            3: "chest",     # Thursday
            4: "shoulders", # Friday
            5: "abs",       # Saturday
            6: "legs"       # Sunday
        }
        
    def load_exercises(self):
        """Load exercises from JSON file"""
        try:
            with open(self.exercises_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading exercises: {e}")
            raise
    
    def load_history(self):
        """Load workout history from JSON file"""
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"workouts": []}
        except Exception as e:
            logger.error(f"Error loading history: {e}")
            raise
    
    def save_history(self, history):
        """Save workout history to JSON file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving history: {e}")
            raise
    
    def get_todays_muscle_group(self):
        """Get today's muscle group based on the day of week"""
        today = datetime.now()
        # Monday=0, Sunday=6
        day_of_week = today.weekday()
        return self.muscle_schedule[day_of_week]
    
    def get_previous_week_exercises(self, history, muscle_group):
        """Get exercises used for same muscle group in the previous week"""
        today = datetime.now()
        previous_week_start = today - timedelta(days=today.weekday() + 7)
        previous_week_end = previous_week_start + timedelta(days=6)
        
        previous_exercises = set()
        for workout in history.get("workouts", []):
            workout_date = datetime.fromisoformat(workout["date"])
            if (previous_week_start <= workout_date <= previous_week_end and 
                workout["muscle_group"] == muscle_group):
                previous_exercises.add(workout["dumbbell_exercise"])
                previous_exercises.add(workout["bodyweight_exercise"])
        
        return previous_exercises
    
    def select_exercises(self, exercises, muscle_group, history):
        """Select exercises ensuring no repetition from previous week"""
        muscle_exercises = exercises[muscle_group]
        previous_exercises = self.get_previous_week_exercises(history, muscle_group)
        
        # Extract exercise names from the new format
        dumbbell_exercises = [ex["name"] if isinstance(ex, dict) else ex for ex in muscle_exercises["dumbbell"]]
        bodyweight_exercises = [ex["name"] if isinstance(ex, dict) else ex for ex in muscle_exercises["bodyweight"]]
        
        # Filter out previous week's exercises
        available_dumbbell = [ex for ex in dumbbell_exercises if ex not in previous_exercises]
        available_bodyweight = [ex for ex in bodyweight_exercises if ex not in previous_exercises]
        
        # If all exercises were used in previous week, allow reuse except immediate previous week
        if not available_dumbbell:
            available_dumbbell = dumbbell_exercises
        if not available_bodyweight:
            available_bodyweight = bodyweight_exercises
        
        # Randomly select exercises
        dumbbell_exercise_name = random.choice(available_dumbbell)
        bodyweight_exercise_name = random.choice(available_bodyweight)
        
        # Get the full exercise objects with descriptions
        dumbbell_exercise = next(ex for ex in muscle_exercises["dumbbell"] 
                               if (ex["name"] if isinstance(ex, dict) else ex) == dumbbell_exercise_name)
        bodyweight_exercise = next(ex for ex in muscle_exercises["bodyweight"] 
                                 if (ex["name"] if isinstance(ex, dict) else ex) == bodyweight_exercise_name)
        
        return dumbbell_exercise, bodyweight_exercise
    
    def create_email_content(self, muscle_group, dumbbell_exercise, bodyweight_exercise):
        """Create email content"""
        # Extract names and descriptions from exercise objects
        dumbbell_name = dumbbell_exercise["name"] if isinstance(dumbbell_exercise, dict) else dumbbell_exercise
        dumbbell_desc = dumbbell_exercise["description"] if isinstance(dumbbell_exercise, dict) else ""
        
        bodyweight_name = bodyweight_exercise["name"] if isinstance(bodyweight_exercise, dict) else bodyweight_exercise
        bodyweight_desc = bodyweight_exercise["description"] if isinstance(bodyweight_exercise, dict) else ""
        
        subject = f"Today's Workout – {muscle_group.title()} Day 💪"
        
        body = f"""{muscle_group.title()} Workout
3 Sets x 10 Reps

1) Dumbbell Exercise: {dumbbell_name}
   {dumbbell_desc}

2) Bodyweight Exercise: {bodyweight_name}
   {bodyweight_desc}

Rest 60–90 seconds between sets."""
        
        return subject, body
    
    def send_email(self, subject, body):
        """Send email using SMTP"""
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        recipient_email = os.getenv("RECIPIENT_EMAIL")
        
        if not all([smtp_server, sender_email, sender_password, recipient_email]):
            raise ValueError("Missing required email configuration environment variables")
        
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        
        message.attach(MIMEText(body, "plain"))
        
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
            logger.info("Email sent successfully")
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            raise
    
    def save_workout(self, history, muscle_group, dumbbell_exercise, bodyweight_exercise):
        """Save workout to history"""
        # Extract exercise names for history storage
        dumbbell_name = dumbbell_exercise["name"] if isinstance(dumbbell_exercise, dict) else dumbbell_exercise
        bodyweight_name = bodyweight_exercise["name"] if isinstance(bodyweight_exercise, dict) else bodyweight_exercise
        
        workout = {
            "date": datetime.now().isoformat(),
            "muscle_group": muscle_group,
            "dumbbell_exercise": dumbbell_name,
            "bodyweight_exercise": bodyweight_name
        }
        
        history["workouts"].append(workout)
        return history
    
    def run(self):
        """Main execution function"""
        try:
            logger.info("Starting workout emailer")
            
            # Load data
            exercises = self.load_exercises()
            history = self.load_history()
            
            # Get today's muscle group
            muscle_group = self.get_todays_muscle_group()
            logger.info(f"Today's muscle group: {muscle_group}")
            
            # Select exercises
            dumbbell_exercise, bodyweight_exercise = self.select_exercises(exercises, muscle_group, history)
            dumbbell_name = dumbbell_exercise["name"] if isinstance(dumbbell_exercise, dict) else dumbbell_exercise
            bodyweight_name = bodyweight_exercise["name"] if isinstance(bodyweight_exercise, dict) else bodyweight_exercise
            logger.info(f"Selected exercises: {dumbbell_name}, {bodyweight_name}")
            
            # Create email content
            subject, body = self.create_email_content(muscle_group, dumbbell_exercise, bodyweight_exercise)
            
            # Send email
            self.send_email(subject, body)
            
            # Save workout to history
            history = self.save_workout(history, muscle_group, dumbbell_exercise, bodyweight_exercise)
            self.save_history(history)
            
            logger.info("Workout emailer completed successfully")
            
        except Exception as e:
            logger.error(f"Error in workout emailer: {e}")
            raise

if __name__ == "__main__":
    emailer = WorkoutEmailer()
    emailer.run()
