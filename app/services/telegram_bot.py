import httpx

TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"

async def send_telegram_notification(
        table_number: int, 
        guest_name: str, 
        starts_at: str
):
    """Асихронно отправка уведомление в Telegram черех библиотеку httpx"""

    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("Telegram Bot не настроен, пропускаем отправку")
        return 
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    message = (
        f"<b>Новая бронь в ReserveMaster</b>\n\n"
        f"<b>Стол</b>{table_number}\n"
        f"<b>Гость</b> {starts_at}"
    )

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        async with httpx.AsyncClient() as client:
            await client.post(url, json=payload, timeout=5.0)
    except Exception as e:
        print(f"ошибка отправки уведомление в Telegram {e}")
