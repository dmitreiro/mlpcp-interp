import telebot
import configparser
import subprocess
from src import (
    mesh_interp,
    reverse_interp,
    training,
    testing
)

# reading config file and accessing variables
config = configparser.ConfigParser()
try:
    config.read(r"config/config.ini")
    TOKEN = config.get("Telegram", "token")
    CHAT_ID = config.get("Telegram", "chat_id")
except Exception as e:
    print(f"Error reading configuration file: {e}")
    exit(1)

def ntfy(msg: str) -> None:
    """
    Sends `msg` string to Telegram bot defined with `TOKEN` and `CHAT_ID` global variables.
    """
    # starting bot
    bot = telebot.TeleBot(TOKEN)

    try:
        bot.send_message(CHAT_ID, msg)
    except Exception as e:
        print(f"Failed to send Telegram notification: {e}")


if __name__ == "__main__":
    ntfy("Starting code")

    ntfy("Running interpolation")
    status = mesh_interp.main()
    if status == 1:
        ntfy("Couldn't execute interpolation... leaving")
        exit(1)

    ntfy("Running reverse interpolation")
    status = reverse_interp.main()
    if status == 1:
        ntfy("Couldn't execute reverse interpolation")
    
    ntfy("Training")
    status = training.main()
    if status == 1:
        ntfy("Couldn't execute training... leaving")
        exit(1)

    ntfy("Testing")
    status = testing.main()
    if status == 1:
        ntfy("Couldn't execute testing... leaving")
        exit(1)

    ntfy("Code finished!")
    exit(0)
    