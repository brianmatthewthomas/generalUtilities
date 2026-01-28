# use this tool to take a data spreadsheet and sort files digitized for the TxDOT project into their appropriate structures
# assumes spreadsheet with the following tabs: General Index, Titles Index, Maps Index
# assumed each tab has the following data columns: txdot_Control_Number1, txdot_Control_Number2, txdot_UID, txdot_District
# will sort files into parent folder for the district, then into control number, based on folder match to txdot_UID
# future development may include metadata export if metadata is missing

import os
import pandas as pd
import PySimpleGUI as SG

my_icon = b'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'



def row_converter(row, columns):
    count = 1
    pictionary = {}
    pictionary['Index'] = row[0]
    for item in columns:
        pictionary[item] = str(row[count])
        count += 1
    return pictionary

def folder_maker(filename):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename), exist_ok=True)

def sorter(preservation_directory, presentation_directory, output_folder, spreadsheet_filename, spreadsheet_tab):
    master_counter = 0
    preservation_dict = {}
    presentation_dict = {}
    for dirpath, dirnames, filenames in os.walk(preservation_directory):
        for filename in filenames:
            master_counter += 1
    for dirpath, dirnames, filenames in os.walk(presentation_directory):
        for filename in filenames:
            master_counter += 1
    for dirpath, dirnames, filenames in os.walk(preservation_directory):
        for filename in filenames:
            my_key = dirpath.split('\\')[-1].split('/')[-1]
            if not my_key in preservation_dict:
                preservation_dict[my_key] = []
            filename = os.path.join(dirpath, filename)
            preservation_dict[my_key].append(filename)
    for dirpath, dirnames, filenames in os.walk(presentation_directory):
        for filename in filenames:
            my_key = dirpath.split('\\')[-1].split('/')[-1]
            if not my_key in presentation_dict:
                presentation_dict[my_key] = []
            filename = os.path.join(dirpath, filename)
            presentation_dict[my_key].append(filename)
    current_counter = 0
    df_counter = 0
    window['-OUTPUT-'].update(f"\nprogress bar data compiled", append=True)
    dataframe = pd.read_excel(spreadsheet_filename, sheet_name=spreadsheet_tab, dtype=object)
    dataframe.fillna("None", inplace=True)
    columns = dataframe.columns
    df_master = len(dataframe)
    for row in dataframe.itertuples():
        pictionary = row_converter(row, columns)
        if pictionary['txdot_UID'] in preservation_dict.keys():
            for item in preservation_dict[pictionary['txdot_UID']]:
                filename = item.split('\\')[-1].split('/')[-1]
                if pictionary['txdot_Control_Number1'] != "None":
                    filename2 = f"{output_folder}/{pictionary['txdot_District']}/{pictionary['txdot_Control_Number1']}/{pictionary['txdot_UID']}/preservation1/{filename}"
                else:
                    filename2 = f"{output_folder}/{pictionary['txdot_District']}/{pictionary['txdot_Control_Number2']}/{pictionary['txdot_UID']}/preservation1/{filename}"
                folder_maker(filename2)
                os.rename(item, filename2)
                window['-OUTPUT-'].update(f"\n{filename} -> {filename2}", append=True)
                current_counter += 1
                window['-Progress-'].update_bar(current_counter, master_counter)
            for item in presentation_dict[pictionary['txdot_UID']]:
                filename = item.split('\\')[-1].split('/')[-1]
                if pictionary['txdot_Control_Number1'] != "None":
                    filename2 = f"{output_folder}/{pictionary['txdot_District']}/{pictionary['txdot_Control_Number1']}/{pictionary['txdot_UID']}/presentation2/{filename}"
                else:
                    filename2 = f"{output_folder}/{pictionary['txdot_District']}/{pictionary['txdot_Control_Number2']}/{pictionary['txdot_UID']}/presentation2/{filename}"
                folder_maker(filename2)
                os.rename(item, filename2)
                window['-OUTPUT-'].update(f"\n{filename} -> {filename2}", append=True)
                current_counter += 1
                window['-Progress-'].update_bar(current_counter, master_counter)
        df_counter += 1
        window['-Progress_spreadsheet-'].update_bar(df_counter, df_master)
SG.theme("DarkGreen5")
layout = [
    [
        SG.Push(),
        SG.Text("TxDOT Metadata Spreadsheet", tooltip="the filename of the excel spreadsheet including filepath, must be an excel spreadsheet"),
        SG.In("", size=(50, 1), visible=True, key="-SPREADSHEET_LOCATION-", tooltip="replace this with the filepath"),
        SG.FileBrowse()
    ],
    [
        SG.Push(),
        SG.Radio("General Index", group_id="sheet_tab", key="-tab_general-", default=True),
        SG.Radio("Titles Index", group_id="sheet_tab", key="-tab_titles-"),
        SG.Radio("Maps Index", group_id="sheet_tab", key="-tab_maps-"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Text("Root folder for putting the files", tooltip="where to put the files. doesn't need to be the district abbreviation"),
        SG.In("", size=(50, 1), visible=True, key="-LOCATION-"),
        SG.FolderBrowse()
    ],
    [
        SG.Push(),
        SG.Text("Root folder for PRESERVATION files", tooltip="this is a completely separate directory from the presentation files. DON'T MIX THIS UP!"),
        SG.In("", size=(50, 1), visible=True, key="-LOCATION_preservation-"),
        SG.FolderBrowse()
    ],
    [
        SG.Push(),
        SG.Text("Root folder for PRESENTATION files", tooltip="this is a completely separate directory from the preservation files. DONT MIX THIS UP!"),
        SG.In("", size=(50, 1), visible=True, key="-LOCATION_presentation-"),
        SG.FolderBrowse(),
    ],
    [
        SG.Button("Close", tooltip="This will close the window, processes in-progress will continue until finished", bind_return_key=True)
    ],
    [
        SG.Push(),
        SG.Button("Execute", tooltip="This will start the program running, will run until it is finished"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Text("Progress by file count"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.ProgressBar(1, orientation="h", size=(50, 20), bar_color="dark green", key="-Progress-", border_width=5, relief="RELIEF_SUNKEN"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.Text("Progress by spreadsheet row"),
        SG.Push()
    ],
    [
        SG.Push(),
        SG.ProgressBar(1, orientation="h", size=(50, 20), bar_color="dark red", key="-Progress_spreadsheet-", border_width=5, relief="RELIEF_SUNKEN"),
        SG.Push()
    ],
    [
        SG.Text("", key="-STATUS-")
    ],
    [
        SG.Push(),
        SG.Multiline(default_text="click on execute to show progress\n-------------", size=(90, 5), auto_refresh=True, key="-OUTPUT-", autoscroll=True, border_width=5, expand_x=True),
        SG.Push()
    ]
]

window = SG.Window("TxDOT file sorter", layout, resizable=True, icon=my_icon)

event, values = window.read()
while True:
    event, value = window.read()
    preservation_directory =  values['-LOCATION_preservation-']
    presentation_directory = values['-LOCATION_presentation-']
    output_folder = values['-LOCATION-']
    spreadsheet_filename = values['-SPREADSHEET_LOCATION-']
    spreadsheet_tab = ""
    if values['-tab_general-'] is True:
        spreadsheet_tab = "General Index"
    if values['-tab_titles-'] is True:
        spreadsheet_tab = "Titles Index"
    if values['-tab_maps-'] is True:
        spreasheet_tab = "Maps Index"
    if event == "Execute":
        window['-OUTPUT-'].update(f"\nstarting routine, getting progress bar information", append=True)
        sorter(preservation_directory=preservation_directory, presentation_directory=presentation_directory, spreadsheet_filename=spreadsheet_filename, spreadsheet_tab=spreadsheet_tab, output_folder=output_folder)
        window['-OUTPUT-'].update(f"\nroutine finished, check for files that didn't get moved. If they exist they probably weren't in the spreadsheet", append=True)
    if event == "Close" or event == SG.WIN_CLOSED:
        break
window.close()