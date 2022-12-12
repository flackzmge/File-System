#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 21:27:51 2021

@author: nathangilbert
"""
# File System

# 1) File Class(everything is a file)  
# PlainFile Class(plain file has a name) 
# Directory Class(name and a list of files)
# constructors (i.e. __init__ methods),

# 2) Add methods that print (recursively) the entire file system tree 
#define appropriate __str__ methods

# 3) Implement a method chown(new_owner)
# allow you to modify the owner of a file or directory.
# If not indicated, the owner will be set to “default”.

# 4 Implement a method ls() that recursively prints the contents of the:
# directory and all the subdirectories
# using indentation to represent how deep in the tree structure the file/directory is

# 5 ...

class PlainFile:
	def __init__(self,filename,owner = "default"): #Constructor with 2 paramaters
		self.filename = filename # creating prtoperty of filename
		self.owner = owner
		self.permissions = ["-","-","-","-","-","-","-","-","-","-"]

	def chown (self,new_owner):
		self.owner = new_owner	# using self.owner property and massing in parameter new_owner		
		
		
class Directory: 
	def __init__(self,foldername,filelist,owner = "default"): # 3 parameters
		self.directoryName = foldername
		self.filelist = filelist
		self.owner = owner
		self.parent = self
		self.permissions = ["d","-","-","-","-","-","-","-","-","-"]
		
	def getDirectoryContents(self,arg): # method that passes through an argument root
		# __str__ method automatically call 
		directoryString = "Directory(" + arg.directoryName + "," # adds Directory name as a string initially root
		for x in range(len(arg.filelist)): # loop for every item on filelist
			if isinstance(arg.filelist[x],Directory): # if the instance is a directory
				directoryString = directoryString + self.getDirectoryContents(arg.filelist[x]) # Add "Directory(" plus the name of the Directory
			else:
				directoryString = directoryString + "PlainFile(" + arg.filelist[x].filename + ")" # if not a directory then add a plainfile in the directory 
				if x < len(arg.filelist)-17:
					directoryString = directoryString + ","
		directoryString = directoryString + ")" # a ) to let us know we are at the end of a directory
		return directoryString 
		
	def chown (self,new_owner):
		self.owner = new_owner 
		"""Every PlainFile method has a property called owner 
		chown method has a parameter called new_owner 
		Is used to change the owner of the PlainFile object """
	
	def printls (self,arg,indent):
		if indent == 0: # 0 automatically passed in by ls method
			print (arg.directoryName) 
			indent = indent + 5 # if there is no indentation then print name of Directory (root) and indent by 5 spaces
		
		for x in range(len(arg.filelist)): # for every file in the filelist
			if isinstance(arg.filelist[x],Directory): # if the instance is a directory
				print(" " * indent, end="") #indent by the current amount in indent end ="" does not print new line after print
				print (arg.filelist[x].directoryName) # Print directory name
				self.printls(arg.filelist[x],indent + 5) # recursive call to printls and pass that directory into printls then indent by 5 
			else:
				print(" " * indent, end="")
				print (arg.filelist[x].filename) # if not a directory then indent by amount in indent and printfile

	def ls (self):
		self.printls(self,0) 
								
	 		
	def __str__(self):
		return self.getDirectoryContents(self)
	
	
		

class FileSystem:
	def __init__(self,currentDirectory): # initialise filesystem and pass in 1 parameter
		self.currentDirectory = currentDirectory
		self.root = currentDirectory
		
	def pwd (self):
		print (self.currentDirectory.directoryName) #print directory name in the current directory 

	def printFilePermissions (self,permissions):
		for x in range(len(permissions)):
			print(permissions[x], end="") 
		print("    ", end="")


	def ls (self,option = ""):		
		for x in range(len(self.currentDirectory.filelist)): #for all the files in filename
			if isinstance(self.currentDirectory.filelist[x],Directory): # if instance is a directory
				if option == "-l": # and if -l 
					self.printFilePermissions(self.currentDirectory.filelist[x].permissions) # passes permissions of directory to printFilepermissions method 
				print (self.currentDirectory.filelist[x].directoryName) # print directory
			else:
				if option == "-l": 
					self.printFilePermissions(self.currentDirectory.filelist[x].permissions) # if not directory then it is a file passes permissions of file to printFilepermissions method 
				print (self.currentDirectory.filelist[x].filename) # print file



			
	def getDirectory (self,directoryName,directory):
		if directory.directoryName == directoryName: 
			return directory # if directory name is equal to the directory that we requested the return that directory
		returnDirectory = None # return none if cant get directory
		for x in range(len(directory.filelist)): # for every file in the directory
			if isinstance(directory.filelist[x],Directory): #if the instance is a directory
				if directory.filelist[x].directoryName == directoryName: # and if the directory name requested is equal the directory name in the filelist
					returnDirectory = directory.filelist[x] # the directory to be returned is the Directory selected 
					break
				else:
					returnDirectory = self.getDirectory (directoryName,directory.filelist[x]) # recursion to repeat search
					if returnDirectory != None:
						break
		return returnDirectory


	def cd (self,newCurrentDirectory):
		found = False # directory not found yet
		if newCurrentDirectory == "..": # if directory selected is ..
			found = True # directory is found
			self.currentDirectory = self.currentDirectory.parent # point the current directory to the parent directory - this is set when mkdir command is run
		else:
			found = False # Directory not found yet		
			for x in range(len(self.currentDirectory.filelist)):# for all the files in filelist
				if isinstance(self.currentDirectory.filelist[x],Directory): # if it is a directory
					if self.currentDirectory.filelist[x].directoryName == newCurrentDirectory: # and if the Directories you request matches one of the Directories in the current directory
						found = True # then we have found the directory
						self.currentDirectory = self.currentDirectory.filelist[x] # the directory we are in is now the directory we selected
						break			
		if found == False:
				print ("The directory does not exist!") # if directory not found then print error message
				
				
				
	
				
	
	def mkdir(self,name,owner ="default"): # 2 parameter with one being optional
		if owner != "default":
			ownerDirectory = self.getDirectory (owner,self.root)
			if ownerDirectory == None: # if couldnt find a directory
				ownerDirectory = self.currentDirectory #Then the owner of directory is the current directory
			found = self.does_file_exist (name,ownerDirectory) # searches to see if Directory exists
			if found == True: 
				print ("Directory already exists") # if directory exists then display a message
				return False
			else:
				newDirectory = Directory(name,[]) # if no directory is found a new directory named after what you put in mkdir and an empty list is created
				newDirectory.chown (ownerDirectory.directoryName) # owner of the directory is now the same as the owner of the old one
				ownerDirectory.filelist.append(newDirectory) # Add new directory to the filelist
				newDirectory.parent = ownerDirectory # the directory it was created in becomes the parent
			
												
		else: # if no owner specified 
			found = self.does_file_exist (name,self.currentDirectory) # searches to see if Directory exists
			if found == True:
				print ("Directory already exists") # if directory exists then display a message
				return False
			else:
				newDirectory = Directory(name,[]) # if no directory is found a new directory named after what you put in mkdir and an empty list is created
				newDirectory.chown (self.currentDirectory.directoryName) # owner of the directory is now the same as the owner of the old one ("Default")
				self.currentDirectory.filelist.append(newDirectory)  # Add new directory to the filelist
				newDirectory.parent = self.currentDirectory  # the directory it was created in becomes the parent				


		 
	

	def does_file_exist (self,name,directory):
		found = False # file not found		
		for x in range(len(directory.filelist)): # for all the files in the file list
			if isinstance(directory.filelist[x],PlainFile): # if the instance is a file
				if directory.filelist[x].filename == name:
					found = True # and the filename is the file we selected then file exists
					break
			else:
				if directory.filelist[x].directoryName == name:
					found = True # then it must a directory and this directory exists
					break					
		return found 	
													
		
	def create_file(self,name):
		found = self.does_file_exist (name,self.currentDirectory)# passes name as a parameter to does file exist		
		if found == False: # if file does not exist
			newFile = PlainFile(name) # ew file equals the name of the file we entered
			newFile.owner = self.currentDirectory.directoryName # owner of file will be the name of the current directory
			self.currentDirectory.filelist.append(newFile) # add new file to file list in the current directory using python append method
		else:
			print("This File already exists") # if file found print that it already exists 

	def rm (self,name): # parameter name of file we want to remove
		found = False	# file not found	
		for x in range(len(self.currentDirectory.filelist)): # for all the files in the directory
			if isinstance(self.currentDirectory.filelist[x],PlainFile): # if the instance is a Plainfile
				if self.currentDirectory.filelist[x].filename == name: # if the name of the file is equal to the one we are searching for
					self.currentDirectory.filelist.remove(self.currentDirectory.filelist[x]) # then remove file using python remove method
					found = True # file found
					break
			else: # if not a plain file then is a directory
				if self.currentDirectory.filelist[x].directoryName == name:
					if len(self.currentDirectory.filelist[x].filelist) > 0:
						print ("Sorry, the directory is not empty") # if there are items in the directory then cannot remove and print message
					else:
						self.currentDirectory.filelist.remove(self.currentDirectory.filelist[x])
						found = True # else remove directory
						break
			
		if found == False:
			print ("File not found") # if found == fale, file is not found and print message


	def findFile (self,filename,searchDirectory,path):
		found = False # file not found yet
		if searchDirectory.directoryName != "root": # when not looking for root
			directoryPath = path + "/" + searchDirectory.directoryName # directory path = root/directoryname
		else:
			directoryPath = searchDirectory.directoryName 
		for x in range(len(searchDirectory.filelist)): # for list of files in filelist
			if isinstance(searchDirectory.filelist[x],Directory): # if the instace is a directory
				
				if searchDirectory.filelist[x].directoryName == filename: # and if the name of the directory is equal to the file name requested
					found = True # Directory has been found
					print (directoryPath + "/" + searchDirectory.filelist[x].directoryName) # print the path taken then a / then the directory we were finding
					break
				else:
					found = self.findFile(filename,searchDirectory.filelist[x],directoryPath) # recursion to repeat method
			else:
				if searchDirectory.filelist[x].filename == filename:
					found = True # file ound
					print (directoryPath + "/"+ searchDirectory.filelist[x].filename ) # print the path taken then a / then the file we were finding
					break							
		return found			


	def find (self,filename):
		rtn = self.findFile (filename,self.root,self.root.directoryName) # passing parameters into findFile
		if rtn == False:
			print ("False") # file name not found print false
			


	def getPermissionUpdatePositionList (self,reference,mode):
		# position 0 either d for directory or -
		if reference == "u": # user 
			if mode == "r":
				return [1] # set user to readable
			if mode == "w":
				return [2] # set user to writable				
			if mode == "x":
				return [3]# set user to executable				
		if reference == "g": # group
			if mode == "r":
				return [4] # set group to readable
			if mode == "w":
				return [5] # set group to writable				
			if mode == "x":
				return [6] # set group to executable
		if reference == "o": # other
			if mode == "r":
				return [7] # set other to readable
			if mode == "w":
				return [8] # set other to writable				
			if mode == "x":
				return [9] # set other to executable
		if reference == "a": # if reference is all of them
			if mode == "r": 
				return [1,4,7] # set u,g & o to readable
			if mode == "w":
				return [2,5,8]	# set u,g & o to writable			
			if mode == "x":
				return [3,6,9] # set u,g & o to executable


	def updatePermissionsList (self,permissions,positionList,mode):
		for x in range(len(positionList)):
			permissions[positionList[x]] = mode



	def chmod (self,name,operation):
		found = False # file not found yet
		fileObject = None # file not found yet
		for x in range(len(self.currentDirectory.filelist)): # for every file in the file list
			if isinstance(self.currentDirectory.filelist[x],PlainFile): # if the instance is a Plainfile
				if self.currentDirectory.filelist[x].filename == name: # if filename is equal to the name passed through
					fileObject = self.currentDirectory.filelist[x] # file object will point to that file
					break 
			else:
				if self.currentDirectory.filelist[x].directoryName == name: # else it could be a directory
					fileObject = self.currentDirectory.filelist[x] #fileobject will point to that directory
					break					
		if fileObject == None:
			print ("file not found") # if file not found then print message
		else: # if file found
			reference = [] # set a variable called reference as a list
			mode = [] # print the path taken then a / then the directory we were finding
			for x in range(len(operation)): # pass in operation from the parameter
				if operation[x] == "-" or operation[x] == "+" or operation[x] == "=":
					operator = operation[x] # if operation equal to +,- or = then it set the operator as that 
				elif operation[x] == "u" or operation[x] == "o" or operation[x] == "g" or operation[x] == "a": # if operation is equal to u,g or o t
					reference.append(operation[x])  # then add this to the reference list
				else:
					mode.append(operation[x]) # else if not a reference or a operator it is a mode add to mode list
			for x in range(len(reference)):
				if operator == "+":
					positionList = self.getPermissionUpdatePositionList(reference[x],mode[0])
					self.updatePermissionsList(fileObject.permissions,positionList,mode[0]) # will add the mode string to position in reference
				elif operator == "-":
					positionList = self.getPermissionUpdatePositionList(reference[x],mode[0])
					self.updatePermissionsList(fileObject.permissions,positionList,"-") # will take a way mode string in position of reference and replace it with -
				else:
					for y in range(len(mode)):
						positionList = self.getPermissionUpdatePositionList(reference[x],mode[y])
						self.updatePermissionsList(fileObject.permissions,positionList,mode[y])
						#updatePermissionsList - sets the position string to ModeSo if mode == r then it will print r 

						
					
					

			
'''f1 = PlainFile("test.tx")
d1 = Directory("root",[PlainFile("test.txt"),PlainFile("test2.txt")])'''


#Question 1 
print('Question 1')
root = Directory("root",[PlainFile("boot.exe"),
               Directory("home",[
                   Directory("thor",
                      [PlainFile("hunde.jpg"),
                       PlainFile("quatsch.txt")]),
                   Directory("isaac",
                      [PlainFile("gatos.jpg")])])])

'''Creates an object called root which passes a root parameter into the directory then adds a a boot.exe Plainfile to the file list and so on '''
                      



#Question 2
print()
print('Question 2')
print(root)
#getDirectoryContents
''' '''
print()
#Question 3
print('Question 3')

file = PlainFile("boot.exe")
folder = Directory("Downloads",[])
print(f'file.owner: {file.owner}; folder: {folder.owner}')
file.chown("root")
folder.chown("isaac")
print(f'file.owner: {file.owner}; folder: {folder.owner}')


#Question 4
print('Question 4')
root.ls()




#Question 5 (a)
print('Question 5a')

fs = FileSystem (root)
fs.pwd()

print()
#Question 5 (b)
print('Question 5b')
fs.pwd()
fs.ls()


print()
print('Question 5c')

fs.cd("home")
fs.pwd()

print()
fs.cd("casa")

fs.ls()
print()
fs.cd ("thor")
print()
fs.ls()
print()
print("*************")
fs.rm ("quatsch.txt")
fs.ls()
print()
print('Question 5d ')

fs = FileSystem(root) # re-initialise fs



fs.mkdir("test") # the owner of the directory should be 'default' as not indicated.  fs.mkdir("test","isaac") would set the owner to isaac
fs.cd("test")
fs.create_file("test.txt")
fs.ls()




print()
print("Testing question 5e:  dot dot")

# to test this properly, let's create the entire file system using our previous functions!

root = Directory("root",[],owner="root")
fs = FileSystem(root)
fs.create_file("boot.exe")  # when creating a file we do not need to indicate owner, it will be the same as the working directory

print ("#################################")
fs.mkdir("test")
fs.mkdir("home",owner="root")
fs.cd("home")
print("-----LS after home")
fs.ls()
fs.cd("..")
print ("-----LS after cd..")
fs.ls()

print ("#################################")



fs.mkdir("thor",owner="thor")
fs.mkdir("isaac",owner="isaac")
fs.cd("thor")
print()
fs.create_file("hunde.jpg")
fs.create_file("quatsch.txt")
fs.cd("..")
fs.cd("isaac")
print("--")
fs.pwd()
fs.ls()
print()
fs.create_file("gatos.jpg")
print("--")
fs.pwd()
fs.ls()
print()
fs.cd("..")
print("--")
fs.pwd()
fs.ls()
print()
fs.cd("..")
print("--")
fs.pwd()
fs.ls()
print()
print("Testing question 5f:  rm")

fs.rm("test") # shouldn't work!
fs.ls()
fs.cd("test")
fs.ls()
print()
fs.rm("test.txt")
fs.cd("..")
fs.rm("test")
fs.ls()

print()
print("Testing question 5d:  mkdir and create file")
fs = FileSystem(root) # re-initialise fs

fs.mkdir("test") # the owner of the directory should be 'default' as not indicated.  fs.mkdir("test","isaac") would set the owner to isaac
fs.cd("test")
fs.create_file("test.txt")
fs.ls()
print()
print("Testing question 5e:  dot dot")

# to test this properly, let's create the entire file system using our previous functions!

root = Directory("root",[],owner="root")
fs = FileSystem(root)
fs.create_file("boot.exe")  # when creating a file we do not need to indicate owner, it will be the same as the working directory
fs.mkdir("test")
fs.mkdir("home",owner="root")
fs.cd("home")
fs.mkdir("thor",owner="thor")
fs.mkdir("isaac",owner="isaac")
fs.cd("thor")
fs.create_file("hunde.jpg")
fs.create_file("quatsch.txt")
fs.cd("..")
fs.cd("isaac")
fs.create_file("gatos.jpg")
fs.cd("..")
fs.cd("..")
fs.ls()

print()
print("Testing question 5f:  rm")

fs.rm("test") # shouldn't work!
fs.cd("test")
fs.rm("test.txt")
fs.cd("..")
fs.rm("test")
fs.ls()

print("Testing question 5g:  find")

print(fs.find("gatos.jpg"))
fs.cd("home")
print(fs.find("boot.exe")) # shouldn't find it!


print()
print("Testing question 5h:  chmod ,-l")
fs.chmod("boot.exe","u+x")
print()
fs.chmod("boot.exe","u+w")
print()
fs.chmod("boot.exe","u+r")
print()
fs.chmod("boot.exe","u-r")
print()
fs.chmod("boot.exe","u-r")
print()
fs.chmod("boot.exe","o+r")
print()

fs.chmod("boot.exe","ugo=rwx")
print()




print()

print ("%%%%%%%%%%%%%%  ls after test")
fs.ls("-l")

fs.mkdir("home2")

print ("---- ls after make home2")
fs.ls()

fs.cd("home2")
print ("---- ls after home2")
fs.ls()
fs.cd("..")
print ("---- ls after cd..")
fs.ls()
print("XXXXXXX")


fs.find("isaac")

print("XXXXXX")
