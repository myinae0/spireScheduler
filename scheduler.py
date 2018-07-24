import json, requests
import imageParser

file = 'screenshot.png'
textFile = 'text.txt'

#Start of CSMO file setup
open('schedule.csmo', 'w').close()
nameOfSchedule = input("What is the name of your schedule? ")
colors = ['#d11141', '#00b159', '#00aedb', '#f37735', '#ffc425', '#ffb3ba', '#ffdfba', '#ffffba', '#baffc9', '#bae1ff', '#ffffff']
scheduleFile = open('schedule.csmo', "a")
scheduleFile.write('{')
scheduleFile.write('"scheduleTitle":"{}",'.format(nameOfSchedule))
scheduleFile.write('"courses":[')

inputChoice = input("Are you inputting via screenshot or text? (Enter 'SCREEN' or 'TEXT') ")

def okayCheck() :
		print(len(infoGroup) == len(classGroup))

def titleFinder(titleString) :
	helper = titleString.split()
	return helper[0] + ' ' + helper[1]

def meetsWhen(daysOfWeekString) :
	#if('mo' not in daysOfWeekString and 'tu' not in daysOfWeekString and 'we' not in daysOfWeekString and 'th' not in daysOfWeekString and 'fr' not in daysOfWeekString and 'sa' not in daysOfWeekString and 'su' not in daysOfWeekString) :
	dayString = daysOfWeekString.lower()
	week = ['false', 'false', 'false', 'false', 'false', 'false', 'false']
	if('mo' in dayString) : week[0] = 'true'
	if('tu' in dayString) : week[1] = 'true'
	if('we' in dayString) : week[2] = 'true'
	if('th' in dayString) : week[3] = 'true'
	if('fr' in dayString) : week[4] = 'true'
	if('sa' in dayString) : week[5] = 'true'
	if('su' in dayString) : week[6] = 'true'
	return week

def timeSplit(startString) :
	initialSplit = startString.split(':')
	isAM = 'false'
	hourMinuteOrd = ['12', '0', 'true']
	if('AM' in startString or 'PM' in startString) :
		if(initialSplit[0] == 'TBA') :
			isAM = 'true'
			hourMinuteOrd = ['12', '0', 'true']
		else :
			if(initialSplit[1][2:] == 'AM') :
				isAM = 'true'
			minuteTime = initialSplit[1][:2]
			if(minuteTime[:1] == '0') :
				minuteTime = minuteTime[1:]
			hourMinuteOrd = [initialSplit[0], minuteTime, isAM]
	else :
		return 'TBA'
	return hourMinuteOrd

def classTypeFinder(titleString) :
	helper = titleString.split()
	return helper[2]

if(inputChoice == 'SCREEN') :
	sourceText = imageParser.imageToText(file)
	sourceArray = imageParser.imageToTextToArray(file)
	classGroup = []
	infoGroupHelper = []
	infoGroup = []

	classSchedule = sourceText.split('Schedule')

	classDone = False
	classPart = classSchedule[0].split('\n')
	for cell in classPart :
		if(cell == 'Class' or cell == '') :
			classDone = True
		else :
			if(classDone) :
				if(cell != '' and cell != ' ') :
					classGroup.append(cell)
				classDone = not classDone	
			else :
				if(cell != '' and cell != ' ') :
					classGroup[-1] = classGroup[-1] + " " + cell

	infoDone = False
	infoPart = classSchedule[1].replace('\n', 'asdf').split('asdf')
	for cell in infoPart :
		if(cell == 'Class' or cell == '') :
			infoDone = True
		else :
			if(infoDone) :
				infoGroupHelper.append(cell)
				infoDone = not infoDone
			else :
				infoGroupHelper[-1] = infoGroupHelper[-1] + " " + cell

	print(classGroup)

	infoText = ''
	cutoff = 30
	for cell in infoGroupHelper :
		if(infoText == '' or len(infoText) < cutoff) :
			if(cell == 'Room: TBA') :
				infoGroup.append(cell)
			else : 
				infoText += cell + ' '
		if(len(infoText) > cutoff) :
			infoGroup.append(infoText.strip())
			infoText = ''

	print(infoGroup)
	#Parsing the array for information

	counter = 0

	title = ''
	infoArray = []
	startTime = [0, 0, 0]
	startHour = startTime[0]
	startMinute = startTime[1]
	startIsAM = startTime[2]
	endTime = [0, 0, 0]
	endHour = endTime[0]
	endMinute = endTime[1]
	endIsAM = endTime[2]
	meetsWeek = ['false', 'false', 'false', 'false', 'false', 'false', 'false']
	classType = ''
	location = ''
	instructor = ''
	color = ''

	while(counter < len(classGroup)) :
		title = titleFinder(classGroup[counter])
		infoArray = infoGroup[counter].split(' ', 4)
		if(infoArray[0] != 'Room:') :
			meetsWeek = meetsWhen(infoArray[0])
			startTime = timeSplit(infoArray[1])
			endTime = timeSplit(infoArray[3])
			classType = classTypeFinder(classGroup[counter])
			location = infoArray[4]
		else :
			meetsWeek = ['false', 'false', 'false', 'false', 'false', 'false', 'false']
			startTime = ['12', '0', 'false']
			endTime = ['12', '30', 'false']
			classType = 'ERR'
			location = 'ERR'
		color = colors[counter]
		data = '''{{"title":"{}","meetingTimes":[{{"startHour":{},"startMinute":{},"startIsAM":{},"endHour":{},"endMinute":{},"endIsAM":{},"meetsOnMonday":{},"meetsOnTuesday":{},"meetsOnWednesday":{},"meetsOnThursday":{},"meetsOnFriday":{},"meetsOnSaturday":{},"meetsOnSunday":{},"classType":"{}","location":"{}","instructor":""}}],"color":"{}","SAVE_VERSION":3,"DATA_CHECK":"69761aa6-de4c-4013-b455-eb2a91fb2b76"}}'''.format(title, startTime[0], startTime[1], startTime[2], endTime[0], endTime[1], endTime[2], meetsWeek[0],  meetsWeek[1],  meetsWeek[2],  meetsWeek[3],  meetsWeek[4],  meetsWeek[5],  meetsWeek[6], classType, location, color)
		if(counter + 1 < len(classGroup)) :
			data += ','
		scheduleFile.write(str(data).replace('\'', '"'))
		counter = counter + 1
else :
	source = []
	with open(textFile) as f:
		for line in f :
			if(('Fall' not in line and 'Schedule' not in line) and ('Class' not in line and 'Schedule' not in line) and ('Academic' not in line and 'Calendar' not in line and 'Schedule' not in line)) :
				if(('Learning' not in line and 'Management' not in line and 'Systems' not in line)) :
					place = line.replace('\t', '').replace('\n', '')
					if(place == ' ') : place = place.replace(' ', '') 
					source.append(place)
				else :
					source.append('')

	counter = 0
	className = []
	classType = []
	classTime = []
	classRoom = []
	info = ''

	for cell in source :
		if(cell == '') : 
			counter = 1
		elif(counter == 1) :
			className.append(cell)
			counter = 2
		elif(counter == 2) :
			classType.append(cell)
			counter = 3
		elif(counter == 3) :
			if(('AM' in cell or 'PM' in cell) and '-' in cell) :
				classTime.append(cell)
				counter = 4
			else :
				classTime.append('TBA')
				classRoom.append('TBA')
				counter = 5
		elif(counter == 4) :
			classRoom.append(cell)
			counter = 0
		else :
			print('Uh, oh.')

	counter = 0

	title = ''
	startTime = ['12', '0', 'false']
	endTime = ['12', '1', 'false']
	meetsWeek = ['false', 'false', 'false', 'false', 'false', 'false', 'false']

	while(counter < len(className)) :
		title = className[counter]
		if('TBA' in classTime[counter] or 'TBA' in classRoom[counter]) :
			timeStuff = ['Err', '12:00PM', '-', '12:30PM']
		else :
			timeStuff = classTime[counter].split(' ')
		startTime = timeSplit(timeStuff[1])
		endTime = timeSplit(timeStuff[3])
		meetsWeek = meetsWhen(timeStuff[0])
		classTypeHelper = classType[counter]
		location = classRoom[counter]
		color = colors[counter]
		data = '''{{"title":"{}","meetingTimes":[{{"startHour":{},"startMinute":{},"startIsAM":{},"endHour":{},"endMinute":{},"endIsAM":{},"meetsOnMonday":{},"meetsOnTuesday":{},"meetsOnWednesday":{},"meetsOnThursday":{},"meetsOnFriday":{},"meetsOnSaturday":{},"meetsOnSunday":{},"classType":"{}","location":"{}","instructor":""}}],"color":"{}","SAVE_VERSION":3,"DATA_CHECK":"69761aa6-de4c-4013-b455-eb2a91fb2b76"}}'''.format(title, startTime[0], startTime[1], startTime[2], endTime[0], endTime[1], endTime[2], meetsWeek[0],  meetsWeek[1],  meetsWeek[2],  meetsWeek[3],  meetsWeek[4],  meetsWeek[5],  meetsWeek[6], classTypeHelper, location, color)
		if(counter + 1 < len(className)) :
			data += ','
		scheduleFile.write(str(data).replace('\'', '"'))
		counter = counter + 1

#End of file stuff
scheduleFile.write(']' + '}')
scheduleFile.close