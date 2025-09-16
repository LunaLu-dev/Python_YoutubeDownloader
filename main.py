import os
import yt_dlp
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

# Ensure a downloads directory exists
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


def download_youtube_audio(url):
    # Configuration for audio-only download
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video information
            info_dict = ydl.extract_info(url, download=True)

            # Get the filename
            filename = ydl.prepare_filename(info_dict)

            # Change extension to mp3
            mp3_filename = filename.rsplit('.', 1)[0] + '.mp3'

            return mp3_filename, info_dict.get('title', 'Unknown Title')

    except Exception as e:
        print(f"Download error: {e}")
        raise


def download_youtube_video(url):
    # Configuration for audio-only download
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video information
            info_dict = ydl.extract_info(url, download=True)

            # Get the filename
            filename = ydl.prepare_filename(info_dict)

            # Change extension to mp3
            mp3_filename = filename.rsplit('.', 1)[0] + '.mp4.'

            return mp3_filename, info_dict.get('title', 'Unknown Title')

    except Exception as e:
        print(f"Download error: {e}")
        raise


@app.route('/', methods=['GET'])
def renter_web_page():
    return render_template('index.html')



@app.route('/audio', methods=['POST'])
def download_audio():
    """Main page for YouTube video downloading."""
    if request.method == 'POST':
        try:
            # Get URL from form
            url = request.form['url']

            # Download audio
            full_path, video_title = download_youtube_audio(url)

            # Return file for download
            return send_file(full_path, as_attachment=True, download_name=os.path.basename(full_path))

        except Exception as e:
            # Log the full error for debugging
            print(f"Full error details: {e}")
            return f"An error occurred: {str(e)}", 400

@app.route('/video', methods=['POST'])
def download_video():
    try:
        # Get URL from form
        url = request.form['url']

        # Download audio
        full_path, video_title = download_youtube_video(url)

        # Return file for download
        return send_file(full_path, as_attachment=True, download_name=os.path.basename(full_path))

    except Exception as e:
        # Log the full error for debugging
        print(f"Full error details: {e}")
        return f"An error occurred: {str(e)}", 400


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)