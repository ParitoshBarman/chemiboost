import requests
import json

# url = "https://graph.facebook.com/v20.0/358554990685260/messages"
# url = "https://graph.facebook.com/v20.0/402625082939997/messages"
url = "https://graph.facebook.com/v21.0/561450780387786/messages"

# Phone number ID: 561450780387786
# WhatsApp Business Account ID: 3974520746096368


# payload = json.dumps({
#   "messaging_product": "whatsapp",
#   "to": "919091467852",
#   "type": "template",
#   "template": {
#     "name": "hello_world",
#     "language": {
#       "code": "en_US"
#     }
#   }
# })
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer EAASDEgdtL8QBO4NvQWJvy94vnPkuKcLvxcUMmbC7BG9r2Q6Or5GZAWx7yzoDWAxZAlZBtwGv56FczAi0s0zywZCVMwrsoEMaGFZCp1J600ImYQSdCK8ycM32ogL9C7cTv3cOEtgX8ZAy6HWimV2te0q9qGfqUVHQ7sekWtGpQrKNSkrZB6mLZA461opfizPcaSzYKYMZBCkBPsifF5AAmpsfl8zWiWU8ZD'
                        #    EAAaOmHGiL78BOZCoUvtA4ZB2fj8fQhm2oxZBZAmh8R3r4xivnRyFfuLH6qXlVQ4rqUy0RhgyotqbezbXbX1Y7Pco1OKYzsfvPom004tCnp39ANKVV5lOuxv6ziw4Sg2T3nkflyiM9ZCyJr9mOdu2PRf5qzhWdvUPFYyHcCHBXzBwzyYbu7zZCsTPfolBr9QmcHGD3ZAI1bXsZCuCJY1jRFhkGES2dD4ZD
}

#   'Authorization': 'Bearer EAARFP9GM4eQBOZCL2Iz4R9YQkA0hvFDxSikgICG6zrvtkVFoOhasEWllI7gUPUhltOXHniueRQqMBGQZAS1T6GSOBXhSQgKLAhIv5ZCGUNY2eyw8qaRmyS3RBuUj7THDfJoJ1vd3ByK9UN451SntHEjpHiAj6DXiNEnKfj2go3m00OZCSYcE0YkCNRYiJzeFOSXxAQETI6MFmiNvRTrZCmfIzPqoxuLhFKHAnzKlR4HEZD'
# response = requests.request("POST", url, headers=headers, data=payload)

# print(response.text)


def sendText(msg, number):
    payload = json.dumps({
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": f"{number}",
    "type": "text",
    "text": {
    "preview_url": True,
    "body": f"{msg}"
        }
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def sendTemplate(templateName, number):
    payload = json.dumps({
    "messaging_product": "whatsapp",
    "to": f"{number}",
    "type": "template",
    "template": {
        "name": f"{templateName}",
        "language": {
        "code": "en_US"
        }
    }
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def sendReplyButton(msg, number):
    payload = json.dumps({
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": f"{number}",
    "type": "interactive",
    "interactive": {
        "type": "button",
        "body": {
        "text": f"{msg}"
        },
        "action": {
        "buttons": [
            {
            "type": "reply",
            "reply": {
                "id": "123",
                "title": "Yes"
            }
            },
            {
            "type": "reply",
            "reply": {
                "id": "122354",
                "title": "No"
            }
            },
        ]
        }
    }
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)




sendText("Hi Paritosh How are you I am fine", "918436804144")
sendTemplate("hello_world", "918436804144")
# sendTemplate("first_template2", "919091467852")
# sendReplyButton("Are you interested?", "918436804144")
# sendReplyButton("Are you Intarested?", "919667558942")