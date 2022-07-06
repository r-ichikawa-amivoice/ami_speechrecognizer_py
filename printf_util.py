import datetime
class Printf_Util:
	LOG_LEVEL_DICT = {"DEBUG": 0, "INFO": 1, "WORN": 2, "ERROR": 3}
	log_level = 1
	output_type = "console"

	def __output(self, text, level):
		if self.output_type == "console":
			color_reset = "\033[0m"
			color = '\033[37m'
			if level == "ERROR":
				color = '\033[31m'
			if level == "WORN":
				color = '\033[33m'
			if level == "INFO":
				color = '\033[34m'
			print(color + text + color_reset)
		elif self.output_type == "date":
			with open(str(datetime.date.today())+".txt", mode="a") as f:
				f.write(text+"\n")

		else:
			with open(self.output_type, mode="a") as f:
				f.write(text+"\n")

	def printf(self, level, text):
		if type(level) is int:
			if level in self.LOG_LEVEL_DICT.values():
				box = ([k for k, v in self.LOG_LEVEL_DICT.items() if v == level])
				if len(box) > 0:
					level = box[0]
		if self.LOG_LEVEL_DICT.get(level) is None:
			if (self.LOG_LEVEL_DICT["ERROR"] >= self.log_level):
				self.__output("%s\t[ERROR]\tOperation: level \"%s\" is not defined: msg = \"%s\"" % (datetime.datetime.now(), level, text), "ERROR")
		elif self.log_level <= self.LOG_LEVEL_DICT[level]:
			self.__output("%s\t[%s]\t%s" % (datetime.datetime.now(), level, text), level)
