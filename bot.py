import os
import requests

def generar_contenido():
    # Nos conectamos directo a la API sin usar librerías de terceros
    api_key = os.getenv("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = "Eres un experto en redes sociales. Escribe un consejo corto de 2 párrafos sobre tecnología y productividad, ideal para Facebook. Escribe de forma directa."
    
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
    payload = {"contenido": texto}
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
