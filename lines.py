# Faisal Jaffer
# Capital One Software Engineer Technical Assessment
#
# Assumptions:
# 	For Python comments, it is assumed that single line comments are started with #
# and multiline comments are consecutive lines starting with #. Also valid comments
# are only declared outside quotes.
#

import sys

file_name = sys.argv[1]

file_type = file_name.split(".")[-1]

if file_type not in ["java", "c", "js", "py"]:
	print("Not a supported file type. Please provide a java, c, js or py file.")
	exit()

file = open(file_name, "r")

totalLines = 0
totalComLines = 0
singleComLines = 0
comBlockLines = 0
blockLines = 0
todoLines = 0

blockComment = False

# validate that comment syntax does not appear inside quotes
def validComment(line, syntax):
	singleQuote = False
	doubleQuote = False
	for c in range(len(line)):
		if line[c] == '"':
			if not singleQuote: # only open double quote if no open single quote appears before
				doubleQuote = not doubleQuote
		elif line[c] == "'":
			if not doubleQuote: # only open single quote if no open double quote appears before
				singleQuote = not singleQuote
		if syntax == line[c:c+len(syntax)]:
			if not singleQuote and not doubleQuote: # only if syntax appears in line and no open quote
				return True
	return False # no syntax appears in line or syntax appears inside open quotes



if file_type in ["java", "c", "js"]:
	for line in file:
		filteredLine = line.lstrip() # remove leading spaces from current line
		if not blockComment and validComment(filteredLine, "//"): # single line comment
			totalComLines+=1
			singleComLines+=1
		elif not blockComment and validComment(filteredLine, "/*"): # block comment starts
			totalComLines+=1
			comBlockLines+=1
			blockLines+=1
			if not validComment(filteredLine, "*/"): # check if current line does not have block comment end
				blockComment = True
		elif blockComment:
			totalComLines+=1
			comBlockLines+=1
			if validComment(filteredLine, "*/"):
				blockComment=False
		if "TODO" in filteredLine: # check for TODO
			todoLines+=1
		totalLines+=1

elif file_type == "py":
	lastComLineCheck = False
	blockCount = 0
	for line in file:
		filteredLine = line.lstrip()
		if not lastComLineCheck and validComment(filteredLine, "#"):
			totalComLines+=1
			lastComLineCheck = True
			blockCount = 1
		elif lastComLineCheck and validComment(filteredLine, "#"):
			totalComLines+=1
			blockCount+=1

		if "TODO" in filteredLine: # check for TODO
			todoLines+=1
		if not validComment(filteredLine, "#"):
			if lastComLineCheck and blockCount == 1:
				singleComLines+=1
			lastComLineCheck = False
			if blockCount > 1:
				comBlockLines += blockCount
			blockCount = 0
		if blockCount == 2:
			blockLines+=1
		totalLines+=1

print("Total # of lines:", totalLines)
print("Total # of comment lines:", totalComLines)
print("Total # of single line comments:", singleComLines)
print("Total # of comment lines within block comments:", comBlockLines)
print("Total # of block line comments:", blockLines)
print("Total # of TODO's:", todoLines)
