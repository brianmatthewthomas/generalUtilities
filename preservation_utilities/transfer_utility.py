import hashlib
import os
import csv
import datetime
import PySimpleGUI as SG

logo = b'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'

def create_sha256(filename):
    sha256 = hashlib.sha256()
    blocksize = 65536
    with open(filename, 'rb') as f:
        buffer = f.read(blocksize)
        while len(buffer) > 0:
            sha256.update(buffer)
            buffer = f.read(blocksize)
    fixity = sha256.hexdigest()
    return fixity

def get_time(filename):
    timer = os.path.getmtime(filename)
    datestamp = str(datetime.datetime.fromtimestamp(timer))
    datestamp = datestamp.split(" ")[0]
    return datestamp

def get_size(my_number):
    master_default = f"{str(my_number)} Bytes"
    if 1024 <= my_number < 1048576:
        my_math = str(my_number/1024)
        if "." in my_math:
            my_math = f"{my_math.split('.')[0]}.{my_math.split('.')[1][:2]}"
        master_default = f"{my_math} KB"
    if 1048576 <= my_number < 1073741824:
        my_math = str(my_number/1048576)
        if "." in my_math:
            my_math = f"{my_math.split('.')[0]}.{my_math.split('.')[1][:2]}"
        master_default = f"{my_math} MB"
    if 1073741824 <= my_number < 1099511627776:
        my_math = str(my_number/1073741824)
        if "." in my_math:
            my_math = f"{my_math.split('.')[0]}.{my_math.split('.')[1][:2]}"
        master_default = f"{my_math} GB"
    if my_number >= 1099511627776:
        my_math = str(my_number/1099511627776)
        if "." in my_math:
            my_math = f"{my_math.split('.')[0]}.{my_math.split('.')[1][:2]}"
        master_default = f"{my_math} TB"
    return master_default


SG.theme("DarkGreen5")
layout = [
    [
        SG.Checkbox("Include files in inventory spreadsheet", key="-FILES_FLAG-",
                    tooltip="Check to include file level information in the output spreadsheet inventory"),
    ],
    [
        SG.Push(),
        SG.Text("Parent directory", key="-PARENT_Text-"),
        SG.In("", size=(75, 1), key="-PARENT-", tooltip="top-most folder/directory to start from"),
        SG.FolderBrowse()
    ],
    [
        SG.Push(),
        SG.Button("Start", tooltip="This will start the program running"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.ProgressBar(1, orientation="h", size=(83, 20), bar_color="dark green", key="-Progress-", border_width=5,
                       relief="RELIEF_SUNKEN"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Multiline(default_text="Click start to start process, it may be necessary to press start twice\nuse transfer_helper.csv file to populate for six "
                                  "columns of transfer form E-records Inventory tab\ninclude checksum.exf file in "
                                  "the transfer\n\n",
                     size=(115, 10), auto_refresh=True, reroute_stdout=False, key="-OUTPUT-", autoscroll=True, border_width=5),
        SG.Push()
    ],
    [
        SG.Button("Close",
                  tooltip="Close this window. Other processes you started must be finished before this button "
                          "will do anything.", bind_return_key=True)
    ],
]

window = SG.Window("TSLAC electronic records transfer preparation tool",
                   layout,
                   icon=logo,
                   button_color="dark green")

event, values = window.read()
while True:
    event, values = window.read()
    if event == "Start":
        file_flag = values['-FILES_FLAG-']
        my_directory = values['-PARENT-']
        # create checksum file
        checksum_file = "checksum.exf"
        if os.path.isfile(checksum_file):
            os.remove(checksum_file)
        checksums = open(checksum_file, "a")
        # set up csv file
        my_csv = open("transfer_helper.csv", 'w', newline='')
        csv_writer = csv.writer(my_csv, delimiter=",", quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["Copy lines 3 through to the bottom into the first 6 columns of the transfer spreadsheet E-records Inventory tab"])
        csv_writer.writerow(["Grand total information for the PDF transfer form is at the bottom of this spreadsheet"])
        csv_writer.writerow(["Volume", "filecount", "formats", "file/folder title", "begin_date", "end_date"])
        directory_list = set()
        window['-OUTPUT-'].update("Creating list of folders to work with\n", append=True)
        # compile folder list
        for dirpath, dirnames, filenames in os.walk(my_directory):
            for filename in filenames:
                directory_list.add(dirpath)
        directory_list = list(directory_list)
        directory_list.sort()
        window['-OUTPUT-'].update("Generating progress bar information\n", append=True)
        big_count = 0
        current_count = 0
        for dirpath, dirnames, filenames in os.walk(my_directory):
            for filename in filenames:
                big_count += 1
        # start working in folders
        overall_volume = 0
        overall_filecount = 0
        overall_extensions = set()
        overall_begin_date = ""
        overall_end_date = ""
        for this_dir in directory_list:
            window['-OUTPUT-'].update(f"Working on {this_dir}\n", append=True)
            master_size = 0
            master_start = ""
            master_end = ""
            format_set = set()
            files = [q for q in os.listdir(this_dir) if os.path.isfile(f"{this_dir}/{q}")]
            count = len(files)
            overall_filecount = overall_filecount + count
            files_list = []
            files.sort()
            for file in files:
                file = os.path.join(this_dir, file)
                file_checksum = create_sha256(file)
                file_minus_dir = file.replace(my_directory, "")
                file_minus_dir = file_minus_dir[1:]
                checksums.write(f"{file_checksum} ?SHA256*{file_minus_dir}\n")
                file_timestamp = get_time(file)
                if master_start == "":
                    master_start = file_timestamp
                if master_end == "":
                    master_end = file_timestamp
                if overall_begin_date == "":
                    overall_begin_date = file_timestamp
                if overall_end_date == "":
                    overall_end_date = file_timestamp
                if master_end < file_timestamp:
                    master_end = file_timestamp
                if overall_end_date < file_timestamp:
                    overall_end_date = file_timestamp
                if master_start > file_timestamp:
                    master_start = file_timestamp
                if overall_begin_date > file_timestamp:
                    overall_begin_date = file_timestamp
                filesize = os.path.getsize(file)
                master_size = master_size + filesize
                overall_volume = overall_volume + filesize
                my_format = file.split(".")[-1]
                format_set.add(my_format)
                overall_extensions.add(my_format)
                files_list.append([get_size(filesize), "1", my_format, file, file_timestamp, file_timestamp])
                current_count += 1
                window['-Progress-'].update_bar(current_count, big_count)
            format_set = list(format_set)
            format_set.sort()
            format_string = ""
            for item in format_set:
                format_string = f"{format_string}/{item}"
            format_string = format_string[1:]
            csv_writer.writerow([get_size(master_size), str(count), format_string, this_dir, master_start, master_end])
            window['-OUTPUT-'].update(f"Processed {this_dir}\n", append=True)
            print(f"processed {this_dir}")
            if file_flag is True:
                for item in files_list:
                    window['-OUTPUT-'].update(f"Processed {item[3]}\n", append=True)
                    print(f"processed {item[3]}")
                    csv_writer.writerow(item)
        overall_extensions = list(overall_extensions)
        overall_extensions.sort()
        overall_extensions_string = ""
        for item in overall_extensions:
            overall_extensions_string = f"{overall_extensions_string}/{item}"
        overall_extensions_string = overall_extensions_string[1:]
        csv_writer.writerow([get_size(overall_volume), str(overall_filecount), overall_extensions_string, "Totals",  overall_begin_date, overall_end_date])
        window['-OUTPUT-'].update("Finishing up process\n", append=True)
        my_csv.close()
        checksums.close()
        window['-OUTPUT-'].update("All done, remember to open transfer_helper.csv in a spreadsheet program and copy into the first 6 columns of Archival-Transfer-Inventory.xlsx spreadsheet\n", append=True)
        print("all done")
    if event == "Close" or event == SG.WIN_CLOSED:
        break
