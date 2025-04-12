import time
import requests

# Authentication tokens list
auth_tokens = [
    "C7BB916D5E5575A60586C3B5FB72A34","F0A0996A2C2B417FBCE1C4E1AB81EAC","45B43268ED961B7BD1E54917EFE3AB9","EA4F6C7A2A2957FD5D0D66E1DC5C","1A12D94804DB93A5D1BA0ECF417D41C","D38262F4E13D1AD5639C8CEB5A73229","878BE644F1BB73FE962E16F509C58B","80865E8EBC16EFDF92FAA4C4D9B462","5A39616BC94B845D16467B722F137593","47E45F9D48356C60D4B91E58AD4564E","68A1372EE178BE7EAB80DEDDBD411A0","D056D1E41BE37C20389A6CEB289F567D","DA61C0B2FE2D744B355D4BAD14A4ACE5","4067E67E67C16648CE6B54B7D7D5B748","8CAC8E73A2E3496708679236EF58D25","5A7D20A0332FD0E88AE29695296B3","E3A1836D9FF49B3A682D7E44F273375","D7E79DEA76455F95269B7385A88FDC2C","174B3C496AC3E8EC189E7E98BDAD70","DD25B16D5FAD27D6257F7D49736795B","10FDDF67B997DF5296562E66984A27F0","89A2115F9C3C52E73B18829352F4925","E2C53D5D381827CC7AE9C08C113334FC","9539D4D4CF4414CC185742216568CDE","E2437ED9508C69C4F978D0E15E4875DB"
,"C7BB916D5E5575A60586C3B5FB72A34","F9BB68A8B72A7BB110D91FCB257C98C1","ECD9F15EA49F293EF234C1DAA3F90F1",  # Add more tokens here
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
    last_run_time = time.time()  # Track last time the 5-minute message was sent
    while True:
        check_balances()

        # Notify every 5 minutes
        if time.time() - last_run_time >= 300:  # 300 seconds = 5 minutes
            print("Bot is running...")
            last_run_time = time.time()  # Update last run time

        time.sleep(30)


