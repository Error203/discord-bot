from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import Salsa20
import getpass
import hashlib
from os import path as file_path
import argparse
import qlogger


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


def main():
	try:
		password_hash = hashlib.sha256(bytes(getpass.getpass(), "utf-8")).hexdigest()

		if password_hash == "37a6760fa43caf5b1ea02f22251b1456c39e060a4918ba3e963dbde336f16148":
			log.info("started reconfiguring protocol")

			with open(ciphered_token, "w") as file:
				file.write("")
				log.debug("cleared token file")

			while True:
				password_hash = (
				hashlib
				.sha256(bytes(getpass.getpass(), "utf-8"))
				.hexdigest()
				)
				if password_hash == "37a6760fa43caf5b1ea02f22251b1456c39e060a4918ba3e963dbde336f16148":
					log.info("password can't be a secret")
				else:
					with open(passphrase_secret, "w") as file:
						file.write(password_hash)
						log.info("hash is stored successfully")

						break

		else:
			with open(passphrase_secret, "r") as file:
				file_content = file.read()

				if not file_content:
					log.warning("file is empty, use a secret to write hash")

					exit(0)

				file_password_hash = file_content
				if password_hash != file_password_hash:
					log.error("couldn't verify hashes, file may be broken, use a secret")
				else:
					log.info("hashes successfully verified")

	except FileNotFoundError:
		log.warning("secret file is not detected")
		with open(passphrase_secret, "w") as file:
			file.write("")

	except Exception as e:
		log.exception(e)


if __name__ == '__main__':
	main()