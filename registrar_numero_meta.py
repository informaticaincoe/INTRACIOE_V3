# import requests

# # Configuración de datos
# ACCESS_TOKEN = 'EAAHmK0fOvhoBO9TgNxPxW7BwSKukP7qXLS5AV0nPaBZCUiwu5ZBzUNZBLPQ1EgMLGQWhS9yceDpC8SDRQEZBGGUoHzhSDm3Q4WjZAtVW9WBj2U3ZANeZCzBf6ZC310gu8LHQDbNCjZCvZBqLwf3uLilmUEuebPpYwNaGuVBuQx0gfcbUW6Xl7YXpKJUZBmLpKOrjPZBkTP9VueLEjQZDZD'
# CERTIFICADO = """CnwKOAiSlvXAiaKnAxIGZW50OndhIh9JbnZlcnNpb25lcyBDb21lcmNpYWxlcyBFc2NvYmFyUPT717kGGkDJNzVzZC5qU8Jj0xTJJ38zDla9CHcd+2Zdmqqh8zotYPEn2HZMoGDvfCbXmAqJUC9U7SiFRnJRAahmSvV/z7MFEi1tazbWt9+wXOBDi7Kbq2UskVrl7FjtNOaRdYdojVR8EKc7TmeXg7K7+cpl6X4"""
# PHONE_NUMBER = '78540194'
# COUNTRY_CODE = '503'
# METHOD = 'sms'
# PHONE_NUMBER_ID = '425139964026024'  # Debe ser el ID correcto del número de teléfono en la cuenta de WhatsApp

# # URL del endpoint correcto
# url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/register"

# # Payload
# payload = {
#     "cc": COUNTRY_CODE,
#     "phone_number": PHONE_NUMBER,
#     "method": METHOD,
#     "cert": CERTIFICADO,
# }

# # Headers para autenticación
# headers = {
#     "Authorization": f"Bearer {ACCESS_TOKEN}",
#     "Content-Type": "application/json"
# }

# # Solicitud POST
# response = requests.post(url, json=payload, headers=headers)

# # Verificar respuesta
# if response.status_code == 201:
#     print("Registro completado.")
# elif response.status_code == 202:
#     print("Código de verificación enviado. Revisa tu SMS o mensaje de voz.")
# else:
#     print("Error al verificar el número de teléfono.")
#     print("Código de estado:", response.status_code)
#     print("Detalles del error:", response.json())


import requests

url = "https://graph.facebook.com/v21.0/481415631717109/phone_numbers"
headers = {
    "Authorization": "Bearer EAAHmK0fOvhoBO9TgNxPxW7BwSKukP7qXLS5AV0nPaBZCUiwu5ZBzUNZBLPQ1EgMLGQWhS9yceDpC8SDRQEZBGGUoHzhSDm3Q4WjZAtVW9WBj2U3ZANeZCzBf6ZC310gu8LHQDbNCjZCvZBqLwf3uLilmUEuebPpYwNaGuVBuQx0gfcbUW6Xl7YXpKJUZBmLpKOrjPZBkTP9VueLEjQZDZD"
}
response = requests.get(url, headers=headers)
print(response.json())