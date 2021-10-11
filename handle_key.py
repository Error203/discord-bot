import pyAesCrypt
import getpass
import hashlib
from os import path as file_path
import argparse
import qlogger
import sys
import io


parser = argparse.ArgumentParser(
					description="WebDog network tool. (netcat analog).",
					epilog="Simple use. Can be used without arguments.",
					)
parser.add_argument("-v", "--verbose", action="store_true", help="more detailed information about script steps.")

args = parser.parse_args()

if args.verbose:
	level = qlogger.logging.DEBUG
else:
	level = qlogger.logging.INFO

log = qlogger.Logger(directory_name="crypto logs", level=level).get_logger("key_handler")

passphrase_secret = "passphrase.secret.hash"
ciphered_token = "ciphered.token"

log.debug(f"passphrase path: {passphrase_secret}")
log.debug(f"token path: {ciphered_token}")


def get_token():
	try:
		password = getpass.getpass()
		password_hash = hashlib.sha256(bytes(password, "utf-8")).hexdigest()
		byte_ciphered_token = io.BytesIO()
		byte_deciphered_token = io.BytesIO()
		buffer_size = 64 * 1024

		if password_hash == "37a6760fa43caf5b1ea02f22251b1456c39e060a4918ba3e963dbde336f16148":
			log.info("started reconfiguring protocol")

			with open(ciphered_token, "w") as file:
				file.write("")
				log.debug("cleared token file")
				# token = getpass.getpass(prompt="Token: ", stream=sys.std)
				token = input("Token: ").encode("utf-8")

			while True:
				l_password = getpass.getpass()
				password_hash = (
				hashlib
				.sha256(bytes(l_password, "utf-8"))
				.hexdigest()
				)
				if password_hash == "37a6760fa43caf5b1ea02f22251b1456c39e060a4918ba3e963dbde336f16148":
					log.info("password can't be a secret")
				else:
					with open(passphrase_secret, "w") as file:
						file.write(password_hash)
						log.info("hash is stored successfully")
						byte_token = io.BytesIO(token)
						pyAesCrypt.encryptStream(byte_token, byte_ciphered_token, l_password, buffer_size)
						# log.debug(l_password)

						with open(ciphered_token, "wb") as file:
							file.write(byte_ciphered_token.getvalue())

						log.info("token is stored and protected successfully")

						return token.decode("utf-8")
						break


		else:
			with open(passphrase_secret, "r") as file:
				file_content = file.read()

				if not file_content:
					log.warning("file is empty, use a secret to write hash and token")

					exit(0)

				file_password_hash = file_content
				if password_hash != file_password_hash:
					log.error("couldn't verify hashes, file may be broken, use a secret")

					exit(0)
				else:
					log.info("hashes successfully verified")

					with open(ciphered_token, "rb") as file:
						raw_byte_ciphered_token = io.BytesIO(file.read())
						crypt_len = len(raw_byte_ciphered_token.getvalue())
						raw_byte_ciphered_token.seek(0)
						# log.debug(password)
						# log.debug(crypt_len)
						# log.debug(raw_byte_ciphered_token.getvalue())
						pyAesCrypt.decryptStream(raw_byte_ciphered_token, byte_deciphered_token, password, buffer_size, crypt_len)

						return byte_deciphered_token.getvalue().decode("utf-8")


	except FileNotFoundError:
		log.warning("secret file is not detected")
		with open(passphrase_secret, "w") as file:
			file.write("")

	except Exception as e:
		log.exception(e)


if __name__ == '__main__':
	main()