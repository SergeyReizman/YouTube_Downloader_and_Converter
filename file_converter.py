import os
from moviepy.editor import VideoFileClip
from moviepy.config import get_setting

def check_ffmpeg():
    # Check if ffmpeg is installed
    if not get_setting("FFMPEG_BINARY"):
        raise Exception("FFmpeg not found. Please install ffmpeg.")

def convert_to_mp3(input_filename):
    try:
        check_ffmpeg()

        # Check if the file exists
        if not os.path.isfile(input_filename):
            raise FileNotFoundError(f"The file '{input_filename}' does not exist.")

        # Check if the file is a video file based on the extension
        _, file_extension = os.path.splitext(input_filename)
        video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv']
        if file_extension.lower() not in video_extensions:
            raise ValueError(f"Invalid file format. Only video files with extensions {video_extensions} are supported.")

        # Output filename for the MP3 file
        output_filename = os.path.join(os.path.splitext(input_filename)[0] + ".mp3")

        # Perform the conversion
        with VideoFileClip(input_filename) as video_clip:
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(output_filename, codec='libmp3lame', logger=None)

        print(f"Conversion of {input_filename} to MP3 complete! Output saved as {output_filename}")
    except Exception as e:
        print(f"Error during conversion: {e}")

def main():
    input_filename = "input_video.mp4"
    convert_to_mp3(input_filename)

if __name__ == "__main__":
    main()
