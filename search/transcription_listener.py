import whisper
import os
import time
import datetime
import sys
'''
# instructions to get this working
# install python3
# follow install instructions on https://github.com/openai/whisper/blob/main/README.md. Should be as follows:
# 1: install ffmpeg, ensure if this is windows that it is on the computer path by trying to invoke on the command line
# 2: install/confirm install of pip on a windows computer
# 3: run install instructions for whisper. should be: pip install -U openai-whisper

For Gary testing
download the mp3 file at https://tsl.access.preservica.com/uncategorized/IO_0948332a-d79a-4d23-b46d-5b1f76b64914/
save to a folder containing just the recording
invoke script and target the folder using an absolute filepath is possible
it'll take a hot second to load the first time. note the start transcription timestamp and the end timestamp. There'll be no progress bar to advise status as it goes, just when it finishes.
output will be a .srt file
hit ctrl+c to stop/pause
'''

# set single parameter
crawl_this = input("directory to crawl for mp3 files: ")

accept_list = ['mp3', 'MP3', 'mp4', 'MP4', 'wav', 'WAV']
#load the base model
print("loading transcription model")
model = whisper.load_model("medium.en")
print("transcription model loaded")
# start the transcription
flag = False
while flag is False:
    try:
        for dirpath, dirnames, filenames in os.walk(crawl_this):
            for filename in filenames:
                filename_extension = filename.split(".")[-1]
                if filename_extension in accept_list:
                    root_filename = filename[:-4]
                    filename1 = os.path.join(dirpath, filename)
                    transcription_filename = f"{root_filename}.srt"
                    transcription_filename = os.path.join(dirpath, transcription_filename)
                    if not os.path.isfile(transcription_filename):
                        print(f"starting transcription for {filename1} at {time.asctime()}")
                        result = model.transcribe(filename1)
                        print(f"transcription for {filename1} completed at {time.asctime()}")
                        transcription_string = ""
                        for block in result['segments']:
                            start = str(datetime.timedelta(seconds=block['start']))[:-3]
                            end = str(datetime.timedelta(seconds=block['end']))[:-3]
                            if transcription_string == "":
                                start = "00:00:00.000"
                                end = str(datetime.timedelta(seconds=result['segments'][1]['start']))[:-3]
                            while len(start) < 12:
                                start = f"0{start}"
                            while len(end) < 12:
                                end = f"0{end}"
                            transcription_string += str(block['id'] + 1) + "\n"
                            transcription_string += f"{start} --> {end}\n"
                            transcription_string += f" {block['text']}\n\n"
                        with open(transcription_filename, "w") as w:
                            w.write(transcription_string)
                        w.close()
                        print(f"{transcription_filename} created, pausing for 2 minutes for funsies")
                        time.sleep(120)
        print(f"done with this pass on transcription, waiting 5 minutes to check for new recordings, it is {time.asctime()}")
        time.sleep(300)
    except KeyboardInterrupt:
        print("process interrupted by you")
        new_variable = input("resume? y/n: ")
        if new_variable == "y":
            continue
        else:
            sys.exit()