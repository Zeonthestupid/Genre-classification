# For each directory in the spotify songs dir, parse through each song and create 2 sec long audio files (using start and end times, in seconds)
# and give each different Dir a different genre and GID as well as the other ID put with audio files
import csv
import os
from mutagen.mp3 import MP3
import math

def generateCSV(path, fieldnames, chunking, defaultclassid, largepooling):
    for dir_name in os.listdir(path):
        if os.path.isdir(os.path.join(path, dir_name)):
            print(f"Directory: {dir_name}")
            for file_name in os.listdir(os.path.join(path, dir_name)):
                if os.path.isfile(os.path.join(path, dir_name, file_name)):
                    print(f"  File: {file_name}")
                    try:
                        audio = MP3(f"C:\\Users\\micah\\PycharmProjects\\pythonProject9\\SpotifySongs\\mp3_files\\{dir_name}\\{file_name}")
                    except:
                        print(f"Failed to read {dir_name} / {file_name} length, not added to database; corrupted")
                    if chunking == True:
                        try:
                            Maxtimesrun = (math.floor(audio.info.length / 2)) / 2
                            print (Maxtimesrun)
                        except:
                            Maxtimesrun = 1

                    currentrun = 0
                    startlength = -2
                    if chunking == False:
                        Maxtimesrun = 1
                    classid = defaultclassid
                    classification = defaultclassid
                    with open('classes.txt', 'r') as file:
                        for line in file:
                            current_line = line.strip()
                            classificationtest = current_line.split("- ")[1]
                            if classificationtest == dir_name or classificationtest == file_name:
                                classid = int(current_line.split(" - ")[0])
                                classification = classificationtest
                    rawfilename = file_name.split(" -")[0]


                    while Maxtimesrun > currentrun:
                        startlength += 2
                        stoplength = startlength + 2
                        if largepooling == True:
                            try:
                                stoplength = math.floor(audio.info.length)
                            except:
                                print("Could not get stop length, Reverting to default")
                                stoplength = 14
                        #The append code
                        rows = {"Title" : f"{file_name}", "Raw_Title": f"{rawfilename}","start" : f"{startlength}", "end" : f"{stoplength}", "salience" : "1",  "fold" : "5", "ClassID" : f"{classid}","class" : f"{classification}"}


                        with open('SpotifySongs/songs_data.csv', mode='a', newline='', encoding='utf-8') as file:
                            writer = csv.DictWriter(file, fieldnames=fieldnames)
                            writer.writerow(rows)
                        currentrun += 1
def generateCSVvalidation(path, fieldnames, chunking, defaultclassid, largepooling):
    for dir_name in os.listdir(path):
        if os.path.isdir(os.path.join(path, dir_name)):
            print(f"Directory: {dir_name}")
            for file_name in os.listdir(os.path.join(path, dir_name)):
                if os.path.isfile(os.path.join(path, dir_name, file_name)):
                    print(f"  File: {file_name}")
                    try:
                        audio = MP3(f"C:\\Users\\micah\\PycharmProjects\\pythonProject9\\SpotifySongs\\mp3_files\\{dir_name}\\{file_name}")
                    except:
                        print(f"Failed to read {dir_name} / {file_name} length, not added to database; corrupted")
                    if chunking == True:
                        try:
                            Maxtimesrun = math.floor(audio.info.length / 2)
                            print (Maxtimesrun)
                        except:
                            Maxtimesrun = 1

                    currentrun = 0
                    startlength = (math.floor(audio.info.length / 2))
                    if chunking == False:
                        Maxtimesrun = 1
                    classid = defaultclassid
                    classification = defaultclassid
                    with open('classes.txt', 'r') as file:
                        for line in file:
                            current_line = line.strip()
                            classificationtest = current_line.split(" - ")[1]
                            if classificationtest == dir_name or classificationtest == file_name:
                                classid = int(current_line.split(" - ")[0])
                                classification = classificationtest
                    rawfilename = file_name.split(" -")[0]


                    while Maxtimesrun > currentrun:
                        startlength += 2
                        stoplength = startlength + 2
                        if largepooling == True:
                            try:
                                stoplength = math.ceil(audio.info.length)
                            except:
                                print("Could not get stop length, Reverting to default")
                                stoplength = 29
                        #The append code
                        rows = {"Title" : f"{file_name}", "Raw_Title": f"{rawfilename}","start" : f"{startlength}", "end" : f"{stoplength}", "salience" : "1",  "fold" : "5", "ClassID" : f"{classid}","class" : f"{classification}"}


                        with open('SpotifySongs/ref_data.csv', mode='a', newline='', encoding='utf-8') as file:
                            writer = csv.DictWriter(file, fieldnames=fieldnames)
                            writer.writerow(rows)
                        currentrun += 1








if __name__ == "__main__":

    # Parameters
    # -------------
    chunking = False
    largepooling = False
    defaultclassid = None

    # -------------

    fieldnames = ["Title", "Raw_Title", "start", "end", "salience", "fold", "ClassID", "class"]
    with open('SpotifySongs/songs_data.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
    with open('SpotifySongs/ref_data.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
    path = '.\\SpotifySongs\\mp3_files'
    generateCSV(path, fieldnames, chunking, defaultclassid, largepooling)
    generateCSVvalidation(path, fieldnames, chunking, defaultclassid, largepooling)