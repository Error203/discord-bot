import discord
import qlogger
import argparse
import handle_key


class DiscordClient:


	def __init__(self, level, console):

		self.log = qlogger.Logger("bot logs", level=level).get_logger("bot")
		self.dev_id = 407598463010734080
		self.my_id = 577946641600872487


	def start_bot(self, token):
		client = discord.Client()
		command_prefix = "$$"
		allowed_commands = ["dada", "help", "info"]
		prefixed_allowed_commands = [command_prefix]

		for cmd in allowed_commands:
			prefixed_allowed_commands.append(command_prefix + cmd)

		@client.event
		async def on_ready():
			self.log.info(f"logged as {client.user}")
			# if console:
			# 	self.log.info("initializing an internal console")
			for guild in client.guilds:
				if guild.id == 780077774508654603:
					self.main_guild = guild

					self.guild_owner_id = self.main_guild.owner_id

			for member in self.main_guild.members:
				print(member)

		@client.event
		async def on_message(message):
			handled_message = message.content.split(" ")
			used_cmd = handled_message[0].lower()
			command_arguments = handled_message[1:len(handled_message)]
			user_main_nickname = message.author.name

			if used_cmd.startswith(command_prefix):
				self.log.info(f"{message.author.id} said# {message.content}")
			
				if message.author != client.user:
					await message.delete()
				
				if used_cmd == command_prefix + "dada":
					await message.channel.send("Еге-ж...")

				if used_cmd == command_prefix + "help" or used_cmd == command_prefix + "info":

					mention_dev_name = f"<@!{self.dev_id}>"
					user_id = message.author.id
					mention_user_name = f"<@!{user_id}>"
					status = "тестер"

					if user_id == self.dev_id:
						status = "розробник"

					elif user_id == self.guild_owner_id:
						status = "засновник серверу"

					elif user_id == self.my_id:
						status = "Пан Робот"

					if not command_arguments:
						await message.channel.send(f"За допомогою звертайтеся до {mention_dev_name} або відправивши **$$**(два символа долару)\n" + \
							f"Ваш псевдонім на сервері: {mention_user_name}\nВаш ID: {user_id}\nВаш статус: {status}")

					if command_arguments:
						try:
							if command_arguments[0].isdigit():
								requested_user_id = int(command_arguments[0])
								self.log.debug(requested_user_id)
								status = "тестер"

								if requested_user_id == self.dev_id:
									status = "розробник"

								elif requested_user_id == self.guild_owner_id:
									status = "засновник серверу"

								elif requested_user_id == self.my_id:
									status = "Пан Робот"

							elif not command_arguments[0].isdigit():
								requested_user_id = int(command_arguments[0][3:-1])
								status = "тестер"

								if requested_user_id == self.dev_id:
									status = "розробник"

								elif requested_user_id == self.guild_owner_id:
									status = "засновник серверу"

								elif requested_user_id == self.my_id:
									status = "Пан Робот"

								self.log.debug(requested_user_id)

							mention_requested_user = f"<@!{requested_user_id}>"
							await message.channel.send(f"Інформація про {mention_requested_user}:\nСтатус: {status}\nID: {requested_user_id}")

						except Exception as e:
							self.log.warning("not a serious error, but check it")
							self.log.exception(e)


				if used_cmd == command_prefix + "clear":
					pass

				if used_cmd == command_prefix:
					await message.channel.send("Дозволені команди:\n\n{0}".format(f"\n".join(prefixed_allowed_commands)))

				# message.content.lower() not in allowed_commands:
				if used_cmd not in prefixed_allowed_commands:
					await message.channel.send(f"Вибач, але команда **{used_cmd}** не дозволена, або її не існує.\nІНФОРМАЦІЯ ДЛЯ РОЗРОБНИКА\n{command_arguments}")

		client.run(token)


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

	client = DiscordClient(level, args.console)
	client.start_bot(handle_key.get_token())


if __name__ == '__main__':
	main()