from speech_recognition import Recognizer, Microphone, RequestError
import ollama
from speak import text_to_speech
from serial import Serial
from time import sleep

ser = Serial('/dev/ttyUSB1', 9600)

sr = Recognizer()

while True:
    try:
        print("Say something: ")

        with Microphone() as source:
            sr.adjust_for_ambient_noise(source)
            audio_data = sr.listen(source)

        print("You said: ")

        text = ''

        try:
            text = sr.recognize_google(audio_data)

        except Exception as e:
            pass

        print(text)

        if text.replace(',', '').replace('.', '').replace('!', '').replace('?', '').strip() == '':
            continue

        response = ollama.chat(
            model='marcel',
            messages=[{
                'role': 'user',
                'content': text,
                'stream': False
            }],
            stream=True
        )

        phrase = ''

        for chunk in response:
            phrase += chunk['message']['content']

            if any(char in chunk['message']['content'] for char in '.,!') and len(phrase) > 100:
                print(phrase)

                if 'shake' in phrase.lower():
                    ser.write('1\n'.encode('utf-8'))

                if 'yes' in phrase.lower():
                    ser.write('y\n'.encode('utf-8'))

                if 'no' in phrase.lower():
                    ser.write('n\n'.encode('utf-8'))

                text_to_speech(phrase)

                phrase = ''

        print(phrase)

        if 'shake' in phrase.lower():
            ser.write('1\n'.encode('utf-8'))

        if 'yes' in phrase.lower():
            ser.write('y\n'.encode('utf-8'))

        if 'no' in phrase.lower():
            ser.write('n\n'.encode('utf-8'))

        text_to_speech(phrase)

    except RequestError:
        pass
