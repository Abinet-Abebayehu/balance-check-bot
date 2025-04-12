import time
import requests

# Authentication tokens list
auth_tokens = [
    "C7BB916D5E5575A60586C3B5FB72A34","F9BB68A8B72A7BB110D91FCB257C98C1","ECD9F15EA49F293EF234C1DAA3F90F1",  # Add more tokens here
]

# Telegram bot credentials
bot_token = "7573403773:AAHHkr3U8_AG3AlT6OvO59Qn4NJ9FrIfb8U"
chat_id = "1775369463"

# API endpoint to check balance
url = "https://ahadubirr.com/api/v1/User/GetAvailableWithdraw"

# Store last known balances
last_balances = {}

def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        requests.post(telegram_url, data=payload)
    except Exception as e:
        print(f"Telegram error: {e}")

def check_balances():
    global last_balances
    for token in auth_tokens:
        headers = {
            "Access-Token": token
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                current_balance = data.get("amount")
                print(f"Bot is running... Last balance: {last_balances.get(token, 'N/A')}")
                if token not in last_balances or last_balances[token] != current_balance:
                    last_balances[token] = current_balance
                    send_telegram_message(f"💰 Balance changed for token {token[:5]}...: {current_balance}")
            else:
                print(f"Failed to fetch balance for token {token[:5]}... (Status: {response.status_code})")
        except Exception as e:
            print(f"Error checking balance for token {token[:5]}...: {e}")

if __name__ == "__main__":
    send_telegram_message("🤖 Bot started and is monitoring balances.")
    while True:
        check_balances()
        time.sleep(30)

