import discord
import qlogger
import argparse


class DiscordClient:


	def __init__(self, level):

		self.log = qlogger.Logger("bot logs", level=level).get_logger("bot")
		self.log.setLevel(level)
		self.dev_id = 407598463010734080


	def start_bot(self, token):
		client = discord.Client()

		@client.event
		async def on_ready():
			print(f"Logged as {client.user}")

		@client.event
		async def on_message(message):
			command_prefix = "$$"
			command = message.content
			allowed_commands = ["dada", "help"]
			prefixed_allowed_commands = [command_prefix]

			for cmd in allowed_commands:
				prefixed_allowed_commands.append(command_prefix + cmd)

			if command.lower().startswith(command_prefix):
			
				if message.author != client.user:
					await message.delete()
				
				if command.lower() == command_prefix + "dada":
					await message.channel.send("Еге-ж...")

				if command.lower() == command_prefix + "help":
					mention_dev_name = f"<@!{self.dev_id}>"
					user_id = message.author.id
					mention_user_name = f"<@!{user_id}>"
					await message.channel.send(f"За допомогою звертайтеся до {mention_dev_name} або за допомогою **$$**(двох символів долара).\n" + \
						f"Ваш статус: {mention_user_name}\nВаш ID: {user_id}")

				if command.lower()

				if command.lower() == command_prefix:
					await message.channel.send("Дозволені команди:\n\n{0}".format(f"\n".join(prefixed_allowed_commands)))

				# message.content.lower() not in allowed_commands:
				if command.lower() not in prefixed_allowed_commands:
					await message.channel.send(f"Вибач, але команда **{message.content}** не дозволена, або її не існує.")

		client.run(token)


def main():
	parser = argparse.ArgumentParser(
					description="WebDog network tool. (netcat analog).",
					epilog="Simple use. Can be used without arguments.",
					)
	parser.add_argument("-v", "--verbose", action="store_true", help="more detailed information about script steps.")

	args = parser.parse_args()

	if args.verbose:
		level = qlogger.logging.DEBUG
	else:
		level = qlogger.logging.CRITICAL

	client = DiscordClient(level)
	client.start_bot("NTc3OTQ2NjQxNjAwODcyNDg3.XNscwQ.rnLgNogxAE1Gxe96sKts2Ya6GjE")


if __name__ == '__main__':
	main()