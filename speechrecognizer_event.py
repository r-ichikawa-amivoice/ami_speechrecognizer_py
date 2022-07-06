import json
import amivoice.WrpListener
import sys

def text_(result):
	try:
		return json.loads(result)["text"]
	except:
		return None

class Speechrecognizer_Event(amivoice.WrpListener):
	printf_func = print

	utterance_started_func = None
	utterance_ended_func = None
	result_created_func = None
	result_updated_func = None
	result_finalized_func = None
	event_notified_func = None
	trace_func = None

	def __init__(self, printf_func = None):
		if not(printf_func is None):
			self.printf_func = printf_func
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")

	def run_func(self, func = None, opt = None):
		if not(func is None):
			if (func is None):
				func()
			else:
				func(opt)
			return True
		return False

	def utteranceStarted(self, startTime):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		self.printf_func("DEBUG", "S %d" % startTime)

		self.run_func(self.utterance_started_func, startTime)

		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")

	def utteranceEnded(self, endTime):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		self.printf_func("DEBUG", "E %d" % endTime)

		self.run_func(self.utterance_ended_func, endTime)
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")

	def resultCreated(self):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		self.printf_func("DEBUG","C")

		self.run_func(self.result_created_func)
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")

	def resultUpdated(self, result):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		#self.printf_func("DEBUG","U %s" % result)
		self.printf_func("DEBUG","U")
		text = text_(result)
		if text != None:
			self.printf_func("DEBUG","   -> %s" % text)

		self.run_func(self.result_updated_func, result)
	
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")

	def resultFinalized(self, result):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		#self.printf_func("DEBUG","F %s" % result)
		self.printf_func("DEBUG","F")
		text = text_(result)
		if text != None:
			self.printf_func("DEBUG","   -> %s" % text)

		if not(self.run_func(self.result_finalized_func, result)):
			self.printf_func("WORN","result_finalized_func is None")

		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")

	def eventNotified(self, eventId, eventMessage):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		self.printf_func("DEBUG",eventId + " " + eventMessage)

		self.run_func(self.event_notified_func, eventMessage)

		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")

	def TRACE(self, message):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		self.printf_func("DEBUG", message)

		self.run_func(self.trace_func, message)

		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")



