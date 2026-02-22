import requests
from models import Bridge

def get_deal_data(domain: str, token: str, deal_id: str) -> dict:
    """Получаем данные сделки из Bitrix24"""
    try:
        resp = requests.post(
            f"https://{domain}/rest/1/{token}/crm.deal.get",
            json={"ID": deal_id}
        )
        return resp.json().get("result", {})
    except Exception as e:
        print(f"Ошибка получения сделки: {e}")
        return {}

def render_template(template: str, deal: dict) -> str:
    """Подставляем переменные в шаблон"""
    def safe(val):
        return str(val) if val is not None else "—"
    
    return (template
        .replace("{TITLE}",    safe(deal.get("TITLE")))
        .replace("{AMOUNT}",   safe(deal.get("OPPORTUNITY")))
        .replace("{CURRENCY}", safe(deal.get("CURRENCY_ID")))
        .replace("{CONTACT}",  safe(deal.get("CONTACT_ID")))
        .replace("{COMPANY}",  safe(deal.get("COMPANY_ID")))
    )

def send_myteam(token: str, chat_id: str, text: str) -> bool:
    """Отправляем сообщение в MyTeam"""
    try:
        resp = requests.get(
            "https://api.internal.myteam.mail.ru/bot/v1/messages/sendText",
            params={"token": token, "chatId": chat_id, "text": text}
        )
        return resp.json().get("ok", False)
    except Exception as e:
        print(f"Ошибка отправки в MyTeam: {e}")
        return False

def process_event(bridge: Bridge, payload: dict) -> tuple:
    try:
        # ONCRMDEALADD — ID в data[FIELDS][ID]
        # ONCRMDEALUPDATE — ID тоже в data[FIELDS][ID]
        deal_id = (
            payload.get("data[FIELDS][ID]") or
            payload.get("data[FIELDS][CURRENT][ID]")
        )

        if not deal_id:
            return "error", "Не удалось получить ID сделки"

        if bridge.source_type == "bitrix24":
            domain = bridge.source_config.get("domain")
            token  = bridge.source_config.get("token")
            deal   = get_deal_data(domain, token, deal_id)
        else:
            return "error", "Неизвестный источник"

        message = render_template(bridge.template, deal)

        if bridge.target_type == "myteam":
            token   = bridge.target_config.get("token")
            chat_id = bridge.target_config.get("chat_id")
            success = send_myteam(token, chat_id, message)
            status  = "success" if success else "error"
        else:
            return "error", "Неизвестный получатель"

        print(f"✅ Мост {bridge.id} сработал — статус: {status}")
        return status, message

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return "error", str(e)
