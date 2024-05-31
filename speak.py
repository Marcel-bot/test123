from gtts import gTTS
from pydub import AudioSegment
from simpleaudio import WaveObject
from io import BytesIO


def text_to_speech(text, lang='en', speed_factor=1.25):
    try:
        tts = gTTS(text=text, lang=lang)
        buf = BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)

        audio = AudioSegment.from_file(buf, format="mp3")

        new_frame_rate = int(audio.frame_rate * speed_factor)
        audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_frame_rate})
        audio = audio.set_frame_rate(44100)

        if len(audio) > 1000:
            audio = audio[:-300]

        temp_buf = BytesIO()
        audio.export(temp_buf, format="wav")
        temp_buf.seek(0)

        wave_obj = WaveObject.from_wave_file(temp_buf)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    except Exception:
        print('Nothing to say')
