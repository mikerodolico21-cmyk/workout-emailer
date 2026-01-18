# Daily Workout Emailer

A fully automated workout email system that sends you a daily workout at 10:00 AM using GitHub Actions. Each workout includes one dumbbell exercise and one bodyweight exercise for the day's muscle group.

## Features

- **Automated Daily Emails**: Sends workout emails every day at 10:00 AM
- **Weekly Muscle Split**: Fixed schedule targeting different muscle groups each day
- **Exercise Variety**: Random selection from predefined exercise pools
- **Weekly Uniqueness**: Exercises don't repeat from the previous week for the same muscle group
- **No Local Dependencies**: Runs entirely on GitHub Actions
- **History Tracking**: Maintains workout history to prevent repetition

## Weekly Schedule

- **Monday**: Back
- **Tuesday**: Biceps  
- **Wednesday**: Triceps
- **Thursday**: Chest
- **Friday**: Shoulders
- **Saturday**: Abs
- **Sunday**: Legs

## Setup

### 1. Fork or Clone This Repository

```bash
git clone https://github.com/yourusername/workout-emailer.git
cd workout-emailer
```

### 2. Configure GitHub Secrets

Go to your repository's **Settings > Secrets and variables > Actions** and add the following secrets:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `SMTP_SERVER` | Your SMTP server address | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP port number | `587` |
| `SENDER_EMAIL` | Your email address | `your.email@gmail.com` |
| `SENDER_PASSWORD` | Your email password or app password | `your-app-password` |
| `RECIPIENT_EMAIL` | Primary email address to receive workouts | `your.email@gmail.com` |
| `RECIPIENT_EMAIL_2` | Secondary email address (optional) | `friend.email@gmail.com` |

#### Gmail Setup

If using Gmail, you'll need to:
1. Enable 2-factor authentication
2. Create an App Password: https://myaccount.google.com/apppasswords
3. Use the App Password as `SENDER_PASSWORD`

### 3. Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. Enable GitHub Actions if not already enabled
3. The workflow will run automatically at 10:00 AM UTC daily

## Manual Testing

You can test the workflow manually:

1. Go to **Actions** tab
2. Select **Daily Workout Emailer** workflow
3. Click **Run workflow**
4. Choose whether to send a test email
5. Click **Run workflow**

## Email Format

**Subject**: `Today's Workout – <Muscle Group> Day 💪`

**Body**:
```
<Muscle Group> Workout
3 Sets x 10 Reps

1) Dumbbell Exercise: <Exercise Name>
2) Bodyweight Exercise: <Exercise Name>

Rest 60–90 seconds between sets.
```

## Project Structure

```
workout-emailer/
├── .github/workflows/
│   └── daily-workout.yml    # GitHub Actions workflow
├── data/
│   ├── exercises.json       # Exercise database
│   └── history.json         # Workout history
├── src/
│   └── send_workout.py      # Main Python script
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## How It Works

1. **Scheduling**: GitHub Actions triggers the workflow daily at 10:00 AM UTC
2. **Muscle Group Selection**: Determines today's muscle group based on the day of week
3. **Exercise Selection**: Randomly selects exercises while avoiding repeats from the previous week
4. **Email Delivery**: Sends the workout email via SMTP
5. **History Update**: Commits updated workout history back to the repository

## Exercise Selection Logic

- Exercises are selected randomly from predefined pools for each muscle group
- The system tracks which exercises were used in the previous week for each muscle group
- Exercises from the previous week are excluded from selection
- If all exercises are exhausted, the system allows reuse except for the immediately previous week's exercises
- History is tracked per muscle group, not globally

## Customization

### Adding Exercises

Edit `data/exercises.json` to add or modify exercises:

```json
{
  "muscle_group": {
    "dumbbell": ["Exercise 1", "Exercise 2"],
    "bodyweight": ["Exercise 1", "Exercise 2"]
  }
}
```

### Changing Schedule

Modify the cron schedule in `.github/workflows/daily-workout.yml`:

```yaml
schedule:
  - cron: '0 10 * * *'  # 10:00 AM UTC daily
```

### Modifying Email Content

Edit the `create_email_content()` method in `src/send_workout.py`.

## Troubleshooting

### Common Issues

1. **Email not sending**: Check that all GitHub secrets are correctly configured
2. **Workflow not running**: Ensure GitHub Actions is enabled in your repository
3. **Time zone issues**: The workflow runs at 10:00 AM UTC - adjust if needed

### Viewing Logs

1. Go to **Actions** tab
2. Click on the workflow run
3. Expand the steps to view detailed logs

## Security

- All email credentials are stored in GitHub Secrets
- No credentials are hard-coded in the repository
- The workflow uses the minimum necessary permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.
=======
"# workout-emailer" 
"# workout-emailer" 
>>>>>>> 75444f6224c51ef88f1c979b023927c4694efc41
