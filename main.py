import telebot
from telebot import TeleBot, types
import random

# ПЕРЕМЕННЫЕ
commands = """/coin - подбрасывает монетку и на рандом выводит: "Орел" или "Решка"
/number - выводит рандомное число от 1 до 10000

/cuefa - игра в камень-ножницы-бумага
/secret_number - игра в угадай число
/tasks - математические задачки
/dice - подбрасывает кубик и выводит рандомное число от 1 до 6

/help - помощь по использованию бота
/commands - список команд"""

user_tasks = {}

choices = ['камень', 'ножницы', 'бумага']
playing_cuefa = set()

API_TOKEN = 'my token'
bot = telebot.TeleBot(API_TOKEN)

secret_number = None
attempts = 0

# СТАРТ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """
Приветствую, меня зовут FrozFunBot, я развлекательный бот.
Список моих команд под командой /commands
""")


# ПОМОЩЬ
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, """
Список команд - /commands
Связь с владельцем - @user
Нашли ошибку? Пишите - @user
""")


# ОРЕЛ И РЕШКА
@bot.message_handler(commands=['coin'])
def send_coin(message):
    bot.reply_to(message, random.choice(['Орел', 'Решка']))
    bot.reply_to(message, "Играть еще раз? - /coin")


# РАНДОМ ЧИСЛО
@bot.message_handler(commands=['number'])
def send_number(message):
    random_number = random.randint(0, 10000)
    bot.reply_to(message, random_number)


# КАМЕНЬ НОЖНИЦЫ БУМАГА
@bot.message_handler(commands=['cuefa'])
def start_game(message):
    bot.send_message(message.chat.id, "Давай сыграем в 'Камень, ножницы, бумага'! Напиши свой выбор: камень, ножницы или бумага.")

@bot.message_handler(func=lambda message: message.text.lower() in choices)
def play_game(message):
    user_choice = message.text.lower()
    bot_choice = random.choice(choices)
    result = determine_winner(user_choice, bot_choice)

    response = f"Ты выбрал: {user_choice}\nБот выбрал: {bot_choice}\n{result}"
    bot.send_message(message.chat.id, response)

def determine_winner(user, bot):
    if user == bot:
        return "⚔️ Ничья! Если хочешь играть дальше, то выбери снова."
    elif (user == 'камень' and bot == 'ножницы') or \
         (user == 'ножницы' and bot == 'бумага') or \
         (user == 'бумага' and bot == 'камень'):
        return "🎉Ты выиграл! Если хочешь играть дальше, то выбери снова."
    else:
        return "☹️Ты проиграл! Если хочешь играть дальше, то выбери снова."""
    

# ЗАДАЧКИ
def generate_task():
    num1 = random.randint(1, 10) # первое число
    num2 = random.randint(1, 10) #второе число
    operation = random.choice(['+', '-', '*'])
    if operation == '+':
        answer = num1 + num2
    elif operation == '-':
        answer = num1 - num2
    else:
        answer = num1 * num2
    task = f"{num1} {operation} {num2} = ?"
    return task, answer

@bot.message_handler(commands=['tasks'])
def start_game(message):
    task, answer = generate_task()
    user_tasks[message.chat.id] = answer 
    bot.send_message(message.chat.id, f"Решите задачу: {task}")

@bot.message_handler(func=lambda message: message.chat.id in user_tasks)
def check_answer(message):
    correct_answer = user_tasks[message.chat.id]
    try:
        user_answer = int(message.text)
        if user_answer == correct_answer:
            bot.send_message(message.chat.id, "🎉Это правильный ответ! Поздравляю! Играть еще раз? - /tasks")
            del user_tasks[message.chat.id] 
        else:
            bot.send_message(message.chat.id, "☹️Неправильно, попробуйте еще раз!")
    
    except ValueError:
        bot.send_message(message.chat.id, "Введите число.")

@bot.message_handler(commands=['stop'])
def stop_game(message):
    if message.chat.id in user_tasks:
        del user_tasks[message.chat.id]
        bot.send_message(message.chat.id, "Игра остановлена."
        "Играть еще раз? - /tasks")


# ИГРА "УГАДАЙ ЧИСЛО"
@bot.message_handler(commands=['secret_number'])
def start_secret_number_game(message):
    global secret_number, attempts
    secret_number = random.randint(1, 100)  # загадать число
    attempts = 0
    bot.send_message(message.chat.id, "Я загадал число от 1 до 100, попробуй угадать!")


@bot.message_handler(func=lambda message: secret_number is not None and message.text.isdigit())
def guess_number(message):
    global attempts
    guess = int(message.text)
    attempts += 1

    if guess < secret_number:
        bot.send_message(message.chat.id, "➕Больше! Попробуй еще раз.")
    elif guess > secret_number:
        bot.send_message(message.chat.id, "➖Меньше! Попробуй еще раз.")
    else:
        bot.send_message(message.chat.id, f"🎉Поздравляю! Ты угадал число {secret_number} за {attempts} попыток! Играть еще раз? - /secret_number")
        reset_game()  # cброс игры


def reset_game():
    global secret_number, attempts
    secret_number = None
    attempts = 0


# КУБИК
@bot.message_handler(commands=['dice'])
def send_number(message):
    random_number = random.randint(1, 6)
    bot.reply_to(message, f"🎲Выпало число {random_number}.  Играть еще раз? - /dice")


# СПИСОК КОМАНД
@bot.message_handler(commands=['commands'])
def send_commands(message):
    bot.reply_to(message, commands)


if __name__ == '__main__':
    print("Бот запущен")  # соо при запуске
    bot.polling(none_stop=True)
