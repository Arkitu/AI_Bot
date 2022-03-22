from cmath import log
from dotenv import load_dotenv
import discord, os, json
from transformers import pipeline, set_seed

#Récupérer les clés d'API
load_dotenv("api_keys.env")

#Connecter le bot discord
bot = discord.Client()

#Démarre l'IA
generator = pipeline('text-generation')
set_seed(42)

with open("chat_logs.json", "r") as fp:
    chat_logs = json.loads(fp.read())

def save():
    with open("chat_logs.json", "w") as fp:
        fp.write(json.dumps(chat_logs))

def ask(question, message):
    global chat_logs
    channel_id = str(message.channel.id)
    user = message.author
    if channel_id not in chat_logs.keys():
        chat_logs[channel_id] = chat_logs["default_version"]
    while len(chat_logs[channel_id]["content"]) > 500:
        array = chat_logs[channel_id]["content"].split("\n")
        array.pop(0)
        chat_logs[channel_id]["content"] = "\n".join(array)
    prompt = f'{chat_logs[channel_id]["content"]}{user.name}: {question}\nAI:'
    result = generator(prompt, max_length=1000)
    answer = result[0]["generated_text"][len(prompt):-1].split("AI:")[0]
    chat_logs[channel_id]["content"] = prompt + answer + '\n'
    save()
    return answer
    
@bot.event
async def on_ready():
    print("Bot logged")

@bot.event
async def on_message(message):
    if message.author != bot.user:
        if bot.user.mentioned_in(message) or message.channel.id == 954819888176828426:
            question = message.content.replace(f'<@!{str(bot.user.id)}>', "")
            answer = ask(question, message)
            await message.channel.send(answer)
            print("Message sended")

bot.run(os.environ.get('DISCORD_KEY'))