## encoding: UTF-8
import sys
import threading
import time
from functools import partial
import traceback

class Recorder():
	printf_func = print

	RECORDER_STATE_DICT = {
		"SETUP": 0,
		"PAUSE": 1,
		"RECORDING": 2
	}
	recorder_state = None
	change_state_func = None

	RECORDER_INSTRUCTION_DICT = {
		"STOP": 0,
		"START": 1
	}
	recorder_instruction = RECORDER_INSTRUCTION_DICT["STOP"]

	audio_format = {
		"RATE": 16000,
		"CHUNK": 8192,
		"CHANNELS": 1
	}

	record_flag = False
	record_output_filename = "out.adc"

	audio_type = "file"
	audio_source = "audio.wav"
	recorder_write_func = None

	recorder_thread = None

	def channnel_parse(self, audio, channel = -1):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		if channel == -1:
			channel = self.audio_format["CHANNELS"]
		audio_ch = [b"" for i in range(channel)]
		for i in range(len(audio)):
			audio_ch[int((i % (2 * channel)) / 2)] += bytes([audio[i]])

		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")
		return audio_ch

	def change_state(self, state):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		self.recorder_state = state
		if not(self.change_state_func is None):
			self.change_state_func(state)
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")

	def start(self):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		result = False

		for i in range(1):
			if not(self.recorder_state == self.RECORDER_STATE_DICT["SETUP"]):
				self.printf_func("ERROR", sys._getframe().f_code.co_name +": recorder_state: " + str(self.recorder_state))
				break
			if (self.recorder_instruction == self.RECORDER_INSTRUCTION_DICT["START"]):
				self.printf_func("ERROR", sys._getframe().f_code.co_name +": recorder_instruction: " + str(self.recorder_state))
				break
				
			self.recorder_thread = threading.Thread(target=self.record)
			self.recorder_instruction = self.RECORDER_INSTRUCTION_DICT["START"]
			self.recorder_thread.start()
			time_out = False
			time_out_time = 10
			i = 0
			interval = 1000
			while self.recorder_state == self.RECORDER_STATE_DICT["SETUP"]:
				time.sleep(1.0 / interval)
				#self.printf_func("DEBUG", "interval: " + str(i))
				i += 1
				if i > (time_out_time * interval):
					self.printf_func("ERROR", "rec start time out")
					time_out = True
					break
			if time_out:
				self.recorder_instruction = self.RECORDER_INSTRUCTION_DICT["STOP"]
				break

			result = True
			break
			
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")
		return result

	def stop(self):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		result = False

		for i in range(1):
			if (self.recorder_state == self.RECORDER_STATE_DICT["SETUP"]):
				self.printf_func("ERROR", sys._getframe().f_code.co_name +": recorder_state: " + str(self.recorder_state))
				break
			if (self.recorder_instruction == self.RECORDER_INSTRUCTION_DICT["STOP"]):
				self.printf_func("ERROR", sys._getframe().f_code.co_name +": recorder_instruction: " + str(self.recorder_instruction))
				break
			self.recorder_instruction = self.RECORDER_INSTRUCTION_DICT["STOP"]
			self.recorder_thread.join()
			result = True
			break
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")
		return result

	def get_device(self, index = -1):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")

		import pyaudio
		pyaudio_handle = pyaudio.PyAudio()
		device = pyaudio_handle.get_device_count()
		result = []
		if index == -1:
			for i in range(device):
				#self.printf_func("DEBUG", pyaudio_handle.get_device_info_by_index(i))
				result.append(pyaudio_handle.get_device_info_by_index(i))
		else:
			#self.printf_func("DEBUG", pyaudio_handle.get_device_info_by_index(index))
			result.append(pyaudio_handle.get_device_info_by_index(index))
			
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")
		return result

	def stream_init(self):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")

		audio_stream = None
		if self.audio_type == "mic":
			import pyaudio
			pyaudio_handle = pyaudio.PyAudio()
			self.printf_func("DEBUG", self.audio_format["RATE"])
			#self.audio_format["RATE"] = int(pyaudio_handle.get_device_info_by_index(self.audio_source)["defaultSampleRate"])
			audio_stream_ = pyaudio_handle.open(
				rate = self.audio_format["RATE"],
				input_device_index = self.audio_source,       
				channels = self.audio_format["CHANNELS"],
				format = pyaudio.paInt16,
				input = True,
				frames_per_buffer = self.audio_format["CHUNK"]
			)
			def close(audio_stream, pyaudio_handle):
				audio_stream.stop_stream()
				audio_stream.close()
				pyaudio_handle.terminate()
			audio_stream = {
				"read": audio_stream_.read,
				"close": partial(close, audio_stream_, pyaudio_handle)
			}
		if self.audio_type == "file":
			audio_stream_ = open(self.audio_source, "rb")
			def read(audio_stream, chunk):
				sleep_time = (self.audio_format["CHUNK"] * 1000.0 / 2 / self.audio_format["RATE"]) / 1000.0
				#self.printf_func("DEBUG", "sleep time: " + str(sleep_time))
				# 微小時間のスリープ
				time.sleep(sleep_time)
				return audio_stream.read(chunk)
			audio_stream = {
				"read": partial(read, audio_stream_),
				"close": audio_stream_.close
			}

		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")
		return audio_stream

	def record(self):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		self.change_state(self.RECORDER_STATE_DICT["PAUSE"])
		for i in range(1):
			if self.recorder_write_func is None:
				
				self.printf_func("ERROR", sys._getframe().f_code.co_name +": recorder_write_func is None")
				break
			
			self.change_state( self.RECORDER_STATE_DICT["RECORDING"])
			self.printf_func("INFO", "record start")
			try:
				audio_stream = self.stream_init()
				
				# 音声データファイルからの音声データの読み込み
				audio_data = audio_stream["read"](self.audio_format["CHUNK"])

				frame = []
				
				self.printf_func("DEBUG", "recorder_instruction == RECORDER_INSTRUCTION_DICT[\"START\"]: " + str(self.recorder_instruction == self.RECORDER_INSTRUCTION_DICT["START"]))
				while self.recorder_instruction == self.RECORDER_INSTRUCTION_DICT["START"] and len(audio_data) > 0:

					# 音声データの送信
					if not self.recorder_write_func(audio_data, len(audio_data)):
						self.printf_func("ERROR", "recorder_write_func: False")
						break

					if self.record_flag:
						with open(self.record_output_filename, mode="ab") as f:
							f.write(audio_data)

					# 音声データファイルからの音声データの読み込み
					audio_data = audio_stream["read"](self.audio_format["CHUNK"])

				audio_stream["close"]()
			except Exception as e:
				self.printf_func("ERROR", e)
				self.printf_func("ERROR", traceback.format_exc())
				self.printf_func("ERROR", u"音声データ %s の読み込みに失敗しました。" % self.audio_source)
			
		self.change_state(self.RECORDER_STATE_DICT["SETUP"])
		self.recorder_instruction = self.RECORDER_INSTRUCTION_DICT["STOP"]
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")
		
	def get_state(self):
		return self.recorder_state	

	def __init__(self, printf_func = None):
		if not(printf_func is None):
			self.printf_func = printf_func
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		self.recorder_state = self.RECORDER_STATE_DICT["SETUP"]
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")
	
