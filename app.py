import os
import sys
import urllib.request
import zipfile
import shutil

# Указываем Pydub путь к ffmpeg и ffprobe
FFMPEG_DIR = os.path.join(os.path.dirname(__file__), "ffmpeg", "bin")
os.environ["PATH"] += os.pathsep + FFMPEG_DIR

from pydub import AudioSegment
import speech_recognition as sr

FFMPEG_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
FFMPEG_DIR = os.path.join(os.path.dirname(__file__), "ffmpeg")
FFMPEG_BIN = os.path.join(FFMPEG_DIR, "bin", "ffmpeg.exe")
FFPROBE_BIN = os.path.join(FFMPEG_DIR, "bin", "ffprobe.exe")

def download_and_extract_ffmpeg():
    """Скачивает и распаковывает FFmpeg в правильную папку, удаляя лишнее."""
    if not os.path.exists(FFMPEG_BIN) or not os.path.exists(FFPROBE_BIN):
        print("Скачиваю FFmpeg...")
        zip_path = os.path.join(os.path.dirname(__file__), "ffmpeg.zip")
        urllib.request.urlretrieve(FFMPEG_URL, zip_path)

        print("Распаковываю FFmpeg...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(FFMPEG_DIR)
        
        os.remove(zip_path)

        # Найдём папку, в которую разархивировался ffmpeg
        extracted_folder = os.path.join(FFMPEG_DIR, os.listdir(FFMPEG_DIR)[0])  # Папка типа "ffmpeg-master-latest-win64-gpl"
        bin_folder = os.path.join(extracted_folder, "bin")

        # Перемещаем исполняемые файлы в ffmpeg/bin/
        os.makedirs(os.path.join(FFMPEG_DIR, "bin"), exist_ok=True)
        for file in os.listdir(bin_folder):
            shutil.move(os.path.join(bin_folder, file), os.path.join(FFMPEG_DIR, "bin", file))

        # Удаляем временную папку extracted_folder
        shutil.rmtree(extracted_folder, ignore_errors=True)

        print("FFmpeg установлен.")

    # Проверяем, что ffmpeg действительно установился
    if not os.path.exists(FFMPEG_BIN) or not os.path.exists(FFPROBE_BIN):
        print("Ошибка: FFmpeg не был установлен корректно!")
        sys.exit(1)

    # Принудительно указываем pydub, где искать ffmpeg
    AudioSegment.converter = FFMPEG_BIN
    AudioSegment.ffprobe = FFPROBE_BIN

def convert_mp3_to_wav(mp3_path, wav_path):
    """Конвертирует MP3 в WAV."""
    download_and_extract_ffmpeg()
    print(f"Конвертирую {mp3_path} -> {wav_path}")
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

def transcribe_audio(wav_path):
    """Распознаёт речь из WAV-файла, обрабатывая его частями."""
    recognizer = sr.Recognizer()

    with sr.AudioFile(wav_path) as source:
        duration = int(source.DURATION)  # Получаем длительность файла
        print(f"Длительность файла: {duration} секунд")

        full_text = []
        step = 30  # Длина сегмента в секундах
        for i in range(0, duration, step):
            source_audio = recognizer.record(source, duration=step, offset=i)  # Читаем кусок файла
            
            try:
                text = recognizer.recognize_google(source_audio, language='ru-RU')
                full_text.append(text)
                print(f"Фрагмент {i}-{min(i+step, duration)} сек: {text}")
            except sr.UnknownValueError:
                print(f"Фрагмент {i}-{min(i+step, duration)} сек не распознан.")
            except sr.RequestError as e:
                print(f"Ошибка сервиса распознавания: {e}")

    return " ".join(full_text)  # Собираем весь текст

def main():
    if len(sys.argv) < 2:
        print("Использование: main.py path/to/file.mp3 [path/to/save.txt]")
        sys.exit(1)

    mp3_path = os.path.abspath(sys.argv[1])  # Делаем путь абсолютным
    print(f"Открываю файл: {mp3_path}")

    if not os.path.isfile(mp3_path):
        print(f"Ошибка: Файл {mp3_path} не найден!")
        sys.exit(1)

    # Генерация пути к выходному файлу
    default_save_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(default_save_dir, exist_ok=True)

    if len(sys.argv) > 2:
        output_path = os.path.abspath(sys.argv[2])
    else:
        base_name = os.path.splitext(os.path.basename(mp3_path))[0]
        output_path = os.path.join(default_save_dir, f"{base_name}.txt")

    wav_path = os.path.splitext(mp3_path)[0] + ".wav"

    try:
        convert_mp3_to_wav(mp3_path, wav_path)
        text = transcribe_audio(wav_path)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"Текст сохранён в {output_path}")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)

if __name__ == "__main__":
    main()
