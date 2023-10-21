import speech_recognition as sr
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment
import os
from moviepy.editor import TextClip
import moviepy.config as config
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip



config.change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})


# Путь к видеофайлу и путь для сохранения аудио
video_path = r'video_path_to_file'

# Путь для сохранения видео с текстом
output_video_path = 'output_video1.mp4'

# Загружаем видео и извлекаем аудио дорожку
video_clip = VideoFileClip(video_path)
audio_clip = video_clip.audio

# Сохраняем аудио в формате WAV
wav_audio_path = '222.wav'
audio_clip.write_audiofile(wav_audio_path)

# Преобразование аудиофайла в WAV
sound = AudioSegment.from_wav(wav_audio_path)
sound.export("temp.wav", format="wav")

# Инициализация объекта распознавания
recognizer = sr.Recognizer()

# Загрузка аудиофайла для распознавания
audio_data = sr.AudioFile("temp.wav")

# Попытка распознавания речи
with audio_data as source:
    audio = recognizer.record(source)

# Распознавание речи с использованием Google Web Speech API
try:
    text1 = recognizer.recognize_google(audio, language="ru-RU")
    print("Распознанный текст: ", text1)
except sr.UnknownValueError:
    print("Не удалось распознать речь")
except sr.RequestError as e:
    print("Ошибка запроса к Google Web Speech API")

# Сохранение распознанного текста в текстовом файле с указанием кодировки UTF-8
with open("recognized_text.txt", "w", encoding="utf-8") as text_file:
    text_file.write(text1)


# Удаление временных файлов
os.remove("temp.wav")
os.remove(wav_audio_path)



# Разбиваем текст на отдельные слова
text_words = text1.split()

# Создаем пустой текстовый видеоклип
text_clips = []

# Продолжительность отображения каждой группы слов в секундах
duration_per_clip = 1.3

# Время начала отображения первой группы слов
start_time = 0

# Индекс начального слова для каждой группы
start_word_index = 0

# Количество слов в каждой группе
words_per_group = 3

while start_word_index < len(text_words):
    end_word_index = start_word_index + words_per_group
    group_words = ' '.join(text_words[start_word_index:end_word_index])

    text_clip = TextClip(group_words, fontsize=24, color="white", bg_color="black")
    text_clip = text_clip.set_duration(duration_per_clip)
    text_clip = text_clip.set_position(("center", "bottom"))
    text_clip = text_clip.set_start(start_time)
    text_clips.append(text_clip)
    
    start_time += duration_per_clip
    start_word_index = end_word_index

# Загружаем видео
video_clip = VideoFileClip(video_path)

# Создаем видеоклип с текстом
video_with_text = CompositeVideoClip([video_clip] + text_clips)

# Сохраняем видео
video_with_text.write_videofile(output_video_path, codec='libx264')