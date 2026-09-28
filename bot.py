import os
import requests

def generar_contenido():
    api_key = os.getenv("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = """
    Actúa como un creador de contenido para una página de Facebook sobre la cultura chola y urbana en México. 
    Escribe una reflexión corta, profunda y callejera sobre la lealtad, el respeto, la familia, el barrio o la superación personal. 
    El texto debe ser viral, auténtico y directo. Incluye emojis (como 💯, 🙏, 🎭, 👊). 
    Entrégame SOLO el texto final listo para publicar en Facebook, sin saludos ni comillas.
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    respuesta = requests.post(url, json=payload)
    datos = respuesta.json()
    
    try:
        texto = datos['candidates'][0]['content']['parts'][0]['text']
        return texto
    except Exception as e:
        print("Error de la IA:", datos)
        return "Error al generar texto"

def publicar(texto):
    url_destino = os.getenv("WEBHOOK_URL")
    
    # ¡AQUÍ ESTÁ EL CAMBIO CLAVE! Mandamos las 3 variables que Make está esperando
    payload = {
        "texto_post": texto,
        "indicacion_para_API_FOTO": "Crea una imagen fotorrealista que represente la cultura urbana y el barrio en México, estilo callejero.",
        "indicacion_para_API_VIDEO": "Genera un video corto estilo cinemático sobre el respeto y la lealtad en el barrio."
    }
    
    respuesta = requests.post(url_destino, json=payload)
    
    if respuesta.status_code in [200, 201, 202]:
        print("¡Enviado a Make con éxito!")
    else:
        print(f"Error al enviar: {respuesta.status_code} - {respuesta.text}")

if __name__ == "__main__":
    post_generado = generar_contenido()
    print("Contenido:\n", post_generado)
    
    if post_generado != "Error al generar texto":
        publicar(post_generado)
