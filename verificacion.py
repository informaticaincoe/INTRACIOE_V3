import requests
import json

def send_whatsapp_message_with_attachment(to_phone_number, template_name, variables, button_url, language_code="es"):
    # URL del endpoint para enviar mensajes
    url = "https://graph.facebook.com/v20.0/461495207047495/messages"
    
    # Token de acceso
    access_token = "EAAHmK0fOvhoBO9KmTjioKw2bWwnsIJU0vWZBJ8kUb0i3xdPbKXNwKmuo3tKiOtNgSyaZBtSL2oASehRdBqcejjLioFjqMNqV0HJZCpLFQCB2MzNraoNEEJApTdz27mhGLotZBVR6g1H2ZB1kFtyFcHisa6J3JNK5T6AUfX6QD6RbnBrSFEU8xMwrOSvbb0uZCL96AAWarfgRzM3Y6yzVW5VBDE2JQJa0ZBMsbZBFulb7fbkZD"

    # Encabezados de la solicitud
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Cuerpo de la solicitud con variables y el enlace en el botón
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone_number,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {
                "code": language_code
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": variables[0]},  # Primer parámetro (ej: nombre)
                        {"type": "text", "text": variables[1]},  # Segundo parámetro
                        {"type": "text", "text": variables[2]}   # Tercer parámetro
                    ]
                },
                {
                    "type": "button",
                    "sub_type": "url",
                    "index": "0",
                    "parameters": [
                        {"type": "text", "text": button_url}  # URL del botón (ej: https://google.com)
                    ]
                }
            ]
        }
    }

    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, json=payload)

    # Verificar la respuesta
    if response.status_code == 200:
        print("Mensaje enviado correctamente.")
    else:
        print(f"Error al enviar el mensaje: {response.status_code}")
        print("Detalles:", response.json())

# Ejemplo de uso
variables = ["Nombre del Empleado", "14.25", "450.00"]
button_url = "https://google.com"  # URL del botón
send_whatsapp_message_with_attachment("50377462310", "boleta_text", variables, button_url)
