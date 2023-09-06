import os
import shutil
import zipfile

'''

        Options

'''
#relative link to the folder where your zipped submissions are
zippedSubmissionsFolder = './_ToMark'
#Remove the rtf coversheet files that you forgot to untick.
removeRTFFiles = True
#Limit the amount of files you want to move, good for testing. 0 = off
limitFilesToMove = 0

def create_folder_and_move_file(file_path, destination_folder):
    # Extract the file name from the file path
    file_name = os.path.basename(file_path)
    extension = file_name[-4:] #get the last 4 digits of an extension
    

    if(extension.lower() == ".rtf" and removeRTFFiles == True):
        os.remove(file_path)
        print(f"Deleted {file_path}")
        return

    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Move the file to the destination folder
    destination_path = os.path.join(destination_folder, file_name)
    if(extension.lower() == ".zip"):
        unzip_file(file_path, destination_folder)
    else:
        shutil.move(file_path, destination_path)
    
    print(f"Moved {file_name} to {destination_folder}")

def unzip_file(file_path, destination_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(destination_path)

def path_to_file(file_path):
    return zippedSubmissionsFolder + '/' + file_path

def path_to_destination(studentID):
    return zippedSubmissionsFolder + '/' + studentID

def bulk_move_files():

    counter = 1

    # Get a list of all files in the folder
    files = os.listdir(zippedSubmissionsFolder)

    for file in files:
        #Limit to a number of files to test
        if(limitFilesToMove > 0 and counter > limitFilesToMove):
             continue

        #Get path to current file
        pathToFile = path_to_file(file)

        #Check if it's a folder
        if(os.path.isdir(pathToFile)):
            continue

        #GetStudentID
        studentID = file.split('_')[4][:8]
        #Get Destination folder
        pathToDest = path_to_destination(studentID)

        create_folder_and_move_file(pathToFile, pathToDest)

        counter = counter + 1

bulk_move_files()