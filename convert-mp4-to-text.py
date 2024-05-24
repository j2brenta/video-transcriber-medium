import os
import ffmpeg
import argparse

INPUT_VIDEOS_PATH = 'input-videos'
PROCESSED_PATH = 'processed'
TEXT_PATH = 'text'

def ffmpeg_convert_mp4_to_wav(file_name):
    print("Converting to wav")
    print("Input file: ", file_name)
    filename_without_extension = file_name.split('.')[0]
    print(filename_without_extension)
    ffmpeg = f'ffmpeg -i {INPUT_VIDEOS_PATH}/{filename_without_extension}.mp4 -acodec pcm_s16le -ac 1 -ar 16000 {PROCESSED_PATH}/{filename_without_extension}-processed.wav'
    os.system(ffmpeg)

def ffmpeg_convert_mp4_to_mp3(file_name):
    print("Converting to mp3")
    print("Input file: ", file_name)
    filename_without_extension = file_name.split('.')[0]
    print(filename_without_extension)
    ffmpeg = f'ffmpeg -i {INPUT_VIDEOS_PATH}/{filename_without_extension}.mp4 {PROCESSED_PATH}/{filename_without_extension}-processed.mp3'
    os.system(ffmpeg)

def whisper_transcribe_mp3(file_name, language):
    filename_without_extension = file_name.split('.')[0]
    print(filename_without_extension)

    whisper_command = 'Whisper-mac'
    model_path = '-m ../whisper.cpp/models/ggml-small.bin'
    output_options = f'-l {language} --output-txt --output-file {TEXT_PATH}/{filename_without_extension} {PROCESSED_PATH}/{filename_without_extension}-processed.wav'

    whisper = f'{whisper_command} {model_path} {output_options}'    
    os.system(whisper)


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Convert mp4 to mp3 or to wav and then to text.")

    # Create a mutually exclusive group for the commands
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--transcribe', action='store_true', help='Transcribe the mp3 file to text.')
    group.add_argument('--convert', action='store_true', help='Convert only mp4 file to mp3/wav.')
    group.add_argument('--convert-transcribe', action='store_true', help='Convert the file and transcribe the mp3 file to text.')

    # Add the other arguments
    parser.add_argument('filename', type=str, help='The name of the file to convert')
    parser.add_argument('--mp3', action='store_true', help='Convert mp4 to mp3')
    parser.add_argument('--wav', action='store_true', help='Convert mp4 to wav')
    parser.add_argument('--language', type=str, default='en', help='Language for transcribing')

    # Parse the arguments
    args = parser.parse_args()

    if args.transcribe:
        whisper_transcribe_mp3(args.filename, args.language)
    elif args.convert:
        if args.mp3:
            ffmpeg_convert_mp4_to_mp3(args.filename)
        elif args.wav:
            ffmpeg_convert_mp4_to_wav(args.filename)        
    elif args.convert_transcribe:
        print("Converting and transcribing")
        ffmpeg_convert_mp4_to_wav(args.filename)   
        whisper_transcribe_mp3(args.filename, args.language)   

if __name__ == "__main__":
    main()