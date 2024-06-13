from pytube import YouTube
from pydub import AudioSegment
import os

def descargar_video(url, solo_audio=False):
    yt = YouTube(url)
    if solo_audio:
        stream = yt.streams.filter(only_audio=True).first()
    else:
        stream = yt.streams.get_highest_resolution()
    
    output_path = os.path.join(os.path.dirname(__file__), 'descargas')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    downloaded_file = stream.download(output_path=output_path)
    print(f'Descargado: {yt.title}')
    
    if solo_audio:
        convertir_a_mp3(downloaded_file)

def convertir_a_mp3(file_path):
    mp4_audio = AudioSegment.from_file(file_path, format="mp4")
    mp3_path = file_path.replace(".mp4", ".mp3")
    mp4_audio.export(mp3_path, format="mp3")
    os.remove(file_path)
    print(f'Convertido a mp3: {mp3_path}')

def leer_enlaces(file_path):
    with open(file_path, 'r') as file:
        enlaces = file.readlines()
    return [enlace.strip() for enlace in enlaces]

def main():
    file_path = os.path.join(os.path.dirname(__file__), 'enlaces.txt')
    enlaces = leer_enlaces(file_path)
    
    opcion = input("¿Quieres descargar solo el audio? (s/n): ").strip().lower()
    solo_audio = opcion == 's'
    
    for enlace in enlaces:
        try:
            descargar_video(enlace, solo_audio)
        except Exception as e:
            print(f'Error al descargar {enlace}: {e}')

if __name__ == "__main__":
    main()
