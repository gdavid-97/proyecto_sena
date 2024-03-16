import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config
import google.generativeai as genai

EMAIL = config("EMAIL")
CONTRASEÑA = config("PASSWORD")
GOOGLE_API_KEY = config('GOOGLE_API_KEY')
NEWS_API_KEY = config("NEWS_API_KEY")

def buscar_wikipedia(query):
    wikipedia.set_lang('es')
    resultados = wikipedia.summary(query, sentences=1)
    return resultados

def buscar_ip():
    direccion_ip = requests.get('https://api64.ipify.org?format=json').json()
    return direccion_ip["ip"]

def youtube(video):
    kit.playonyt(video)

def enviar_whatsapp(numero, mensaje):
    kit.sendwhatmsg_instantly(f"+57{numero}", mensaje)

def google(query):
    kit.search(query)


def enviar_email(destinatario, asunto, mensaje):
    try:
        email = EmailMessage()
        email['To'] = destinatario
        email["Subject"] = asunto
        email['From'] = EMAIL
        email.set_content(mensaje)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, CONTRASEÑA)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False
    

def noticias():
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=co&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]



def ai(query, stream = False):
    genai.configure(api_key= GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name = 'gemini-pro')
    prompt = query
    response = model.generate_content(
        contents=prompt,
        stream=stream)
    try:
        if stream:      
            return response  #stream=True en generate_content
        else:
            return response.text 
    except Exception as e:
        print(f'{type(e).__name__}: {e}')
    