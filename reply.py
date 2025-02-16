import speech_recognition as sr
from gtts import gTTS
import os
import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("話しかけて！")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="ja-JP")
        print(f"聞き取った: {text}")
        return text
    except sr.UnknownValueError:
        print("聞き取れんかった…")
        return None

def chat_with_haruka(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}]
    )
    return response['choices'][0]['message']['content']

def speak_response(response_text):
    tts = gTTS(text=response_text, lang='ja')
    tts.save("response.mp3")
    os.system("mpg123 response.mp3")  # Mac or Linux
    # playsound('response.mp3')  # Windowsならこっち

if __name__ == "__main__":
    while True:
        user_input = recognize_speech()
        if user_input:
            response = chat_with_haruka(user_input)
            print(f"はるか: {response}")
            speak_response(response)