#
# $Id: LineParser.py 551 2006-05-07 19:51:32Z nicb $
#

import string
import ConfParser

import pdb

class LineParser(ConfParser.ConfParser):
	"""
	LineParser --- a Parser of configuration files
	which have pipe-separated record lines.
	The virtal 'save' method is used in children classes
	to define the specialized record saving.
	"""

	def splitchar(self):
		"""LineParser.splitchar()

		Returns the splitting character for all fields
		"""
		return self.mysplitchar

	def set_splitchar(self, char):
		"""LineParser.set_splitchar(char)
	
		Sets the splitting character and returns the previous one.
		"""
		old_splitchar = self.splitchar()
		self.mysplitchar = char
		return old_splitchar

	def parse(self, line):
		return string.split(line, self.splitchar())

	def load(self, fdbname):
		"""LineParser.load(fdbname)
	
		Opens a file and reads out all lines,
		and finally calling the parse() method
		to and passing the obtained array.
		"""
		ConfParser.ConfParser.load(self, fdbname)

		while 1:
			#pdb.set_trace()
			(line, EOF) = self.readline()
			if EOF == True:
				break
			if len(line):
				datum = None
				try:
					datum = self.parse(line)
				except self.error:
					print str(self.error)
				else:
					self.save(datum)

	def __init__(self, sepchar='|', commentchar='#'):
		ConfParser.ConfParser.__init__(self, commentchar)
		self.mysplitchar = sepchar # this can't be done using methods
