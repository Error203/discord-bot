import qlogger
import argparse


class BotConsole:


	def __init__(self, level):

		self.log = qlogger.Logger("bot console logs", level=level).get_logger("bot console")
		self.null_stream_file = "null"
		self.null_stream_rights = "ab+"
		self.null_check = "rb"
		self.end_char = b"\x03"
		self.arg_pause = b"\x20"
		self.start_char = b"\x02"


	def start_console(self):

		try:

			with open(self.null_stream_file, "wb") as null_stream:
				null_stream.write(b"")

			self.log.debug("cleared null")

			while True:
				command = input("command for bot# ")
				command = command.strip().split(" ")
				command_args = command[1:len(command)]
				command = command[0]

				with open(self.null_stream_file, self.null_stream_rights) as null_stream:
					null_stream.write(self.start_char + bytes(command, "utf-8") + self.end_char)
				# self.log.debug(f"args: {command_args}")
				# self.log.debug(f"command: {command}")

		except KeyboardInterrupt:
			print("\n")
			self.log.info("stopped operation")

			self.check_null()

		except Exception as e:
			self.log.exception(e)

			with open(self.null_stream_file, self.null_stream_rights) as null_stream:
				null_stream.write(self.start_char + b"exception" + self.end_char)


	def check_null(self):

		try:
			with open(self.null_stream_file, self.null_check) as null_stream:
				null_stream = null_stream.read()

				null_stream = null_stream.replace(b"\x03", b"")
				commands = null_stream.split(b"\x02")
				del(commands[0])

				self.log.debug(f"total commands flushed {len(commands)}:\n{commands}")

		except Exception as e:
			self.log.exception(e)
			


def main():
	parser = argparse.ArgumentParser(
					description="WebDog network tool. (netcat analog).",
					epilog="Simple use. Can be used without arguments.",
					)
	parser.add_argument("-v", "--verbose", action="store_true", help="more detailed information about script steps.")
	parser.add_argument("-c", "--console", action="store_true", help="initialize an internal script console to control over the situation.")

	args = parser.parse_args()

	if args.verbose:
		level = qlogger.logging.DEBUG
	else:
		level = qlogger.logging.INFO

	bot_con = BotConsole(level)
	bot_con.start_console()

if __name__ == '__main__':
	main()