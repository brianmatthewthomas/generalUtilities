import whisper
import os
import time
import datetime
import sys
import json
from whisper.utils import get_writer
from pdfme import build_pdf
import torch
'''
# instructions to get this working
# install python3
# follow install instructions on https://github.com/openai/whisper/blob/main/README.md. Should be as follows:
# 1: install ffmpeg, ensure if this is windows that it is on the computer path by trying to invoke on the command line
# 2: install/confirm install of pip on a windows computer
# 3: run install instructions for whisper. should be: pip install -U openai-whisper
# 4: use pip to install pdfme
'''
logfile = "./transcription_log.txt"
# the constant values for pdfme to save space below
#global_header1 = {'.': 'Notes about the transcription', 'style': 'title2', 'outline': {'level': 1, 'text': 'Notes'}}

# commented out standard descriptive extras per request by Steve
global_header1 = {".": "", "style": "title2", "outline": {'level': 1, 'text': 'Notes'}}
global_note2 = {'.': "Note: timed transcription format is \n\tLine 1: Transcribed text sequence in the recording\n\tLine 2:[Section begin] --> [Section end]\n\t\t\tSection begin: 'Hour':'Minute':'Second','millisecond\n\t\t\tSection end: 'Hour':'Minute':'Second','millisecond'\n\tLine 3: Transcribed audio", 'style': 'notes'}
#global_note2 = {'.': ""}
global_note3 = {'.': "Note: If there is a large gap between spoken words or the recording ends before the end of file, the last spoken word(s) will repeat in the transcript.", 'style': 'notes'}
#global_note3 = {'.': ''}
global_note4 = {'.': "Note: Transcription completed using automated means with tools designed for video captions. Speakers are not labeled or differentiated in this transcript. It is intended to assist users in locating a portion of the recording of interest to their research and is not part of the records. The accuracy of the transcript has not been verified, users should refer to the actual recording to confirm spoken content.", 'style': 'notes'}
#global_note4 = {'.': ''}
global_header2 = {'.': 'Transcript', 'style': 'title2', 'outline': {'level': 1, 'text': 'Transcript'}}
#global_header2 = {'.': '', 'style': 'title2', 'outline': {'level': 1, 'text': 'Transcript'}}
pdf_style = {'margin_bottom': 8, 'text-align': 'j'}
pdf_formats = {'title': {'b': 1, 's': 13, 'text_align': 'c'}, 'title2': {'b': 2, 's': 13, 'text_align': 'l'}, 'notes': {'s': 10, 'text_align': 'l', 'margin_left': 20}}
document_header = {'x': 'left', 'y': 20, 'height': 'top', 'style': {'text_align': 'r'}, 'content': [{'.b': 'Transcript'}]}
document_footer = {'x': 'left', 'y': 800, 'height': 'bottom', 'style': {'text_align': 'r'}, 'content': [{'.': ['Page ', {'var': '$page'}]}]}
document_perPage = [{'pages': '1:1000:2', 'style': {'margin': [60, 100, 60, 60]}},
{'pages': '0:1000:2', 'style': {'margin': [60, 60, 60, 100]}},
{'pages': '0:4:2', 'running_sections': {'include': ['header', 'footer']}}]


# set single parameter
crawl_this = input("directory to crawl for mp3 files: ")
while crawl_this.startswith("'") or crawl_this.startswith('"'):
    crawl_this = crawl_this[1:]
while crawl_this.endswith("'") or crawl_this.endswith('"'):
    crawl_this = crawl_this[:-1]

accept_list = ['m4v', 'mp3', 'MP3', 'mp4', 'MP4', 'wav', 'WAV', 'mov', 'MOV', 'avi', 'AVI', 'wma', 'WMA', 'mts', 'MTS', 'wmv', 'WMV']

device = 'cuda' if torch.cuda.is_available() else 'cpu'
# model to work off of, use medium.en as the default, small has accuracy problems
model_type = "medium.en" #large-v2 #turbo #large-v3
print(f"device type {device} is best available")
if device == "cuda":
    try:
        print("testing GPU configuration, will revert to CPU if GPU functionality is insufficient")
        model = whisper.load_model(model_type).to(device)
        print("transcription model loaded")
    except:
        print(f"model {model_type} too large for GPU, switching to CPU")
        device = "cpu"
#load the base model
print("loading transcription model")
if device == "cuda":
    model = whisper.load_model(model_type).to(device)
if device == "cpu":
    model = whisper.load_model(model_type, device=device)
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
                        time_start = time.time()
                        #audio = whisper.load_audio(filename1)
                        #audio = whisper.pad_or_trim(audio)
                        #mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)
                        #_, probs = model.detect_language(mel)
                        #print(f"Detected language: {max(probs, key=probs.get)}")
                        #options = whisper.DecodingOptions()
                        #print("decoding options loaded, running")
                        #result = whisper.decode(model, mel, options)
                        result = model.transcribe(filename1, fp16=False, verbose=None)
                        time_end = time.time()
                        print(f"transcription for {filename1} completed at {time.asctime()} in {str(datetime.timedelta(seconds=time_end-time_start))} minutes")
                        srt_writer = get_writer('srt', dirpath)
                        srt_writer(result, filename1)
                        '''
                        # original manual creation of srt file
                        transcription_string = ""
                        for block in result['segments']:
                            start = str(datetime.timedelta(seconds=block['start']))
                            end = str(datetime.timedelta(seconds=block['end']))
                            if "." not in start:
                                start = f"{start}.000000"
                            if "." not in end:
                                end = f"{end}.000000"
                            if transcription_string == "":
                                start = "00:00:00.000000"
                                end = str(datetime.timedelta(seconds=result['segments'][1]['start']))
                                if "." not in end:
                                    end = f"{end}.000000"
                            start = start[:-3]
                            end = end[:-3]
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
                        #to troubleshoot faulty output, create companion json file
                        with open(f"{transcription_filename}.json", "w") as w:
                            json.dump(result, w)
                        w.close()
                        '''
                        try:
                            # prep character list in case of failure
                            character_set = []
                            character_set = set()
                            # now try to generate a pdf version for audio sidecars
                            pdf_name = f"{filename1[:-3]}pdf"
                            #clear last instance of the pdf constructor to start fresh
                            # the pdf variables and header text
                            document = "something"
                            document = {}
                            document['style'] = pdf_style
                            document['formats'] = pdf_formats
                            document['running_sections'] = {'header': document_header, 'footer': document_footer}
                            document['sections'] = []
                            section1 = {}
                            document['sections'].append(section1)
                            section1['running_sections'] = ['footer']
                            section1['content'] = content1 = []
                            #content1.append({'.': f'Transcript for recording {root_filename}', 'style': 'title', 'outline': {'level': 1, 'text': 'Title'}})
                            content1.append(global_header1)
                            content1.append(global_note2)
                            content1.append(global_note3)
                            content1.append(global_note4)
                            content1.append(global_header2)
                            # print list of characters to special file to help flag problems for correction
                            character_set_text = ""
                            # the transcript to be put into the pdf
                            with open(f"{filename1[:-3]}srt", 'r', encoding='utf-8') as f:
                                for line in f:
                                    content1.append(line[:-1])
                                    # generating set of characters for if this fails
                                    for character in line:
                                        character_set.add(character)
                            character_set = list(character_set)
                            character_set.sort()
                            for character in character_set:
                                character_set_text = f"{character_set_text}{character}\n"
                            with open(f"{filename1[:-4]}_characters.txt", "w") as w:
                                w.write(character_set_text)
                            w.close()
                            # write the transcript
                            with open(pdf_name, 'wb') as w:
                                build_pdf(document, w)
                            w.close()
                            # if saving the pdf works, remove the character list file as unnecessary
                            os.remove(f"{filename1[:-4]}_characters.txt")
                        except:
                            try:
                                with open(logfile, "a") as w:
                                    w.write(f"saving transcription failed for {filename1} at {time.asctime()} in {str(datetime.timedelta(seconds=time_end-time_start))} minutes\n")
                                w.close()
                            except:
                                continue
                        try:
                            with open(logfile, "a") as w:
                                w.write(f"transcription for {filename1} completed at {time.asctime()} in {str(datetime.timedelta(seconds=time_end-time_start))} minutes\n")
                            w.close()
                        except:
                            continue
                        print(f"{transcription_filename} created, pausing for 30 seconds to prevent system overloading")
                        time.sleep(60)
        print(f"done with this pass on transcription, waiting 5 minutes to check for new recordings, it is {time.asctime()}")
        time.sleep(300)
    except KeyboardInterrupt:
        print("process interrupted by you")
        new_variable = input("resume? y/n: ")
        if new_variable == "y":
            continue
        else:
            sys.exit()
