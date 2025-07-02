from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)
OUTPUT_DIR = "downloads"
FFMPEG_PATH = r'C:\Users\LENOVO\Downloads\ffmpeg-7.1.1-essentials_build\bin'  # ← AJUSTA esta ruta si es necesario

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def descargar_mp3(url):
    FFMPEG_PATH = r'C:\Users\LENOVO\Downloads\ffmpeg-7.1.1-essentials_build\bin'  # ← Ajusta esta ruta si es necesario

    ydl_opts_info = {
        'quiet': True,
        'skip_download': True,
    }

    # 1. Extraer información del video (como título)
    with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
        info = ydl.extract_info(url, download=False)
        titulo = info.get("title", "audio")
        titulo = "".join(c if c.isalnum() or c in " _-" else "_" for c in titulo)  # Sanitiza caracteres
        output_filename = f"{titulo}.mp3"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

    # 2. Descargar y convertir
    ydl_opts_download = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(OUTPUT_DIR, f'{titulo}.%(ext)s'),
        'ffmpeg_location': FFMPEG_PATH,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
        ydl.download([url])

    if os.path.exists(output_path):
        return output_path
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            try:
                mp3_path = descargar_mp3(url)
                if mp3_path:
                    return send_file(mp3_path, as_attachment=True)
                else:
                    return "❌ No se pudo convertir a MP3."
            except Exception as e:
                return f"❌ Error al procesar: {e}"
        else:
            return "❗ Por favor, ingresa un enlace válido."

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
