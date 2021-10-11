import discord
import qlogger
import argparse
import handle_key


class DiscordClient:


	def __init__(self, level, console):

		self.log = qlogger.Logger("bot logs", level=level).get_logger("bot")
		self.dev_id = 407598463010734080


	def start_bot(self, token):
		client = discord.Client()

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
			command_prefix = "$$"
			command = message.content
			allowed_commands = ["dada", "help", "info"]
			prefixed_allowed_commands = [command_prefix]

			for cmd in allowed_commands:
				prefixed_allowed_commands.append(command_prefix + cmd)

			handled_message = message.content.split(" ")
			used_cmd = handled_message[0]
			command_arguments = handled_message[1:len(handled_message)]

			if command.lower().startswith(command_prefix):
				self.log.debug(f"{message.author.id} said# {message.content}")
			
				if message.author != client.user:
					await message.delete()
				
				if command.lower() == command_prefix + "dada":
					await message.channel.send("Еге-ж...")

				if command.lower() == command_prefix + "help" or command.lower() == command_prefix + "info":
					mention_dev_name = f"<@!{self.dev_id}>"
					user_id = message.author.id
					mention_user_name = f"<@!{user_id}>"
					status = "тестер"

					if user_id == self.dev_id:
						status = "розробник"

					if user_id == self.guild_owner_id:
						status = "засновник серверу"

					await message.channel.send(f"За допомогою звертайтеся до {mention_dev_name} або відправивши **$$**(два символа долару).\n" + \
						f"Ваш псевдонім на сервері: {mention_user_name}\nВаш ID: {user_id}\nВаш статус: {status}.")

				if command.lower() == command_prefix + "clear":
					pass

				if command.lower() == command_prefix:
					await message.channel.send("Дозволені команди:\n\n{0}".format(f"\n".join(prefixed_allowed_commands)))

				# message.content.lower() not in allowed_commands:
				if command.lower() not in prefixed_allowed_commands:
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