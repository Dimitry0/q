# -*- coding: utf-8 -*-
# https://severecloud.github.io/vk-keyboard/
# https://github.com/gennadis/quiz-bot
import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from random import randint, choice
from db import UsersInfo as user
import time

casino_items = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3]

def main():
    global mes_text, id
    vk_session = vk_api.VkApi(token='49a201ef83089c786c3f9d9838f4a9847096db2d293b53c0cf42ed45b8cc0244a90e3c014a65ee80a078d')
    longpoll = VkBotLongPoll(vk_session, '212404498')
    vk = vk_session.get_api()
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                text = event.message.text
                user_id = event.message.from_id
                if event.message.peer_id < 2000000000:
                    if not user.is_reg(user_id):
                        if text.lower() == "начать":
                            user.insert(user_id)
                            vk.messages.send(user_id=user_id,
                                             random_id=get_random_id(),
                                             keyboard=open('keyboard_main.json', 'r', encoding='UTF-8').read(),
                                             message="Вы зарегистирировались в чат-игре Кликер 👍🏻\nКликайте на кнопку 'Клик' и зарабатывайте деньги 💥\n\nДля просмотра топа игроков по кликам нажмите кнопку 'Топ игроков' 👥\n\nЕсли нужна помощь используйте команду 'помощь' 📣\n\nПриятной игры 😘")
                    else:
                        if text.lower() == "помощь" or text == "Помощь 📚":
                            vk.messages.send(user_id=user_id,
                                             random_id=get_random_id(),
                                             message="Чат-игра кликер - игра, суть которой заключается в наборе денег топа благодаря кликам на главную кнопку 💥\n\nЕсли у вас пропала клавиатура напишите любое сообщение, которое не похоже на команды 💡")

                        elif text.lower() == "заработать" or text == "Заработать":
                            vk.messages.send(user_id=user_id,
                                             random_id=get_random_id(),
                                             keyboard=open('keyboard_rabota.json', 'r', encoding='UTF-8').read(),
                                             message="Клавиатура отправлена")
        # клавиатура 1
                        elif text.lower() == "клик 💥" or text == "Клик 💥":
                            s = user.get_improvements(user_id)
                            g = [(s * 3) - 2, (s * 3) - 1, s * 3]
                            if user.get_cars(user_id) == 1 or user.get_cars(user_id) == 2:
                                g = [(s * 3) - 2, (s * 3) - 1, s * 3, (s * 3) - 2, (s * 3) - 1, s * 3, 8]
                            point = choice(g)
                            if point == 8:
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 message=f"Ваш автомобиль принес вам +{user.get_cars(user_id) * 35} копеек💥")
                                user.update_clicks(user_id, user.get_clicks(user_id) + user.get_cars(user_id) * 35)
                            else:
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                message=f"Вы кликнули и получили +{point} {'копейка' if point == 1 else 'копейки'} топа 💥")
                                user.update_clicks(user_id, user.get_clicks(user_id) + point)
            # клавиатура 1_1
                        elif text.lower() == "казино" or text == "Казино":
                            if user.get_stavka(user_id) > user.get_clicks(user_id):
                                mes_text = f"У вас не хватает денег\n"
                                mes_text += f"Зарабатывай на кликах\n"
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_rabota.json', 'r', encoding='UTF-8').read(),
                                                 message=mes_text)
                            else:
                                mes_text = f"Приветствуем вас в казино\n"
                                mes_text += f"НАЧАЛЬНАЯ СТАВКА 5 КОПЕЕК\n\n"
                                mes_text += f"Шанс выпадения черного = 47%\n"
                                mes_text += f"шанс выпадения красного = 47%\n"
                                mes_text += f"шанс выпадения зеленого = 5%\n"
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_casino.json', 'r', encoding='UTF-8').read(),
                                                 message=mes_text)
                        elif text.isdigit():
                            if 5 <= int(text) <= user.get_clicks(user_id):
                                user.update_stavka(user_id, int(text))
                                mes_text = f"Ставка принята✅"
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_casino.json', 'r', encoding='UTF-8').read(),
                                                 message=mes_text)
                            elif 5 >= int(text):
                                mes_text = f"Ставка слишком маленькая\n"
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_rabota.json', 'r', encoding='UTF-8').read(),
                                                 message=mes_text)
                            elif int(text) >= user.get_clicks(user_id):
                                mes_text = f"У вас не хватает денег на ставку\n"
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_rabota.json', 'r', encoding='UTF-8').read(),
                                                 message=mes_text)
                        elif text.lower() == "2x--черное" or text == "2X--черное":
                            if user.get_stavka(user_id) <= user.get_clicks(user_id):
                                cas = choice(casino_items)
                                if cas == 1:
                                    mes_text =f"Вы выиграли +{user.get_stavka(user_id)} копеек!✅\n"
                                    mes_text += f"На вашем счету {user.get_clicks(user_id) + user.get_stavka(user_id)} копеек. 👍🏻\n\n"
                                    vk.messages.send(user_id=user_id,
                                                     random_id=get_random_id(),
                                                     message=mes_text,
                                                     attachment='photo554043179_457239075')
                                    user.update_clicks(user_id, user.get_clicks(user_id) + user.get_stavka(user_id))
                                else:
                                    mes_text = f"Вы проиграли -{user.get_stavka(user_id)} копеек!❌\n"
                                    mes_text += f"На вашем счету {user.get_clicks(user_id) - user.get_stavka(user_id)} копеек. 👍🏻\n\n"
                                    mes_text += f"ВЫПАЛО:"
                                    if cas == 2:
                                        vk.messages.send(user_id=user_id,
                                                         random_id=get_random_id(),
                                                         message=mes_text,
                                                         attachment='photo554043179_457239072')
                                    elif cas == 3:
                                        vk.messages.send(user_id=user_id,
                                                         random_id=get_random_id(),
                                                         message=mes_text,
                                                         attachment='photo554043179_457239073')
                                    user.update_clicks(user_id, user.get_clicks(user_id) - user.get_stavka(user_id))
                            else:
                                mes_text = f"Недостаточно средств для ставки\n"
                                mes_text += f"Попробуйте уменьшить ставку или заработать на кликах"
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 message=mes_text)
                        elif text.lower() == "2x--красное" or text == "2X--красное":
                            if user.get_stavka(user_id) <= user.get_clicks(user_id):
                                cas = choice(casino_items)
                                if cas == 2:
                                    mes_text = f"Вы выиграли +{user.get_stavka(user_id)} копеек!✅\n"
                                    mes_text += f"На вашем счету {user.get_clicks(user_id) + user.get_stavka(user_id)} копеек. 👍🏻\n\n"
                                    vk.messages.send(user_id=user_id,
                                                     random_id=get_random_id(),
                                                     message=mes_text,
                                                     attachment='photo554043179_457239075')
                                    user.update_clicks(user_id, user.get_clicks(user_id) + user.get_stavka(user_id))
                                else:
                                    mes_text = f"Вы проиграли -{user.get_stavka(user_id)} копеек!❌\n"
                                    mes_text += f"На вашем счету {user.get_clicks(user_id) - user.get_stavka(user_id)} копеек. 👍🏻\n\n"
                                    mes_text += f"ВЫПАЛО:"
                                    if cas == 1:
                                        vk.messages.send(user_id=user_id,
                                                         random_id=get_random_id(),
                                                         message=mes_text,
                                                         attachment='photo554043179_457239071')
                                    elif cas == 3:
                                        vk.messages.send(user_id=user_id,
                                                         random_id=get_random_id(),
                                                         message=mes_text,
                                                         attachment='photo554043179_457239073')
                                    user.update_clicks(user_id, user.get_clicks(user_id) - user.get_stavka(user_id))
                            else:
                                mes_text = f"Недостаточно средств для ставки\n"
                                mes_text += f"Попробуйте уменьшить ставку или заработать на кликах"
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 message=mes_text)
                        elif text.lower() == "10x--зеленое" or text == "10X--зеленое":
                            if user.get_stavka(user_id) <= user.get_clicks(user_id):
                                cas = choice(casino_items)
                                if cas == 3:
                                    mes_text = f"Вы выиграли +{user.get_stavka(user_id) * 10} копеек!✅\n"
                                    mes_text += f"На вашем счету {user.get_clicks(user_id) + user.get_stavka(user_id) * 10} копеек. 👍🏻\n\n"
                                    vk.messages.send(user_id=user_id,
                                                     random_id=get_random_id(),
                                                     message=mes_text,
                                                     attachment='photo554043179_457239075')
                                    user.update_clicks(user_id, user.get_clicks(user_id) + user.get_stavka(user_id) * 10)
                                else:
                                    mes_text = f"Вы проиграли -{user.get_stavka(user_id)} копеек!❌\n"
                                    mes_text += f"На вашем счету {user.get_clicks(user_id) - user.get_stavka(user_id)} копеек. 👍🏻\n\n"
                                    mes_text += f"ВЫПАЛО:"
                                    if cas == 1:
                                        vk.messages.send(user_id=user_id,
                                                         random_id=get_random_id(),
                                                         message=mes_text,
                                                         attachment='photo554043179_457239071')
                                    elif cas == 2:
                                        vk.messages.send(user_id=user_id,
                                                         random_id=get_random_id(),
                                                         message=mes_text,
                                                         attachment='photo554043179_457239072')
                                    user.update_clicks(user_id, user.get_clicks(user_id) - user.get_stavka(user_id))
                            else:
                                mes_text = f"Недостаточно средств для ставки\n"
                                mes_text += f"Попробуйте уменьшить ставку или заработать на кликах"
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 message=mes_text)
                        elif text.lower() == "back" or text == "back":
                            user.update_stavka(user_id, 5)
                            vk.messages.send(user_id=user_id,
                                             random_id=get_random_id(),
                                             keyboard=open('keyboard_rabota.json', 'r', encoding='UTF-8').read(),
                                             message="Клавиатура отправлена")
                        elif text.lower() == "назад" or text == "Назад":
                            vk.messages.send(user_id=user_id,
                                             random_id=get_random_id(),
                                             keyboard=open('keyboard_main.json', 'r', encoding='UTF-8').read(),
                                             message="Клавиатура отправлена")
                        elif text == "Игроки 👥":
                            vk.messages.send(user_id=user_id,
                                             random_id=get_random_id(),
                                             keyboard=open('keyboard_players.json', 'r', encoding='UTF-8').read(),
                                             message="Клавиатура отправлена")
                        elif text.lower() == "топ игроков" or text == "Топ игроков 👥":
                            if user.rows() <= 15:
                                mes_text = "Топ игроков по состоятельности 👥\n\n"
                                top = user.get_top(user.rows())
                                for i, value in enumerate(top):
                                    data = (vk.users.get(user_ids=(value[0])))[0]
                                    name = data["first_name"]
                                    family = data["last_name"]
                                    mes_text += f"- {name} {family} [{value[1]} копеек.] 👍🏻\n"
                                mes_text += "\nКликайте больше и возвышайтесь в топы 📣"
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 message=mes_text)
                            else:
                                mes_text = "Топ-15 игроков по состоятельности 👥\n\n"
                                top = user.get_top(15)
                                for i, value in enumerate(top):
                                    data = (vk.users.get(user_ids=(value[0])))[0]
                                    name = data["first_name"]
                                    family = data["last_name"]
                                    mes_text += f"- {name} {family} [{value[1]} копеек.] 👍🏻\n"
                                mes_text += "\nКликайте больше и возвышайтесь в топы 📣"
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 message=mes_text)
                        elif text == "Авторынок":
                            mes_text = "АВТОРЫНОК👥\n\n"
                            cars = user.get_autosale(user.rows())
                            for i, value in enumerate(cars):
                                if value[2] == 1 or value[2] == 2:
                                    data = (vk.users.get(user_ids=(value[0])))[0]
                                    name = data["first_name"]
                                    family = data["last_name"]
                                    q = f'[https://vk.com/id{value[0]}|{name} {family}]'
                                    if value[2] == 1:
                                        mes_text += f"- {q} продает ВАЗ 2107👍🏻\n"
                                        mes_text += f"  Цена = {value[3]}\n"
                                    elif value[2] == 2:
                                        mes_text += f"- {q} продает Lada Granta👍🏻\n"
                                        mes_text += f"  Цена = {value[3]}\n"
                            mes_text += "\nДля того чтобы купить автомобиль отправьте ссылку на страницу любого продавца."
                            vk.messages.send(user_id=user_id,
                                             random_id=get_random_id(),
                                             message=mes_text)
                        elif text[0:15] == 'https://vk.com/':
                            s = vk_session.method('utils.resolveScreenName', {'screen_name': text[15:]})
                            id = s["object_id"]
                            kars = user.get_autosale(user.rows())
                            for i, value in enumerate(kars):
                                if value[2] == 1 or value[2] == 2:
                                    data = (vk.users.get(user_ids=(value[0])))[0]
                                    if s["object_id"] == value[0]:
                                        name = data["first_name"]
                                        family = data["last_name"]
                                        q = f'[https://vk.com/id{value[0]}|{name} {family}]'
                                        user.update_old_car(user_id, value[3])
                                        user.update_type_of_car(user_id, value[2])
                                        if value[2] == 1:
                                            mes_text = f"Вы действительно хотите купить ВАЗ 2107?\n"
                                            mes_text += f"  Цена = {value[3]}\n"
                                            mes_text += f"  Владелец: {q}"
                                        elif value[2] == 2:
                                            mes_text = f"Вы действительно хотите купить Lada Granta?\n"
                                            mes_text += f"  Цена = {value[3]}\n"
                                            mes_text += f"  Владелец: {q}"
                            vk.messages.send(user_id=user_id,
                                             random_id=get_random_id(),
                                             keyboard=open('buy_car.json', 'r', encoding='UTF-8').read(),
                                             message=mes_text)
                        elif text == 'да.':
                            if user.get_clicks(user_id) < user.get_old_car(user_id):
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_players.json', 'r', encoding='UTF-8').read(),
                                                 message='У вас не хватает денег на покупку это машины')
                            elif user.get_cars(user_id) != 0:
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_players.json', 'r', encoding='UTF-8').read(),
                                                 message='У вас уже имеется автомобиль')
                            else:
                                user.update_clicks(user_id, user.get_clicks(user_id) - user.get_old_car(user_id))
                                user.update_clicks(id, user.get_clicks(id) + user.get_old_car(user_id))
                                mes_text = f"Вы успешно приобрели автомобиль!"
                                user.update_cars(user_id, user.get_type_of_car(user_id))
                                user.update_cars(id, 0)
                                user.update_autosale(id, 0)
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_players.json', 'r', encoding='UTF-8').read(),
                                                 message=mes_text)
                                mess_text = f"Вы успешно продали автомобиль!"
                                vk.messages.send(user_id=id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_players.json', 'r', encoding='UTF-8').read(),
                                                 message=mess_text)
                        elif text == 'нет.':
                            vk.messages.send(user_id=user_id,
                                             random_id=get_random_id(),
                                             keyboard=open('keyboard_players.json', 'r', encoding='UTF-8').read(),
                                             message="Клавиатура отправлена")
                        elif text == 'назад':
                            vk.messages.send(user_id=user_id,
                                             random_id=get_random_id(),
                                             keyboard=open('keyboard_main.json', 'r', encoding='UTF-8').read(),
                                             message="Клавиатура отправлена")
                        elif text.lower() == "профиль" or text == "Профиль":
                            vk.messages.send(user_id=user_id,
                                             random_id=get_random_id(),
                                             keyboard=open('keyboard_profile.json', 'r', encoding='UTF-8').read(),
                                             message="Клавиатура отправлена")
                        elif text == "Я":
                            data = (vk.users.get(user_ids=user_id))[0]
                            name = data["first_name"]
                            family = data["last_name"]
                            if user.get_cars(user_id) == 0:
                                mes_text = f" {name} {family}, на твоем счету {user.get_clicks(user_id)} копеек\n\n"
                                mes_text += f"Мощность твоих кликов на {user.get_improvements(user_id)} уровне.\n"
                                mes_text += f"Автомобиль отсутствует."
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 message=mes_text)
                            elif user.get_cars(user_id) == 1:
                                mes_text = f" {name} {family}, на твоем счету {user.get_clicks(user_id)} копеек\n\n"
                                mes_text += f"Мощность твоих кликов на {user.get_improvements(user_id)} уровне.\n"
                                mes_text += f"Ваш автомобиль - Ваз 2107"
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 attachment='photo554043179_457239076',
                                                 message=mes_text)
                            elif user.get_cars(user_id) == 2:
                                mes_text = f" {name} {family}, на твоем счету {user.get_clicks(user_id)} копеек\n\n"
                                mes_text += f"Мощность твоих кликов на {user.get_improvements(user_id)} уровне.\n"
                                mes_text += f"Ваш автомобиль - Lada Granta"
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 attachment='photo554043179_457239077',
                                                 message=mes_text)
                        elif text.lower() == "улучшить мощность клика" or text == "Улучшить мощность клика":
                            q = user.get_improvements(user_id)
                            data = (vk.users.get(user_ids=user_id))[0]
                            name = data["first_name"]
                            family = data["last_name"]

                            mes_text = f" {name} {family}, у тебя {q} уровень клика\n\n"
                            mes_text += f"Стоимость улучшения = {q * 1000} копеек\n"
                            vk.messages.send(user_id=user_id,
                                             random_id=get_random_id(),
                                             keyboard=open('keyboard_up.json', 'r', encoding='UTF-8').read(),
                                             message=mes_text)
                        elif text.lower() == "улучшить клик" or text == "Улучшить клик":
                            q = user.get_improvements(user_id)
                            if user.get_clicks(user_id) <= q * 1000:
                                s = q * 1000 - user.get_clicks(user_id)
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_profile.json', 'r', encoding='UTF-8').read(),
                                                 message=f"Тебе не хватает {s} копеек(")
                            else:
                                user.update_clicks(user_id, user.get_clicks(user_id) - q * 1000)
                                user.update_improvements(user_id, user.get_improvements(user_id) + 1)
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_profile.json', 'r', encoding='UTF-8').read(),
                                                 message=f"Поздравляем, вы улучшили мощность клика!")
                # авто
                        elif text.lower() == "купить машину" or text == "Купить машину":
                            if user.get_cars(user_id) != 0:
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_profile.json', 'r', encoding='UTF-8').read(),
                                                 message='У вас уже есть один автомобиль')
                            else:
                                mes_text = f"Свой автомобиль будет приносить вам деньги!\n"
                                mes_text += f"Чем лучше машина, тем больше она приносит денег\n\n"
                                mes_text += f"Вы можете купить:\n"
                                mes_text += f"1) Ваз 2107 == 10000 копеек✅\n"
                                mes_text += f"2) Lada Granta == 20000 копеек✅\n\n"
                                mes_text += f"Выберите автомобиль, который хотите приобрести..."
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_two_cars.json', 'r', encoding='UTF-8').read(),
                                                 message=mes_text)
                        elif text == 'Ваз 2107' or text == 'Lada Granta':
                            if (user.get_cars(user_id) == 0 or user.get_cars(user_id) == 2) and text == 'Ваз 2107':
                                mes_text = f"Вы собираетесь приобрести Ваз 2107?"
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_car.json', 'r', encoding='UTF-8').read(),
                                                 attachment='photo554043179_457239076',
                                                 message=mes_text)
                            elif (user.get_cars(user_id) == 0 or user.get_cars(user_id) == 1) and text == "Lada Granta":
                                mes_text = f"Вы собираетесь приобрести Lada Granta?"
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_car1.json', 'r', encoding='UTF-8').read(),
                                                 attachment='photo554043179_457239077',
                                                 message=mes_text)
                            else:
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_profile.json', 'r', encoding='UTF-8').read(),
                                                 message=f"Вы уже имеете автомобиль")
                        elif text == 'Back':
                            vk.messages.send(user_id=user_id,
                                             random_id=get_random_id(),
                                             keyboard=open('keyboard_profile.json', 'r', encoding='UTF-8').read(),
                                             message=f"Клавиатура отправлена")
                        elif text == 'Да':
                            if user.get_clicks(user_id) < 10000:
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_profile.json', 'r', encoding='UTF-8').read(),
                                                 message=f"Вам не хватает {10000 - user.get_clicks(user_id)}")
                            else:
                                mes_text = f"Вы успешно приобрели автомобиль!"
                                user.update_clicks(user_id, user.get_clicks(user_id) - 10000)
                                user.update_cars(user_id, 1)
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_profile.json', 'r', encoding='UTF-8').read(),
                                                 message=mes_text)
                        elif text == 'Да.':
                            if user.get_clicks(user_id) < 20000:
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_profile.json', 'r', encoding='UTF-8').read(),
                                                 message=f"Вам не хватает {20000 - user.get_clicks(user_id)}")
                            else:
                                mes_text = f"Вы успешно приобрели автомобиль!"
                                user.update_clicks(user_id, user.get_clicks(user_id) - 20000)
                                user.update_cars(user_id, 2)
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_profile.json', 'r', encoding='UTF-8').read(),
                                                 message=mes_text)
                        elif text == "Продать машину":
                            if user.get_autosale(user_id) != 0:
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_profile.json', 'r', encoding='UTF-8').read(),
                                                 message='Вы уже продаете один автомобиль')
                            elif user.get_cars(user_id) == 1 or user.get_cars(user_id) == 2:
                                mes_text = f"Для того чтобы выставить свое авто на авторынок, введите цену\n"
                                mes_text += f'Например: "Цена-5000"'
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_profile.json', 'r', encoding='UTF-8').read(),
                                                 message=mes_text)
                            else:
                                vk.messages.send(user_id=user_id,
                                                 random_id=get_random_id(),
                                                 keyboard=open('keyboard_profile.json', 'r', encoding='UTF-8').read(),
                                                 message="У вас отсутствует автомобиль")
                        elif text[0:5] == 'Цена-':
                            cost = int(text[5:])
                            user.update_cost_of_car(user_id, cost)
                            mes_text = f"Вы действительно хотите продать машину за {cost} копеек"
                            vk.messages.send(user_id=user_id,
                                             random_id=get_random_id(),
                                             keyboard=open('sold_car.json', 'r', encoding='UTF-8').read(),
                                             message=mes_text)
                        elif text == 'YES':
                            user.update_autosale(user_id, user.get_cars(user_id))
                            user.update_cars(user_id, 0)
                            mes_text = 'Вы успешно выставили свое авто на авторынок'
                            vk.messages.send(user_id=user_id,
                                             random_id=get_random_id(),
                                             keyboard=open('keyboard_profile.json', 'r', encoding='UTF-8').read(),
                                             message=mes_text)
                        elif text == 'NO':
                            vk.messages.send(user_id=user_id,
                                             random_id=get_random_id(),
                                             keyboard=open('keyboard_profile.json', 'r', encoding='UTF-8').read(),
                                             message='Клавиатура отправлена')
                        elif text.lower() == "назад." or text == "Назад.":
                            vk.messages.send(user_id=user_id,
                                             random_id=get_random_id(),
                                             keyboard=open('keyboard_main.json', 'r', encoding='UTF-8').read(),
                                             message="Клавиатура отправлена")
                        else:
                            user.update_stavka(user_id, 5)
                            vk.messages.send(user_id=user_id,
                                             random_id=get_random_id(),
                                             keyboard=open('keyboard_main.json', 'r', encoding='UTF-8').read(),
                                             message="Ты по-моему перепутал\n\n\nКлавиатура отправлена",
                                             attachment='photo554043179_457239074')

    except requests.exceptions.ReadTimeout:
        print("--------------- [ СЕТЕВАЯ ОШИБКА ] ---------------")
        print("Переподключение к серверам...")
        time.sleep(3)


if __name__ == '__main__':
    main()