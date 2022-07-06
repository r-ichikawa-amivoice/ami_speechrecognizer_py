import printf_util
import sys
import speechrecognizer
import recorder

if __name__ == "__main__":
	pri = printf_util.Printf_Util()

	input = "mic"
	authorization = ""

	# 引数のチェック
	for arg in sys.argv:
		if arg.startswith("o="):
			pri.output_type = arg[2:]
		elif arg.startswith("l="):
			pri.log_level = int(arg[2:])
		elif arg.startswith("r="):
			input = arg[2:]
		elif arg.startswith("a="):
			authorization = arg[2:]

	pri_ = pri.printf

	pri_("INFO", "try to init")
	stt = speechrecognizer.Speechrecognizer(pri_)
	rec = recorder.Recorder(pri_)

	def result_event(json):
		text = stt.result_to_text(json)
		pri_("INFO", text)

	def start():
		result = True
		for x in range(1):
			if not(stt.start()):
				pri_("ERROR", "stt start False")
				result = False
				break
			if not(rec.start()):
				pri_("ERROR", "rec start False")
				result = False
				break
		return result

	def stop():
		result = False
		if not(rec.get_state() == rec.RECORDER_STATE_DICT["SETUP"]):
			rec.stop()
			result = True
		if not(stt.get_state() == stt.SPEECHRECOGNIZER_STATE_DICT["SETUP"]):
			stt.stop()
			result = True
		return result

	def check_stop(state):
		if state == stt.SPEECHRECOGNIZER_STATE_DICT["SETUP"]:
			stop()

	def change_speechrecognizer_state():
		result = False
		if stt.get_state() == stt.SPEECHRECOGNIZER_STATE_DICT["SETUP"]:
			result = start()
		else:
			result = stop()
		return result

	pri_("INFO", "try to setup")
	rec.change_state_func = check_stop
	rec.recorder_write_func = stt.write

	if input == "mic":
		rec.audio_type = "mic"
		pri_("DEBUG", rec.get_device())
		rec.audio_source = -1
		for m in rec.get_device():
			if m["name"] == "pulse":
				rec.audio_source = m["index"]
		if rec.audio_source == -1:
			pri_("ERROR", "pulseaudio not found")
		stt.codec = stt.rate_to_format(rec.get_device(rec.audio_source)[0]["defaultSampleRate"], head = False)
		#rec.audio_format["CHANNELS"] = rec.get_device(rec.audio_source)[0]["maxInputChannels"]
		rec.audio_format["CHANNELS"] = 1
		rec.audio_format["CHUNK"] = 4096
		rec.audio_format["RATE"] = int(rec.get_device(rec.audio_source)[0]["defaultSampleRate"])
		pri_("DEBUG", "channel = " + str(rec.audio_format["CHANNELS"]))
	else:
		rec.audio_type = "file"
		rec.audio_source = input
		stt.codec = "16k"

	#rec.record_flag = True
	stt.server_url = "wss://acp-api.amivoice.com/v1/"
	stt.grammar_file_names = "-a-general"
	stt.authorization = authorization

	stt.init_speechrecognizer()
	stt.set_event_func(result_finalized_func = result_event)
	
	pri_("INFO", "start APP!!")
	start()
