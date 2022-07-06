# encoding: UTF-8
import sys

# <!-- バイトコードキャッシュファイルの作成を抑制するために...
sys.dont_write_bytecode = True
# -->
import amivoice.Wrp
import speechrecognizer_event


class Speechrecognizer():
	printf_func = print

	SPEECHRECOGNIZER_STATE_DICT = {
		"SETUP": 0,
		"PAUSE": 1,
		"RECORDING": 2
	}
	speechrecognizer_state = None
	change_state_func = None

	# WebSocket 音声認識サーバ URL
	server_url = None
	# プロキシサーバ名
	proxy_server_name = None
	# 音声データファイル名
	audio_file_names = []
	# グラマファイル名
	grammar_file_names = None
	# プロファイル ID
	profile_id = None
	# プロファイル登録単語
	profile_words = None
	# セグメンタプロパティ
	segmenter_properties = None
	# フィラー単語を保持するかどうか
	keep_filler_token = None
	# 認識中イベント発行間隔
	result_updated_interval = None
	# 拡張情報
	extension = None
	# サービス認証キー文字列
	authorization = None
	# 音声データ形式
	codec = None
	# 認識結果タイプ
	result_type = None
	# サービス認証キー文字列
	service_authorization = None
	# 接続タイムアウト
	connect_timeout = 5000
	# 受信タイムアウト
	receive_timeout = 0
	# 処理ループ (1～)
	loop = 1
	# スリープ時間
	sleep_time = -2
	# 詳細出力
	verbose = False
	# 実装タイプ
	implementation = 1

	def rate_to_format(self, rate, head = False):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		result = ""
		if head:
			if rate == 8000:
				result = "8k"
			if rate == 16000:
				result = "16k"
		else:
			if rate == 8000:
				result = "lsb8k"
			if rate == 16000:
				result = "lsb16k"
			if rate == 22000:
				result = "lsb22k"
			if rate == 32000:
				result = "lsb32k"
			if rate == 44100:
				result = "lsb44k"
			if rate == 48000:
				result = "lsb48k"
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")
		return result

	def change_state(self, state):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		self.speechrecognizer_state = state
		if not(self.change_state_func is None):
			self.change_state_func(state)
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")

	def set_event_func(self, 
		utterance_started_func = None, 
		utterance_ended_func = None, 
		result_created_func = None, 
		result_updated_func = None, 
		result_finalized_func = None, 
		event_notified_func = None, 
		trace_func = None
	):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		if not(utterance_started_func is None):
			self.listener.utterance_started_func = utterance_started_func 
		if not(utterance_ended_func is None): 
			self.listener.utterance_ended_func = utterance_ended_func
		if not(result_created_func is None): 
			self.listener.result_created_func = result_created_func
		if not(result_updated_func is None):
			self.listener.result_updated_func = result_updated_func 
		if not(result_finalized_func is None):
			self.listener.result_finalized_func = result_finalized_func
		if not(event_notified_func is None):
			self.listener.event_notified_func = event_notified_func 
		if not(trace_func is None):
			self.listener.trace_func = trace_func
		
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")

	def get_state(self):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		self.printf_func("DEBUG", "speechrecognizer_state: " + str(self.speechrecognizer_state))
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")
		return self.speechrecognizer_state
		

	def init_speechrecognizer(self):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		# WebSocket 音声認識サーバイベントリスナの作成
		#listener = WrpTester(verbose)

		# WebSocket 音声認識サーバの初期化
		self.speechrecognizer_handle.setListener(self.listener)
		self.speechrecognizer_handle.setServerURL(self.server_url)
		self.speechrecognizer_handle.setProxyServerName(self.proxy_server_name)
		self.speechrecognizer_handle.setConnectTimeout(self.connect_timeout)
		self.speechrecognizer_handle.setReceiveTimeout(self.receive_timeout)
		self.speechrecognizer_handle.setGrammarFileNames(self.grammar_file_names)
		self.speechrecognizer_handle.setProfileId(self.profile_id)
		self.speechrecognizer_handle.setProfileWords(self.profile_words)
		self.speechrecognizer_handle.setSegmenterProperties(self.segmenter_properties)
		self.speechrecognizer_handle.setKeepFillerToken(self.keep_filler_token)
		self.speechrecognizer_handle.setResultUpdatedInterval(self.result_updated_interval)
		self.speechrecognizer_handle.setExtension(self.extension)
		self.speechrecognizer_handle.setAuthorization(self.authorization)
		self.speechrecognizer_handle.setCodec(self.codec)
		self.speechrecognizer_handle.setResultType(self.result_type)
		self.speechrecognizer_handle.setServiceAuthorization(self.service_authorization)

		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")

	def start(self):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")

		result = False

		for i in range(1):

			if not(self.speechrecognizer_state == self.SPEECHRECOGNIZER_STATE_DICT["SETUP"]):
				self.printf_func("ERROR", "operation: speechrecognizer_state = " + str(self.speechrecognizer_state))			
				break

			# WebSocket 音声認識サーバへの接続
			if not self.speechrecognizer_handle.connect():
				self.printf_func("ERROR", u"WebSocket 音声認識サーバ %s への接続に失敗しました。" % self.server_url)			
				break

			if not self.speechrecognizer_handle.feedDataResume():
				self.printf_func("ERROR", self.speechrecognizer_handle.getLastMessage())
				self.printf_func("ERROR", u"WebSocket 音声認識サーバへの音声データの送信の開始に失敗しました。")
				break

			self.change_state(self.SPEECHRECOGNIZER_STATE_DICT["PAUSE"])
			self.printf_func("DEBUG", "start to speech recognizer!")			
			result = True
			break

		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")
		return result

	def stop(self):
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		result = False
		for i in range(1):
			if self.speechrecognizer_state == self.SPEECHRECOGNIZER_STATE_DICT["PAUSE"] or self.speechrecognizer_state == self.SPEECHRECOGNIZER_STATE_DICT["RECORDING"]:
				self.change_state(self.SPEECHRECOGNIZER_STATE_DICT["SETUP"])

				if not self.speechrecognizer_handle.feedDataPause():
					self.printf_func("ERROR", self.speechrecognizer_handle.getLastMessage())
					self.printf_func("ERROR", u"WebSocket 音声認識サーバへの音声データの送信の完了に失敗しました。")
					break
				# WebSocket 音声認識サーバからの切断
				self.speechrecognizer_handle.disconnect()
				self.printf_func("DEBUG", "stop to speech recognizer!")
			else:
				self.printf_func("ERROR", "operation: speechrecognizer_state = " + str(self.speechrecognizer_state))			
				break
			result = True
			break
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")
		return result

	def write(self, audio_data, audio_size):
		#self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")

		result = False
		for i in range(1):
			if (self.speechrecognizer_state == self.SPEECHRECOGNIZER_STATE_DICT["SETUP"]):
				self.printf_func("ERROR", "speechrecognizer_state: " + str(self.speechrecognizer_state))
				break
			if (self.speechrecognizer_state == self.SPEECHRECOGNIZER_STATE_DICT["PAUSE"]):
				self.change_state(self.SPEECHRECOGNIZER_STATE_DICT["RECORDING"])
			# WebSocket 音声認識サーバへの音声データの送信
			if not self.speechrecognizer_handle.feedData(audio_data, 0, audio_size):
				self.printf_func("ERROR", self.speechrecognizer_handle.getLastMessage())
				self.printf_func("ERROR", u"WebSocket 音声認識サーバへの音声データの送信に失敗しました。")
				break

			result = True
			break

		#self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")
		return result

	def result_to_text(self, result):
		#try:
			return speechrecognizer_event.text_(result)
		
		#except:
		#	return None

	def __init__(self, printf_func):
		if not(printf_func is None):
			self.printf_func = printf_func
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" ->")
		self.listener = speechrecognizer_event.Speechrecognizer_Event(printf_func)
		self.change_state(self.SPEECHRECOGNIZER_STATE_DICT["SETUP"])

		# WebSocket 音声認識サーバの初期化
		self.speechrecognizer_handle = amivoice.Wrp.construct(self.implementation)
		self.printf_func("DEBUG", self.__class__.__name__ + "."+ sys._getframe().f_code.co_name +" <-")

