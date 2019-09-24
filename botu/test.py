import speech_recognition as sr
 
r = sr.Recognizer()
with sr.AudioFile('sample001.wav') as src:
    audio = r.record(src)
print(r.recognize_google(audio, key='AIzaSyBhxSlMyTsC4kHNX5x6qfH1B8FQMZxrAP4', language='ja-JP'))