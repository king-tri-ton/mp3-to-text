import speech_recognition as sr

def record_vol():
	r = sr.Recognizer()

	with sr.AudioFile("path/to/mp3/name.wav") as source:
		audio = r.listen(source)
		print("Слушаю...")

	query = r.recognize_google(audio, language = 'ru-RU')
	f = open('data.txt', 'a')
	f.write(query + '\n')
	f.close()

record_vol()
print('Completed')