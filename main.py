import telebot
import configparser
import subprocess

# Reading configuration file
config = configparser.ConfigParser()
config.read(r"config/config.ini")

# Accessing variables
TOKEN = config.get("Telegram", "token")
CHAT_ID = config.get("Telegram", "chat_id")

def notify(msg):
    # Initialize the bot
    bot = telebot.TeleBot(TOKEN)

    try:
        bot.send_message(CHAT_ID, msg)
    except Exception as e:
        print(f"Failed to send notification: {e}")


if __name__ == "__main__":
    notify("Starting code")
    notify("Running interpolation")
    subprocess.run(["python", "src/mesh_interp.py"])
    notify("Running reverse interpolation")
    subprocess.run(["python", "src/reverse_interp.py"])
    notify("Training")
    subprocess.run(["python", "src/training.py"])
    notify("Testing")
    subprocess.run(["python", "src/testing.py"])
    # subprocess.run(["python", "tools/inter_plots.py"])
    # subprocess.run(["python", "src/pred_params_plots.py"])
    # subprocess.run(["python", "src/test_plots.py"])
    notify("Code finished!")
    