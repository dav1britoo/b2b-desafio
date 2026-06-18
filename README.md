# b2bflow Challenge — WhatsApp Message Sender

Lê contatos do Supabase e envia via Z-API a mensagem:
> "Olá, \<nome_contato\> tudo bem com você?"

## Setup da tabela (Supabase)

No painel do Supabase, execute no SQL Editor:

```sql
create table contacts (
  id serial primary key,
  name text not null,
  phone text not null
);

insert into contacts (name, phone) values
  ('Maria', '5511999990001'),
  ('João', '5511999990002'),
  ('Ana', '5511999990003');
```

> O campo `phone` deve estar no formato internacional sem `+` (ex: `5511999990001`).

## Variáveis de ambiente

Copie `.env.example` para `.env` e preencha:

```env
SUPABASE_URL=https://xxxxxxxxxxx.supabase.co
SUPABASE_KEY=your_supabase_anon_key

ZAPI_INSTANCE_ID=your_instance_id
ZAPI_TOKEN=your_token
ZAPI_CLIENT_TOKEN=your_client_token
```

- **SUPABASE_URL / SUPABASE_KEY** → Project Settings → API no painel do Supabase.
- **ZAPI_*** → painel da Z-API na instância conectada ao WhatsApp.

## Como rodar

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar
python main.py
```

## Exemplo de saída

Output real obtido durante a execução do projeto:

```
2026-06-18 15:11:11,265 [INFO] Buscando contatos no Supabase...
2026-06-18 15:11:12,320 [INFO] HTTP Request: GET .../rest/v1/contacts?select=name%2Cphone&limit=3 "HTTP/2 200 OK"
2026-06-18 15:11:12,327 [INFO] 3 contato(s) encontrado(s). Iniciando envios...
2026-06-18 15:11:12,532 [INFO] Mensagem enviada para Maria (5511999990001). Resposta: {'zaapId': '019EDBEE...', 'messageId': '3EB033...'}
2026-06-18 15:11:12,714 [INFO] Mensagem enviada para João (5511999990002). Resposta: {'zaapId': '019EDBEE...', 'messageId': '3EB0B8...'}
2026-06-18 15:11:12,899 [INFO] Mensagem enviada para Ana (5511999990003). Resposta: {'zaapId': '019EDBEE...', 'messageId': '3EB0B5...'}
2026-06-18 15:11:12,899 [INFO] Envios concluídos.
```
