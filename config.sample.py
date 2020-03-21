BOT_TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"

# Webhook configuration - If set to false we use long polling
USE_WEBHOOK = False
WEBHOOK_PORT = 9001
WEBHOOK_URL = "https://domain.example.com/" + BOT_TOKEN
CERTPATH = "/etc/certs/example.com/fullchain.cer"

# business logic settings
doctor_room = -123456789
psychologist_room = -987654321
newmembers_room = -789456123
