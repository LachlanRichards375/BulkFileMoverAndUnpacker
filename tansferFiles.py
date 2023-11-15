import os
import shutil
import zipfile
import xml.etree.ElementTree as ET

'''

		Options

'''
#relative link to the folder where your zipped submissions are
zippedSubmissionsFolder = './DDWT/Exam'
#Remove the rtf coversheet files that you forgot to untick.
removeRTFFiles = True
#Limit the amount of files you want to move, good for testing. 0 = off
limitFilesToMove = 0

'''

		DDWT Options

'''
#Modify connection string for DDWT
new_connection_string = "Data Source=(LocalDB)\MSSQLLocalDB;Initial Catalog=MoviesDB;Integrated Security=True"
#Expected Folder Name
expected_folder_name = "DDWTMovies"

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
	DDWT_cleanup(destination_folder)

def DDWT_cleanup(folder_path):
	attemptCount = 0
	AppData = folder_path

	logs = []
	logs.append("Pre: {AppData}: AppData in folder?({not os.path.exists(AppData + '/App_Data')}), appData exists:{os.path.exists(AppData)}")

	while(not os.path.exists(AppData + "/App_Data") and os.path.exists(AppData) and attemptCount < 3):
		AppData += "/" + expected_folder_name
		attemptCount+=1
		logs.append(f"In Loop: {AppData}:{not os.path.exists(AppData + '/App_Data')}, appData exists:{os.path.exists(AppData)}")

	logs.append(f"Post: {AppData}: AppData exists?{os.path.exists(AppData)}")

	AppData += "/App_data"

	if(not os.path.exists(AppData)):
		print(f"ERROR: Unable to find App_Data folder for {folder_path}")
		for log in logs:
			print(f"{log}")
		return
	   
	if(os.path.exists(AppData + "/MoviesDB.mdf")):
		os.remove(AppData + "/MoviesDB.mdf")

	if(os.path.exists((AppData + "/MoviesDB_log.ldf"))):
		os.remove(AppData + "/MoviesDB_log.ldf")
		
	if(os.path.exists((AppData + "/SQLQuery MoviesDB.sql"))):
		os.remove(AppData + "/SQLQuery MoviesDB.sql")

	#Replace Connection String
	WebConfigFile = AppData + "/../Web.config"
	if(os.path.exists(WebConfigFile)):
		modify_connection_string(WebConfigFile, new_connection_string)
	else:
		print(f"UNABLE to clean {WebConfigFile}")

def modify_connection_string(xml_file, new_connection_string):
	tree = ET.parse(xml_file)
	root = tree.getroot()

	# Find the connection string element
	connection_string_elem = root.find(".//add[@name='MoviesDB']")

	# Modify the connection string attribute
	if connection_string_elem is not None:
		connection_string_elem.set("connectionString", new_connection_string)
		tree.write(xml_file)
		print("Connection string modified successfully.")
	else:
		print("Connection string not found in the XML file.")

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
