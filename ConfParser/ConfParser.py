#
# $Id: ConfParser.py 551 2006-05-07 19:51:32Z nicb $
#

import re
import string

import pdb

class ParseError:
	"""
	ConfParser.ParseError()
	Exception raised when a parse error occurs during the parsing of the
	record lines

	The error message is returned as a string object
	"""
	def set_line(self, linenum, line):
		self.linenum = linenum
		self.line = line

	def set_error(self, err):
		self.msg =  ": ParseError at line %d (\"%s\"): %s" % (self.linenum, self.line, err)

	def __str__(self):
		return self.msg

	def __init__(self):
		self.set_line(0, '')


class ConfParser:
	"""
	ConfParser --- Base class for configuration file parsing.
	The virtual 'load' method is used in derived classes
	to specify the way to read records.
	The virtal 'save' method is used in derived classes
	to define the specialized record saving.
	"""

	def clean_comments(self, l):
		"""ConfParser.clean_comments(line)

		This is a method that removes all comments from a line.
		A comment is usually initiated by a commenting character
		('#' by default) and extends to end of line. The whitespace
		leading to the comment is also removed. The cleaned
		up line is returned to the caller.
		"""
		result = re.sub(self.comment_re, '', l)
		string.rstrip(result) # strip trailing whitespace
		return result

	def save(self, d):
		"""ConfParser.save(data)
	
		This is a virtual function usually implemented in end-user subclasses.
		It gets an array which contains all the positional fields to
		be saved in the specific database. The subclass implementation
		defines what to do with the array.
		"""
		pass

	def parse(self, l):
		"""ConfParser.parse(line)
	
		This is a virtual function usually implemented in subclasses.
		It gets a single line string which must be parsed according
		to the rules implemented therein.
		"""
		pass

	def readline(self):
		"""ConfParser.readline()

		Returns a tuple containing the read line and the EOF flag.
		If the EOF flag is set to true, then the file is finished
		and the line does not contain anything. Otherwise, the line
		returned is actually valid.
		"""
		EOF = False
		line = self.f.readline()
		if len(line) == 0:				# zero-lengh is EOF
			EOF = True
		self.linenum = self.linenum + 1
		line = line[:-1]				# chop
		self.error.set_line(self.linenum, line)
		line = self.clean_comments(line)
		return (line, EOF)

	def load(self, fdbname):
		"""ConfParser.load(fdbname)

		Opens a file and set the number of lines read to 0.
		This method is generally called from children classes
		that then will read the file in different ways.
		"""
		self.f = open(fdbname, "r")
		self.linenum = 0

	def set_comment_char(self, char):
		"""ConfParser.set_comment_char(c)

		Sets the comment delimiter character.
		"""
		#pdb.set_trace()
		#comment_regexp = "\\s+%c.*$" % char
		comment_regexp = "%c.*$" % char
		self.comment_re = re.compile(comment_regexp)

	def __del__(self):
		if (self.f != None):
			self.f.close()

	def __init__(self, commentchar='#'):
		self.f = None
		self.set_comment_char(commentchar)
		self.error = ParseError()
		self.linenum = 0
