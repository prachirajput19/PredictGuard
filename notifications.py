"""
notifications.py -- Deliverable (d): Alert & Notification System.

Real implementations for email (SMTP), SMS (Twilio), and API/webhook
notifications. Each function returns a result dict describing what
actually happened -- sent, skipped (not configured), or failed (with the
real error) -- so the UI can show honest status rather than pretending
everything fired.
"""

import smtplib
from email.mime.text import MIMEText

import requests

import config


def send_email_alert(alert: dict) -> dict:
    if not config.EMAIL_ENABLED:
        return {"channel": "email", "status": "skipped", "detail": "Email not configured (EMAIL_ENABLED=False in config.py)"}

    try:
        subject = f"PredictGuard ALERT - {alert['ring_id']} - Risk {alert['risk_score']:.2f}"
        body = (
            f"Ring ID: {alert['ring_id']}\n"
            f"Predicted location: {alert['predicted_location']}\n"
            f"Predicted time window: {alert['predicted_time_window']}\n"
            f"Risk score: {alert['risk_score']:.2f}\n"
        )
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = config.EMAIL_SENDER_ADDRESS
        msg["To"] = config.EMAIL_RECIPIENT

        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT, timeout=8) as server:
            server.starttls()
            server.login(config.EMAIL_SENDER_ADDRESS, config.EMAIL_SENDER_APP_PASSWORD)
            server.sendmail(config.EMAIL_SENDER_ADDRESS, config.EMAIL_RECIPIENT, msg.as_string())

        return {"channel": "email", "status": "sent", "detail": f"Email sent to {config.EMAIL_RECIPIENT}"}
    except Exception as e:
        return {"channel": "email", "status": "failed", "detail": str(e)}


def send_sms_alert(alert: dict) -> dict:
    if not config.SMS_ENABLED:
        return {"channel": "sms", "status": "skipped", "detail": "SMS not configured (SMS_ENABLED=False in config.py)"}

    try:
        from twilio.rest import Client  # imported lazily so the package is only required if SMS is actually used

        client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
        body = (
            f"PredictGuard ALERT: Ring {alert['ring_id']} risk {alert['risk_score']:.2f} "
            f"predicted at {alert['predicted_location']} ({alert['predicted_time_window']})"
        )
        message = client.messages.create(
            body=body, from_=config.TWILIO_FROM_NUMBER, to=config.SMS_RECIPIENT_NUMBER,
        )
        return {"channel": "sms", "status": "sent", "detail": f"SMS sent, SID={message.sid}"}
    except ImportError:
        return {"channel": "sms", "status": "failed", "detail": "twilio package not installed (pip install twilio)"}
    except Exception as e:
        return {"channel": "sms", "status": "failed", "detail": str(e)}


def send_api_webhook(alert: dict) -> dict:
    """POSTs the alert to a webhook URL -- demonstrates the real 'API
    trigger' notification channel. Defaults to httpbin.org (a free public
    echo endpoint) so this works out of the box with no server setup,
    while still being a genuine HTTP round trip, not a mock."""
    if not config.API_WEBHOOK_ENABLED:
        return {"channel": "api", "status": "skipped", "detail": "API webhook disabled (API_WEBHOOK_ENABLED=False in config.py)"}

    try:
        response = requests.post(config.API_WEBHOOK_URL, json=alert, timeout=6)
        return {
            "channel": "api",
            "status": "sent" if response.ok else "failed",
            "detail": f"POST {config.API_WEBHOOK_URL} -> HTTP {response.status_code}",
        }
    except Exception as e:
        return {"channel": "api", "status": "failed", "detail": str(e)}


def notify_all_channels(alert: dict) -> list:
    """Fires all three channels for one alert and returns a list of result
    dicts (one per channel) for display in the UI / ledger."""
    return [
        send_email_alert(alert),
        send_sms_alert(alert),
        send_api_webhook(alert),
    ]


if __name__ == "__main__":
    dummy_alert = {
        "alert_id": "ALTTEST0001", "ring_id": "RING999",
        "predicted_location": "Test City", "predicted_time_window": "Next 1-2 hours",
        "risk_score": 0.91,
    }
    for result in notify_all_channels(dummy_alert):
        print(result)
