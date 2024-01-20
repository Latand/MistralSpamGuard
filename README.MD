# Telegram Bot with Spam Detection

## Introduction
This project is a Telegram bot designed to facilitate interactions within a specific Telegram group. A key feature is its integration with the Mistral AI API for efficient spam detection, enhancing user experience by maintaining a spam-free environment.

## Requirements
- Python 3.x
- aiogram
- betterlogging
- mistralai

## Installation
1. Clone the repository:
   ```
   git clone [repository link]
   ```
2. Navigate to the project directory:
   ```
   cd [project directory]
   ```
3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration
Create a `.env` file in the root directory and fill in the necessary details:
```
BOT_TOKEN=your_telegram_bot_token
MISTRAL_TOKEN=your_mistral_ai_api_key
```

## Usage
Run the bot with the following command:
```
python bot.py
```

## Spam Detection
The bot uses the Mistral AI API for detecting spam messages. When a message is identified as spam, the user is restricted from sending further messages, and the offending message is deleted.

## Contribution and Support
Contributions to this project are welcome. Please submit pull requests or issues through the project's GitHub repository. For support, contact [your contact information].
