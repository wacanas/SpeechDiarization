#conda install -c conda-forge ffmpeg

#pip install audioread
#pip install sounfile
import os
import librosa
import soundfile as sf
import shutil
from wav_rw import  wavwrite

def convertir_mp3_a_wav(directorio_origen, directorio_destino, duracion_minima=1.0, tasa_muestreo=16000):
    
    
    for ruta_raiz, directorios, archivos in os.walk(directorio_origen):
        for nombre_archivo in archivos:
            if nombre_archivo.endswith('.mp3'):
                ruta_archivo_mp3 = os.path.join(ruta_raiz, nombre_archivo)
                print(f"Cargando {ruta_archivo_mp3} ...")
                
                # Cargar archivo MP3
                audio, sr = librosa.load(ruta_archivo_mp3, sr=None)

                # Verificar la duracion del archivo
                duracion = librosa.get_duration(y=audio, sr=sr)
                if duracion > duracion_minima:
                    print(f"Convertir {nombre_archivo} (duración: {duracion:.2f} s) a WAV ...")
                    
                    # Converter el archivo a la nueva tasa de muestreo
                    audio_resampled = librosa.resample(audio, orig_sr=sr, target_sr=tasa_muestreo)
                    
                    # Generar la nueva ruta de archivo en el directorio destino
                    nombre_base, _ = os.path.splitext(nombre_archivo)
                    dir_base = os.path.join(directorio_destino,ruta_raiz.split(os.sep)[1])
                    
                    if not os.path.exists(dir_base):
                        os.makedirs(dir_base)
        
                    file_wav = nombre_base.replace(" ", "_")
                    nuevo_nombre = f"{file_wav}.wav"
                    
                    ruta_archivo_wav = os.path.join(dir_base, nuevo_nombre)
                    
                    # Guardar el archivo WAV
                    wavwrite(audio_resampled, tasa_muestreo, ruta_archivo_wav)
                    #sf.write(ruta_archivo_wav, audio_resampled, tasa_muestreo)
                    print(f"Guardado: {ruta_archivo_wav}")
                else:
                    print(f"Saltado {nombre_archivo} debido a duración insuficiente ({duracion:.2f} s).")
                
# Especifica los directorios de origen y destino

from glob import glob
import os

directorio_origen = 'incognitus_audios'

root = os.path.join(directorio_origen, "**/*.mp3")
lista_files = glob(root,recursive=True)
lista_paths = glob(directorio_origen+"/*",recursive=True)

directorio_destino = 'wavFiles'

convertir_mp3_a_wav(directorio_origen, directorio_destino)