from parse import parseDoc
# from table import readTables
import pandas as pd 
import argparse
import json

def insertionSort(page):
  
    # Traverse through 1 to len(arr)
    for i in range(1, len(page)):
  
        key = page[i][0].bbox[3]
        value = page[i]

        j = i-1
        while j >=0 and key < page[j][0].bbox[3] :
                page[j+1] = page[j]
                j -= 1
        page[j+1] = value
    return page




def removeEmpty(page):
	## Removing Empty Slot
	k = len(page) - 1 
	i = 0 
	while i < k:
		# print (page[i], (len(page[i])==1 and page[i][0].text == " "))
		if len(page[i])==1 and page[i][0].text ==" ":
			page.pop(i) 
			k-=1
			i-=1

		i+=1
	return page



def extendingLines(page):
	# Extending same lines
	k = len(page) - 1 
	i = 0 
	while i < k:
		# print (page[i], (len(page[i])==1 and page[i][0].text == " "))
		if int(page[i][0].bbox[3]) == int(page[i+1][0].bbox[3]):
			page[i].extend(page.pop(i+1))
			k-=1
			i-=1

		i+=1
	return page

def cutCorners(pages):
	# Thres upper - 145, lower - 720
	# Remove Header/ Footer
	k = len(page) - 1
	i = 0 
	while i < k:
		# print (page[i][0].bbox[3], int(page[i][0].bbox[3]) < 150, int(page[i][0].bbox[3])>720)
		if int(page[i][0].bbox[3]) < 150 or int(page[i][0].bbox[3])>720:
			page.pop(i)
			k-=1
			i-=1
		i+=1
	return page


def extractPointers(pages):
	dstruct = []
	data = []
	iind = 0
	s = 0
	# checking struct
	for line in page:
		for i,wrd in enumerate(line):
			if wrd.struct:
				s = 1
				# if i != 0:
				# 	line[i], line[0] == line[0], line[i]
				data.append(line)
				break

			elif wrd.note:
				s = 0 
				break

			elif s == 1:
				if wrd.text[0] in ['_']:
					continue
				if data[-1][0].font == line[0].font:
					data[-1].extend(line)
				s=0

	return data

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('--path', type=str, default='data\\HACKATHON_SAMPLE.pdf', help='path of the pdf file')
	parser.add_argument('--page', type=int, default=6, help='page')

	opt = parser.parse_args()

	pg = opt.page
	obj = parseDoc(opt.path)
	page = obj.readPage(pg)

	page = removeEmpty(page)


	page = insertionSort(page)

	page = cutCorners(page)

	page = extendingLines(page)


	data = extractPointers(page)

	# print (data)

	ival = None
	instruction = None

	tval = None
	task = None

	filedata = {}

	try:
		for line in data:
			if len(line[0].struct) == 1:
				ival = line[0].struct[0]
				instruction = line[0].text
				filedata[instruction] = []
				tval = None

			elif len(line[0].struct) == 2:
				tval = line[0].struct

				entry = {}
				task = line[0].text
				entry[task] = {'subtask':[]}
				for i in range(1, len(line)):
					entry[task]['subtask'].append(line[i].text)
				if ival and ival == line[0].struct[0]:
					filedata[instruction].append(entry)
				else:
					filedata['task '+str(tval[0])+'.'+str(tval[1])] = entry

				tval = tval[1]


			elif len(line[0].struct) == 3:
				point = line[0].struct

				entry = {}
				entry[line[0].text] = {'component':[]}
				for i in range(1, len(line)):
					entry[line[0].text]['component'].append(line[i].text)

				if ival is not None and tval is not None:
					filedata[instruction][-1][task]['subtask'].append(entry)
				else:
					# print ('yo')
					filedata['subtask '+str(point[0])+'.'+str(point[1])+'.'+str(point[2])] = entry

		# print (filedata)


	except:
		filedata['Structure'] = []
		for line in page:
			Line = []
			for wrd in line:
				Line.append(wrd.text)
			filedata['Structure'].append(Line)

	if filedata == {}:
		filedata['Structure'] = []
		for line in page:
			Line = []
			for wrd in line:
				Line.append(wrd.text)
			filedata['Structure'].append(Line)

	print (filedata)



	with open('pages/page '+str(pg)+'.json', 'w') as outfile:
	    json.dump(filedata, outfile)