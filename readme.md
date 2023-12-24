# Speech Recognition Script

This simple Python script utilizes the SpeechRecognition library to transcribe speech from an audio file and appends the transcribed text to a data file.

## Prerequisites

Before running the script, ensure that you have the following prerequisites installed:

- Python (https://www.python.org/)
- SpeechRecognition library (`pip install SpeechRecognition`)

## Usage

1. Save your audio file (in WAV format) to a location on your machine.
2. Update the script with the correct path to your audio file.

    ```python
    with sr.AudioFile("path/to/your/audio/file.wav") as source:
    ```

3. Run the script:

    ```bash
    python main.py
    ```

4. The script will transcribe the speech from the audio file using the Google Speech Recognition API and append the transcribed text to the `data.txt` file.

## Note

Make sure to replace `"path/to/your/audio/file.wav"` with the actual path to your audio file.

## Dependencies

- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)

## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License.