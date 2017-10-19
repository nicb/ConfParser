#
# $Id: MultilineParser.py 357 2006-03-03 21:46:57Z nicb $
#

import string
import ConfParser

import pdb

class MultilineParser(ConfParser.ConfParser):
	"""
	MultilineParser --- a Parser of configuration files
	which have multi-line records.
	The virtal 'save' method is used in children classes
	to define the specialized record saving.
	"""

	def record_start(self, line):
		"""MultilineParser.record_start(line)

		Returns True if the line is a record start,
		otherwise returns false.
		"""
		return False

	def record_end(self, line):
		"""MultilineParser.record_end(line)

		Returns True if the line is a record end,
		otherwise returns false.
		"""
		return False

	def inside_record(self):
		"""MultilineParser.inside_record()

		Returns True if parsing is inside a record,
		False otherwise
		"""
		return self.inside_record_flag

	def add_line(self, line):
		self.cur_record.add_line(line)

	def parse(self, line):
		"""MultilineParser.parse(line)

		The parse() method and reads the line in argument looking for a record start.
		When it finds one, it calls the virtual function add_line()
		which will actually read the record. This method returns none until 
		a record_end is actually found. At that point, the actual record
		is returned.
		"""
		result = None
		if self.inside_record_flag == True:
			if self.record_end(line) == False:
				self.add_line(line)
			else:
				result = self.cur_record
		else:
			self.record_start(line) # starts record *only* if line is a record start

		return result


	def load(self, fdbname):
		"""MultilineParser.load(fdbname)
	
		Opens a file and reads out all lines,
		getting record starts and record ends.
		When a record end is reached, it
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
					if datum != None:		# if a record_end has been found
						self.save(datum)

	def __init__(self, commentchar='#'):
		ConfParser.ConfParser.__init__(self, commentchar)
		self.cur_record = None
		self.inside_record_flag = False
