"""docstring"""
from datetime import datetime
import os
import requests

MM_URL = os.getenv("MM_URL", "https://your-mattermost-instance.com")
MM_TOKEN = os.getenv("MM_TOKEN", "YOUR_ACCESS_TOKEN")
MM_USER_ID = os.getenv("MM_USER_ID", "YOUR_USER_ID")
MM_STATUS = os.getenv("MM_STATUS", "online")
# Time in epoch seconds at which a dnd status would be unset.
MM_STATUS_DND_END_TIME = os.getenv("MM_STATUS_DND_END_TIME")
if MM_STATUS_DND_END_TIME is not None:
    MM_STATUS_DND_END_TIME = int(MM_STATUS_DND_END_TIME)
MM_STATUS_EMOJI = os.getenv("MM_STATUS_EMOJI", "house")
MM_STATUS_TEXT = os.getenv("MM_STATUS_TEXT", "Working from home")
# The time at which custom status should be expired. It should be in ISO format.
MM_STATUS_EXPIRES_AT = os.getenv("MM_STATUS_EXPIRES_AT")
REQUESTS_TIMEOUT = float(os.getenv("REQUESTS_TIMEOUT", "10"))

headers = {
    "Authorization": f"Bearer {MM_TOKEN}",
    "Content-Type": "application/json"
}


def send_request(
    url: str | bytes,
    payload,
):
    """
    Function for sending request to MM REST API
    """
    response = requests.put(
        url,
        json=payload,
        headers=headers,
        timeout=REQUESTS_TIMEOUT
    )

    if response.status_code == 200:
        print(f"Status successfully set at {datetime.now()}")
    else:
        print(
            f"Status failed to set. Status code: {response.status_code}, {response.text}"
        )


def set_status(
    user_id: str = MM_USER_ID,
    status: str = MM_STATUS,
    dnd_end_time: int | None = MM_STATUS_DND_END_TIME
):
    """
    Function to set Mattermost status
    """

    url = f"{MM_URL}/api/v4/users/{user_id}/status"
    payload = {
        "user_id": user_id,
        "status": status,
        "dnd_end_time": dnd_end_time,
    }
    send_request(url, payload)


def set_custom_status(
    user_id: str = MM_USER_ID,
    emoji: str = MM_STATUS_EMOJI,
    text: str = MM_STATUS_TEXT,
    duration: str | None = None,
    expires_at: str | None = MM_STATUS_EXPIRES_AT
):
    """
    Function to set custom Mattermost status
    """

    url = f"{MM_URL}/api/v4/users/{user_id}/status/custom"
    payload = {
        "user_id": user_id,
        "emoji": emoji,
        "text": text,
        "duration": duration,
        "expires_at": expires_at
    }
    send_request(url, payload)


if __name__ == "__main__":
    set_status()
    set_custom_status()
