import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random

# === Konfiguracja i Kolory ===
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

sample_rate = 44100
duration = 4
max_errors = 3
score = 0
errors = 0

languages_config = {
    "en": {"name": "Angielski", "code": "en-US", "dest": "en"},
    "es": {"name": "Hiszpański", "code": "es-ES", "dest": "es"},
    "de": {"name": "Niemiecki", "code": "de-DE", "dest": "de"},
    "fr": {"name": "Francuski", "code": "fr-FR", "dest": "fr"},
}

words_by_level = {
    "łatwy": ["kot", "pies", "dom", "ptak", "mleko"],
    "średni": ["szkoła", "komputer", "książka", "przyjaciel", "żółty"],
    "trudny": ["przyszłość", "wyobraźnia", "doświadczenie", "satysfakcja"]
}

print("🏰 " + GREEN + "Witaj w Speak Right!" + RESET)

print("\nWybierz język nauki (wpisz skrót):")
for k, v in languages_config.items():
    print(f"🔹 {k} -> {v['name']}")

lang_choice = input(">>> ").lower()
while lang_choice not in languages_config:
    lang_choice = input("❌ Wybierz z listy (en/es/de): ").lower()

selected_lang = languages_config[lang_choice]

# Wybór Poziomu
level = input("\nWybierz poziom (łatwy/średni/trudny): ").lower()
while level not in words_by_level:
    level = input("❌ Brak poziomu. Spróbuj: łatwy, średni, trudny: ").lower()

words = list(words_by_level[level])
translator = Translator()

print(f"\n🟢 Język: {selected_lang['name']} | Życia: {max_errors}")


while errors < max_errors and len(words) > 0:
    word = random.choice(words)
    words.remove(word)
    
    translation = translator.translate(word, src='pl', dest=selected_lang['dest']).text.lower()
    
    print(f"\n📁 Słowo po polsku: **{word}**")
    print(f"🎙️ Powiedz to po {selected_lang['name']}...")

    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16', device = 4)
    sd.wait()
    wav.write("output.wav", sample_rate, recording)
    
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)
        
        recognized_text = recognizer.recognize_google(audio, language=selected_lang['code']).lower()
        print(f"📄 Rozpoznano: {recognized_text}")

        if recognized_text == translation:
            score += 1
            print(GREEN + f"✅ DOBRZE! Wynik: {score}" + RESET)
        else:
            errors += 1
            print(RED + f"❌ BŁĄD! Powiedziałeś: {recognized_text}" + RESET)
            print(f"💡 Poprawna odpowiedź to: {GREEN}{translation}{RESET}") 
            print(f"❤️ Pozostałe życia: {max_errors - errors}")

    except sr.UnknownValueError:
        errors += 1
        print(RED + "🔊 Nie usłyszałem Cię wyraźnie." + RESET)
        print(f"💡 Powinieneś był powiedzieć: {GREEN}{translation}{RESET}") 
        print(f"❤️ Pozostałe życia: {max_errors - errors}")

if errors >= max_errors:
    print(RED + "\n💀 KONIEC GRY! Straciłeś wszystkie życia." + RESET)
else:
    print(GREEN + "\n🏆 BRAWO! Wszystkie słówka zaliczone!" + RESET)

print(f"Finalny wynik: {score}")