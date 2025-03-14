import requests
import json

url = "https://graph.facebook.com/v21.0/561450780387786/messages"

# Phone number ID: 561450780387786
# WhatsApp Business Account ID: 3974520746096368

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer EAASDEgdtL8QBOxeNQsxeKCTZCweEHkATGDavTHrUi0QHT4sowgCqAvNZCpmfVYUTRnQy1NGVOiqQmqH9dX1DU0tZAtuMgqzVBuaWiUjV2ZAyIkCzA0ZAHEVE7tQQm5eZCMK8oTfhP9SjGeUKKjO46MdVEFu2WlpGbVr6K9ZCkMMPEKc0t35QYoI9nO9FZCj9Qp839wT2zkgROUeZB9oa0ErZCQLrIU8exl'
}



def send_whatsapp_message(phone_number, message):
    """
    Sends a WhatsApp text message using Meta's WhatsApp Cloud API.

    :param phone_number: Recipient's WhatsApp number in international format (e.g., "9190XXXXXXX")
    :param message: Text message to send
    :return: API response (JSON)
    """
    url = f"https://graph.facebook.com/v20.0/{'561450780387786'}/messages"
    headers = {
        "Authorization": f"Bearer {'EAASDEgdtL8QBOxeNQsxeKCTZCweEHkATGDavTHrUi0QHT4sowgCqAvNZCpmfVYUTRnQy1NGVOiqQmqH9dX1DU0tZAtuMgqzVBuaWiUjV2ZAyIkCzA0ZAHEVE7tQQm5eZCMK8oTfhP9SjGeUKKjO46MdVEFu2WlpGbVr6K9ZCkMMPEKc0t35QYoI9nO9FZCj9Qp839wT2zkgROUeZB9oa0ErZCQLrIU8exl'}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone_number,
        "type": "text",
        "text": {"body": message}
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Example Usage
if __name__ == "__main__":
    phone = "918436804144"  # Replace with recipient's number
    msg = "Hello! This is a test message from our Python script."
    
    response = send_whatsapp_message(phone, msg)
    print(response)