"""
config.py -- Central configuration for PredictGuard.

Fill in real credentials here to make email/SMS notifications actually
fire. Without credentials, the app still runs fine -- notifications are
logged as "skipped, not configured" instead of crashing.
"""

# --- LEA Interface login (Deliverable c: "Secure interface for investigators") ---
# Demo-only hardcoded accounts. In production this would be a real
# authentication system (hashed passwords, SSO, or I4C's own identity provider).
LEA_CREDENTIALS = {
    "investigator1": "1234",
    "i4c_admin": "predictguard",
}

# --- Email notifications (Deliverable d) ---
# To enable real email alerts: use a Gmail account with an "App Password"
# (Google Account -> Security -> 2-Step Verification -> App Passwords).
EMAIL_ENABLED = False
EMAIL_SENDER_ADDRESS = "your_email@gmail.com"
EMAIL_SENDER_APP_PASSWORD = "your_16_char_app_password"
EMAIL_RECIPIENT = "lea_officer@example.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# --- SMS notifications (Deliverable d) ---
# To enable real SMS alerts: sign up for a free Twilio trial account
# (twilio.com), verify a recipient number, and fill these in.
SMS_ENABLED = False
TWILIO_ACCOUNT_SID = "your_twilio_account_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_FROM_NUMBER = "+10000000000"
SMS_RECIPIENT_NUMBER = "+910000000000"

# --- API/webhook notifications (Deliverable d) ---
# Defaults to httpbin.org, a free public test endpoint that echoes back
# whatever is POSTed to it -- this lets you show a REAL HTTP round trip
# firing and getting a real response, with no server setup needed.
# Point this at your own endpoint (e.g. a bank/CFCFRMS mock receiver) later.
API_WEBHOOK_ENABLED = True
API_WEBHOOK_URL = "https://httpbin.org/post"
