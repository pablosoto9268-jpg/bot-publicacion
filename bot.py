import os
import requests
import google.generativeai as genai

# Configurar la API de Gemini usando tu secreto de GitHub
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generar_contenido():
    # Usamos el modelo de Gemini
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = "Eres un experto en redes sociales. Escribe un consejo corto de 2 párrafos sobre tecnología y productividad, ideal para Facebook. Escribe de forma directa, sin saludos ni hashtags excesivos."
    
    respuesta = model.generate_content(prompt)
    return respuesta.text

def publicar(texto):
    # Obtiene la URL de Make.com de tus secretos
    url_destino = os.getenv("WEBHOOK_URL") 
    
    # Prepara el texto para enviarlo a Make
    payload = {"contenido": texto}
    respuesta = requests.post(url_destino, json=payload)
    
    if respuesta.status_code in [200, 201, 202]:
        print("¡Enviado a Make con éxito!")
    else:
        print(f"Error al enviar: {respuesta.status_code} - {respuesta.text}")

if __name__ == "__main__":
    post_generado = generar_contenido()
    print("Contenido generado:\n", post_generado)
    publicar(post_generado)
