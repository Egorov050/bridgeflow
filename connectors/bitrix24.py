import requests

def register_webhook(domain: str, token: str, event_type: str, handler_url: str) -> bool:
    """Регистрируем вебхук через REST API Bitrix24"""
    try:
        resp = requests.get(
            f"https://{domain}/rest/1/{token}/event.bind",
            params={
                "event": event_type,
                "handler": handler_url
            }
        )
        result = resp.json()
        print(f"Регистрация вебхука: {result}")
        return "result" in result
    except Exception as e:
        print(f"Ошибка регистрации вебхука: {e}")
        return False

def unregister_webhook(domain: str, token: str, event_type: str, handler_url: str) -> bool:
    """Удаляем вебхук из Bitrix24"""
    try:
        resp = requests.post(
            f"https://{domain}/rest/1/{token}/event.unbind",
            json={
                "event": event_type,
                "handler": handler_url
            }
        )
        return "result" in resp.json()
    except Exception as e:
        print(f"Ошибка удаления вебхука: {e}")
        return False
    
    
    