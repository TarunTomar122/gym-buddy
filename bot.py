import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import requests
import os

language = 'en'

# Create a Recognizer object
r = sr.Recognizer()

lastMessage = ""

# Set the device index to the default microphone
with sr.Microphone() as source:

    while True:

        # Print a message indicating that the script is listening
        print("Listening...")

        # Listen for audio from the microphone
        audio = r.listen(source)

        # Try to recognize the audio as speech
        try:
            text = r.recognize_google(audio)
        except sr.UnknownValueError:
            text = ""

        # If the text contains the word "bestie", start converting audio to text
        if "bestie" in text.lower():

            myobj = gTTS(text="hi, what's up!", lang=language, slow=False)

            # Saving the converted audio in a mp3 file named
            # welcome
            myobj.save("welcome.mp3")

            # Playing the converted file
            playsound("welcome.mp3")
            os.remove("welcome.mp3")

            while True:
                # Listen for more audio from the microphone
                audio = r.listen(source)

                # Try to recognize the audio as speech
                try:
                    text = r.recognize_google(audio)
                except sr.UnknownValueError:
                    text = ""

                if len(text)==0:
                    continue

                # If the text contains the word "over", stop converting audio to text
                if "yes" in text.lower():

                    # send this text to rasa and rasa will start this action
                    response = requests.post(
                        'http://localhost:5005/webhooks/rest/webhook', json={'sender': 'Tarun', 'message': lastMessage})
                    
                    print(response)

                    break

                # Print the recognized text
                print(f"You said: {text}")

                lastMessage = text
                reply = "you said - "+text+" ...right?"
                myobj = gTTS(
                    text=reply, lang=language, slow=False)

                # Saving the converted audio in a mp3 file named
                # welcome
                myobj.save("welcome.mp3")

                # Playing the converted file
                playsound("welcome.mp3")
                os.remove("welcome.mp3")

        else:
            print("Did not receive the start command.")
