# mp3-to-text

## Описание
Программа для автоматической транскрипции аудиофайлов в текст. Принимает на вход MP3-файл, конвертирует его в WAV и распознаёт речь с использованием Google Speech Recognition.

## Возможности
- Автоматическая загрузка и установка FFmpeg
- Конвертация MP3 в WAV
- Разбиение аудиофайла на части и их обработка
- Распознавание речи с использованием Google Speech Recognition
- Сохранение транскрибированного текста в файл

## Установка
### 1. Установка зависимостей
Перед использованием необходимо установить зависимости:

```sh
pip install -r requirements.txt
```

## Использование
Запуск программы выполняется через командную строку:

```sh
python app.py C:/path/to/audio.mp3 [C:/path/to/output.txt]
```

- `C:/path/to/audio.mp3` — путь к входному MP3-файлу.
- `[C:/path/to/output.txt]` — (необязательно) путь для сохранения распознанного текста.

Если путь к файлу вывода не указан, программа создаст файл в папке `results`.

## Пример работы
```sh
python app.py example.mp3
```
Выходной файл с текстом будет сохранён в `results/example.txt`.

## Возможные ошибки и их решения
### FFmpeg не установлен
Программа автоматически загружает и устанавливает FFmpeg, но если этого не произошло, попробуйте установить его вручную и добавить в переменную среды `PATH`.

### Ошибка запроса к сервису распознавания
- Проверьте подключение к интернету.
- Попробуйте выполнить программу позже, так как сервис Google может временно недоступен.

### Аудиофайл не распознаётся
- Убедитесь, что качество записи хорошее.
- Проверьте, что язык аудиофайла совпадает с указанным в коде (`ru-RU`).

## Лицензия
Этот проект распространяется под лицензией MIT.

