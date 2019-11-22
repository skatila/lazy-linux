#!/usr/bin/env python3
"""
	Run google chrome with specified profile
"""
__author__ = "Sabin Katila"
__license__ = "GPLv3"
__copyright__ = "Copyright(c) 2018 Sabin Katila"

import sys
import os
import subprocess
import datetime
import logging
import io
import json
from json.decoder import JSONDecodeError
log = logging.getLogger("pygchrome")

SOCKS_VERSION = 5
SOCKS_SERVER = "socks5://localhost:9050"
PASSWORD_STORAGE_CHOICES = ["gnome", "basic", "kwallet", "default"]
TOR_DIR = ["torbrowse", "tor", "tor1", "tor2"]
O_DIR = ["reg", "work", "fun"]
SECURE_PROFILES = []
CHROME_DIR = os.path.join(os.path.expanduser("~"), "chrome")
CHROME_STABLE = "google-chrome-stable"  # default chrome
CHROME_UNSTABLE = "google-chrome-unstable"
DISK_CACHE_DIR = "/dev/shm"
DEFAULT_HOST_RESOLVER = "--host-resolver-rules=\"MAP * ~NOTFOUND , EXCLUDE localhost\""

DEFAULT_CONFIG = {
	'SECURE_PROFILES': ['shera', 'bo', 'c'],
	'CHROME_DIR': '~/chrome',
	'CHROME_STABLE': 'google-chrome-stable',
	'CHROME_UNSTABLE': 'google-chrome-unstable',
	'DISK_CACHE_DIR': '/dev/shm',
	'TOR_DIR': ['torbrowse', 'tor', 'tor1', 'tor2'],
	'SOCKS_SERVER': 'socks5://localhost:9050'
}


class ConfigHandle(object):
	@classmethod
	def get_config_dir(cls, dry_run=False):
		"""place holder"""
		log.debug("%s.get_config_dir, dry_run:%s", cls.__name__, dry_run)
		try:
			from xdg.BaseDirectory import xdg_config_home as confighome
			config_dir = os.path.join(confighome, "pygchrome")
		except ModuleNotFoundError:
			log.error("System lacks xdg module, trying to brute-force")
			confighome = os.path.join(os.path.expanduser("~"), ".config")
			config_dir = os.path.join(confighome, "pygchrome")
		if os.path.isfile(confighome):
			log.critical(
				"%s appears to be a file - it should not be possible ABORT!!!",
				confighome
			)
			sys.exit(1)

		dir_to_create = []
		if os.path.isdir(confighome):
			if not os.path.isdir(config_dir):
				dir_to_create.append(config_dir)
		else:
			dir_to_create.append(confighome)
			dir_to_create.append(config_dir)
		config_file = os.path.join(config_dir, "pygchrome.json")

		if dry_run:
			log.info("DRY RUN (get_config_dir) would create %s", dir_to_create)
		else:
			list(map(create_dir, dir_to_create))
		log.debug("config_dir: %s config_file: %s", config_dir, config_file)
		return config_dir, config_file

	@classmethod
	def write_config(cls, config_file=None, dry_run=False):
		if config_file is None:
			log.debug("(write_config) -> get_config_dir")
			config_dir, config_file = cls.get_config_dir(dry_run=dry_run)
		if dry_run:
			log.info("DRY RUN (write_config) would write %s", config_file)
			return True
		with io.open(config_file, "w") as fp:
			json.dump(DEFAULT_CONFIG, fp, indent=4)
			return True

	@classmethod
	def read_config(cls, config_file=None, dry_run=False):
		# load config
		log.debug(
			"(read_config) with config_file %s, dry_run %s", config_file,
			dry_run
		)
		if config_file is None:
			config_dir, config_file = cls.get_config_dir(dry_run=dry_run)
		try:
			with io.open(config_file, "r") as fp:
				try:
					myconfig = json.load(fp)
				except JSONDecodeError as e:
					log.info("Problem with your config file %s", config_file)
					log.info("Use -w flag to overwrite config file")
					raise e
		except FileNotFoundError:
			log.error(
				"Since there was no config file (possibly first run), we will generate a new one"
			)
			cls.write_config(dry_run=dry_run)
			return DEFAULT_CONFIG
		# override default config
		return myconfig


def run_chrome(chromeargs, dry_run=False):
	"""Launch chrome"""
	if dry_run:
		log.info(chromeargs)
		return 0
	log.info(chromeargs)
	runner = subprocess.run(chromeargs)
	return runner.returncode


def google_chrome(
	user_dir, use_proxy=False, tor=False, dry_run=False, **kwargs
):
	"""Run google chrome
	:param user_dir: User profile directory
	:param use_proxy: True if using tor or another proxy
	:param password: defaults to basic
	:param disk_cache_dir: defaults to /dev/shm; used only when using tor proxy
	"""
	chrome_args = []
	chrome_binary = kwargs.get("chrome", CHROME_STABLE)
	chrome_args.append(chrome_binary)
	password = kwargs.get("password", "basic")
	disk_cache_dir = kwargs.get("disk_cache_dir", False)
	remaining_args = ' '.join(kwargs.get("all_args", [""]))
	if password != "default":
		chrome_args.append("--password-store={}".format(password))
	chrome_args.append("--user-data-dir={}".format(user_dir))

	if tor:
		log.info("Using tor")
		disk_cache_dir = kwargs.get("disk_cache_dir", DISK_CACHE_DIR)
		chrome_args.append("--disk-cache-dir={}".format(disk_cache_dir))
		if not use_proxy:
			log.error("Forcing use_proxy to True; Using tor means using proxy")
			use_proxy = True

	if use_proxy:
		log.info("Setting proxy")
		log.info(SOCKS_SERVER)
		proxy_server = kwargs.get("proxy_server", SOCKS_SERVER)
		chrome_args.append("--proxy-server={}".format(proxy_server))

	if remaining_args:
		chrome_args.append("{}".format(remaining_args))

	log.debug(chrome_args)
	log.info("%s", " ".join(chrome_args))
	log.info(
		"\n\nStarting google chrome %s\n",
		datetime.datetime.now().strftime("%b %d %T")
	)
	exit_code = run_chrome(chrome_args, dry_run)
	log.info(
		"\n\nEnded google chrome %s",
		datetime.datetime.now().strftime("%b %d %T")
	)
	sys.exit(exit_code)


def opts():
	"""Defining options"""
	import argparse
	parser = argparse.ArgumentParser()
	mutual_excl_group = parser.add_mutually_exclusive_group()
	mutual_excl_group.add_argument('--foo', action='store_true')

	mutual_excl_group.add_argument(
		"-l",
		"--list-profiles",
		dest="list",
		action="store_true",
		default=False,
		help="List available chrome profiles in CHROME_DIR"
	)
	mutual_excl_group.add_argument(
		"user_profile",
		nargs="*",
		default=[],
		help=
		"User profile to use; Should exist under CHROME_DIR/?; If not, specify -c"
	)
	parser.add_argument(
		"-t", "--enable-tor", action="store_true", dest="tor", help="Use tor"
	)
	parser.add_argument(
		"-a",
		"--alt-profile-dir",
		action="store",
		dest="alt_profile",
		default=None,
		help="Profile located somewhere other than CHROME_DIR"
	)
	parser.add_argument(
		"-c",
		"--create-dir",
		action="store_true",
		help="Create new user directory under CHROME_DIR (or alt dir)"
	)
	parser.add_argument(
		"-p",
		"--password-storage",
		action="store",
		# This should be basic but is set to None in order to enforce security
		default=None,
		dest="password",
		choices=PASSWORD_STORAGE_CHOICES,
		help=
		"""Password storage system: basic, gnome, kwallet, default; Specifying default causes chrome to use whatever password system your desktop environment prefers. The default enforced by this program however is basic"""
	)
	parser.add_argument(
		"--no-prefetch",
		action="store_true",
		dest="host_resolver_rules",
		default=False,
		help="""
			Some traffic such as DNS prefetching will not go through proxy server and as such, to prevent browser from doing a local resolution this flag will have to be added. This will simply pass on: --host-resolver-rules="MAP * ~NOTFOUND , EXCLUDE localhost" to google-chrome"""
	)

	parser.add_argument(
		"--use-unstable",
		action="store_true",
		default=False,
		dest="use_unstable",
		help="Use google-chrome-unstable"
	)

	parser.add_argument(
		"-v", "--verbose", action="count", help="Verbosity level"
	)
	#parser.add_argument(
	#	"remaining", nargs="*", help="Optional chrome specific arguments"
	#)


	parser.add_argument(
		"-w",
		"--over-write-config",
		dest="write_config",
		default=False,
		action="store_true",
		help="Overwrite configuration"
	)

	parser.add_argument(
		"-s",
		"--skip-config",
		dest="skip_config",
		action="store_true",
		default=False,
		help="Skip parsing/writing config file"
	)

	parser.add_argument(
		"-n",
		"--dry-run",
		action="store_true",
		default=False,
		help="Dry run - instead of launching chrome, just build arg and exit"
	)
	args = parser.parse_args()
	# I need the elements in mutual_excl_group to
	# satisfy XOR constraint, but argparse has no facility
	# ONLY one should be filled
	if  ((args.list is False) and (len(args.user_profile) < 1)):
		parser.error("Not enough arguments!!!\n\nUse -l to list available profiles")
	return args


def create_dir(dpath):
	"""Create directory given my dpath"""
	log.info("CREATING DIR: %s", dpath)
	os.makedirs(dpath)

def decor_dry(dry_run=False):
	if dry_run:
		log.debug("Setting dry run")
		def wrap(f):
			def wrapped_f(*args, **kw):
				log.info("%s with args %s and kwargs %s", f.__name__, args, kw)
				return False
			return wrapped_f
	else:
		log.debug("Function is really going to run")
		def wrap(f):
			def wrapped_f(*args, **kw):
				log.info("%s with args %s and kwargs %s", f.__name__, args, kw)
				return f(*args, **kw)
			return wrapped_f
	return wrap


def main():
	"""main"""
	options = opts()
	
	if options.verbose is None:
		logging.basicConfig(level=logging.WARNING)
		sys.tracebacklimit = 0
	else:
		if options.verbose == 1:
			sys.tracebacklimit = 0
			logging.basicConfig(level=logging.INFO)
		else:
			logging.basicConfig(level=logging.DEBUG)
	if not options.skip_config:
		if options.write_config:
			log.debug("Overwriting config file")
			ConfigHandle.write_config(dry_run=options.dry_run)
		# if you are doing a dry run with a bad config file
		# a jsondecode error will occur here
		my_defaults = ConfigHandle.read_config(
			dry_run=options.dry_run
		)  #myconfig()
	else:
		my_defaults = DEFAULT_CONFIG
	all_args = []
	# defining some variables - can be overriden by options
	chrome = my_defaults['CHROME_STABLE']
	tor = False
	profile_dir = my_defaults['CHROME_DIR']
	password = "basic"
	if options.host_resolver_rules:
		log.info("No prefetch")
		all_args.append(DEFAULT_HOST_RESOLVER)
	if len(options.user_profile) > 1:
		all_args.extend(options.user_profile[1:])
	log.debug(my_defaults)

	if options.alt_profile:
		log.debug("options.alt_profile %s", options.alt_profile)
		# using alternative profile dir instead of CHROME_DIR
		profile_dir = options.alt_profile
	profile_dir = os.path.expanduser(profile_dir)

	if not os.path.isdir(profile_dir):
		log.critical("%s %s",
			"The alternative profile storage directory does not exist.",
			"You need to create it")
		raise FileNotFoundError

	if options.list:
		log.debug("listing stuff in profile dir %s", profile_dir)
		if os.path.isdir(profile_dir):
			import textwrap
			if os.isatty(0):
				print("\nAvailable profiles in {} are\n".format(profile_dir))
				profiles = os.listdir(profile_dir)
				rows, cols = os.popen('stty size', 'r').read().split()
				cols = int(cols)/2
				print(textwrap.fill("\t".join(profiles), width=cols))
			else:
				print("\t".join(profiles))
			sys.exit(0)
		else:
			log.error("You want a listing done but %s has issues", profile_dir)
			sys.exit(1)

	user_profile = os.path.join(profile_dir, options.user_profile[0])
	log.info(user_profile)

	if not os.path.isdir(user_profile):
		if options.create_dir:
			log.info(
				"%s %s", "The directory does not exist but since you have",
				"specified --create flag, we are going to create it for you"
			)
			# decor_dry is supposed to be used as a function decoration
			# but, this is how a decoration works at it's core
			# and I don't really feel like messing around anymore
			decor_dry(dry_run=options.dry_run)(create_dir)(user_profile)
		else:
			log.critical(
				"The user profile directory %s does not exist\n\nEXITING",
				user_profile
			)
			raise FileNotFoundError

	if options.use_unstable:
		chrome = my_defaults['CHROME_UNSTABLE']

	if options.password is None:
		log.debug("options.password is None")
		log.debug("options.user_profile[0] %s", options.user_profile[0])
		log.debug(my_defaults['SECURE_PROFILES'])
		if options.user_profile[0] in my_defaults['SECURE_PROFILES']:
			# Secure profile that cannot be using basic password properties
			log.debug("Setting password to gnome")
			password = "gnome"
	else:
		password = options.password
	# boom boom
	google_chrome(
		user_profile,
		tor=options.tor,
		chrome=chrome,
		password=password,
		dry_run=options.dry_run,
		all_args=all_args
	)


if __name__ == "__main__":
	main()
