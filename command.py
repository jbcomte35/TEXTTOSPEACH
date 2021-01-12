from google.cloud import texttospeech
import csv


def text_to_wav(voice_name, text, number):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    filename = f"{language_code}-{voice_name}-{number}.mp3"
    with open("EXPORTSV3/"+filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to "{filename}"')

def list_voices(language_code=None):
    client = texttospeech.TextToSpeechClient()
    response = client.list_voices(language_code=language_code)
    voices = sorted(response.voices, key=lambda voice: voice.name)

    print(f" Voices: {len(voices)} ".center(60, "-"))
    for voice in voices:
        languages = ", ".join(voice.language_codes)
        name = voice.name
        gender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
        rate = voice.natural_sample_rate_hertz
        print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")


# Read CSV FILES
compteur = 0

with open('textes-v5.csv', newline='', encoding='utf-8-sig') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in spamreader:
        compteur=compteur+1
        if len(row) :
            print(row[0]+ ' - '+row[1])
            text_to_wav("fr-FR-Wavenet-A", row[1], str(row[0]))

#list_voices("fr-FR")
#text_to_wav("fr-FR-Wavenet-A", "Dans votre vie professionnelle, aujourd’hui, où vous situez-vous ? ", 1)
#text_to_wav("fr-FR-Wavenet-C", "Dans votre vie professionnelle, aujourd’hui, où vous situez-vous ? ", 1)
#text_to_wav("fr-FR-Wavenet-E", "Dans votre vie professionnelle, aujourd’hui, où vous situez-vous ? ", 1)
