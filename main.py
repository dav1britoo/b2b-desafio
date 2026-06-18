import os
import logging
import requests
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")

MAX_CONTACTS = 3


def get_contacts():
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    response = client.table("contacts").select("name, phone").limit(MAX_CONTACTS).execute()
    return response.data


def send_whatsapp(phone: str, name: str):
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"
    headers = {
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN,
    }
    payload = {
        "phone": phone,
        "message": f"Olá, {name} tudo bem com você?",
    }
    response = requests.post(url, json=payload, headers=headers, timeout=15)
    response.raise_for_status()
    return response.json()


def main():
    logger.info("Buscando contatos no Supabase...")
    contacts = get_contacts()

    if not contacts:
        logger.warning("Nenhum contato encontrado na tabela.")
        return

    logger.info(f"{len(contacts)} contato(s) encontrado(s). Iniciando envios...")

    for contact in contacts:
        name = contact["name"]
        phone = contact["phone"]
        try:
            result = send_whatsapp(phone, name)
            logger.info(f"Mensagem enviada para {name} ({phone}). Resposta: {result}")
        except requests.HTTPError as e:
            logger.error(f"Erro HTTP ao enviar para {name} ({phone}): {e.response.status_code} - {e.response.text}")
        except Exception as e:
            logger.error(f"Erro inesperado ao enviar para {name} ({phone}): {e}")

    logger.info("Envios concluídos.")


if __name__ == "__main__":
    main()
