from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")

STUPIDWALLET_TOKEN = env.str("STUPIDWALLET_TOKEN")

DEPOSIT_MINIMUM = env.int("DEPOSIT_MINIMUM")
DEPOSIT_MAXIMUM = env.int("DEPOSIT_MAXIMUM")

CUBE_XP = env.int("CUBE_XP")
RULET_XP = env.int("RULET_XP")
CRASH_XP = env.int("CRASH_XP")

INVITE_REWARD_WAV = env.int("INVITE_REWARD_WAV")
INVITE_REWARD_XP = env.float("INVITE_REWARD_XP")

BOT_NAME = env.str("BOT_NAME")

ADMIN = env.int("ADMIN")
