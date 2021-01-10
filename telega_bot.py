import time
import datetime as dt
import json
import requests
import confing
import db

base_url_str = 'https://api.telegram.org/bot{0}/{1}'
current_offset = 0
timeout = 100
chat_id = '-1001383165413'
add_user_db = {
    "Должность": '',
    "Фамилия": '',
    "Имя": '',
    "Отчество": '',
    "Адрес": '',
    "Телефон": '',
    "Почта": ''
}


def show_keyboard(admin):
    if admin in admin_list:
        requests.get(
            base_url_str.format(
                confing.Token,
                'sendMessage'
            ),
            params={
                'chat_id': message['chat']['id'],
                'text': f'Что будем делать, {admin}?',
                'reply_markup': json.dumps({
                    'one_time_keyboard': True,
                    'keyboard': [
                        [
                            {
                                'text': 'Добавить'
                            }
                        ],
                        [
                            {
                                'text': 'Редактировать'
                            },
                            {
                                'text': 'Удалить'
                            }
                        ]
                    ]
                })
            })
    else:
        requests.get(base_url_str.format(
            confing.Token,
            'sendMessage') + '?chat_id=' + chat_id + f'&text=•У вас,{admin},недостаточно прав!')


def search_user(message):
    worker = db.read({'Должность': message})
    if worker is not None:
        text = ''
        for dic in worker:
            if dic != '_id':
                text += f'{dic} : {worker[dic]}\n'
        requests.get(base_url_str.format(
            confing.Token,
            'sendMessage') + '?chat_id=' + chat_id + '&text=' + text)
    if worker is None:
        requests.get(base_url_str.format(
            confing.Token,
            'sendMessage') + '?chat_id=' + chat_id + '&text=•Пользователь не найден!')


def add_user(current_offset1, admin):
    for key in add_user_db:
        requests.get(base_url_str.format(
            confing.Token,
            'sendMessage') + '?chat_id=' + chat_id + f'&text=•Введите {key}!')
        flag = True
        while flag:
            res = requests.get(
                base_url_str.format(
                    confing.Token,
                    'getUpdates'
                ),
                params={
                    'timeout': timeout,
                    'offset': current_offset1
                }
            ).json()
            if res['ok']:
                for message in res['result']:
                    current_offset1 = message['update_id'] + 1
                    if 'message' in message:
                        message = message['message']
                        if 'text' in message:
                            if message['from']['username'] == admin:
                                add_user_db[key] = message['text']
                                flag = False
                            else:
                                requests.get(base_url_str.format(
                                    confing.Token,
                                    'sendMessage') + '?chat_id=' + chat_id + f'&text=•Бот занят пользователем {admin}!')
    requests.get(base_url_str.format(
        confing.Token,
        'sendMessage') + '?chat_id=' + chat_id + f'&text=•Информация добавлена!')
    db.create(add_user_db)
    return (current_offset1)


def redactor_user(current_offset1, admin):
    requests.get(base_url_str.format(
        confing.Token,
        'sendMessage') + '?chat_id=' + chat_id + f'&text=•Введите должность, которую нужно отредактировать?')
    flag = True
    counter=0
    position=''
    while flag:
        if counter!=0:
            requests.get(base_url_str.format(
                confing.Token,
                'sendMessage') + '?chat_id=' + chat_id + f'&text=•Введите поле и его новое значение!')
        res = requests.get(
            base_url_str.format(
                confing.Token,
                'getUpdates'
            ),
            params={
                'timeout': timeout,
                'offset': current_offset1
            }
        ).json()
        if res['ok']:
            for message in res['result']:
                current_offset1 = message['update_id'] + 1
                if 'message' in message:
                    message = message['message']
                    if 'text' in message:
                        if message['from']['username'] == admin:
                            fields = message['text'].split()
                            if len(fields) >= 2 and counter==1:
                                checker = db.update({'Должность': position}, {fields[0]: fields[1]})
                                checker = checker.__getattribute__('raw_result')
                                checker = checker['updatedExisting']
                                if checker is True:
                                    requests.get(base_url_str.format(
                                        confing.Token,
                                        'sendMessage') + '?chat_id=' + chat_id + f'&text=•Готово!')
                                    flag = False
                                else:
                                    requests.get(base_url_str.format(
                                        confing.Token,
                                        'sendMessage') + '?chat_id=' + chat_id + f'&text=•Такой должности нет!')
                                    flag = False
                            elif counter==0:
                                position=message['text']
                                counter+=1
                            else:
                                requests.get(base_url_str.format(
                                    confing.Token,
                                    'sendMessage') + '?chat_id=' + chat_id + '&text=•Редактирование только в формате {Поле: Новое значение}!')
                        else:
                            requests.get(base_url_str.format(
                                confing.Token,
                                'sendMessage') + '?chat_id=' + chat_id + f'&text=•Бот занят пользователем {admin}!')

    return (current_offset1)


def remove_user(current_offset1, admin):
    requests.get(base_url_str.format(
        confing.Token,
        'sendMessage') + '?chat_id=' + chat_id + f'&text=•Введите поле и значение, которое нужно удалить!')
    flag = True
    while flag:
        res = requests.get(
            base_url_str.format(
                confing.Token,
                'getUpdates'
            ),
            params={
                'timeout': timeout,
                'offset': current_offset1
            }
        ).json()
        if res['ok']:
            for message in res['result']:
                current_offset1 = message['update_id'] + 1
                if 'message' in message:
                    message = message['message']
                    if 'text' in message:
                        if message['from']['username'] == admin:
                            fields = message['text'].split(maxsplit=1)
                            if len(fields) == 2:
                                checker = db.delete({fields[0]: fields[1]})
                                if checker.__getattribute__('acknowledged'):
                                    requests.get(base_url_str.format(
                                        confing.Token,
                                        'sendMessage') + '?chat_id=' + chat_id + f'&text=•Готово!')
                                    flag = False
                                else:
                                    requests.get(base_url_str.format(
                                        confing.Token,
                                        'sendMessage') + '?chat_id=' + chat_id + f'&text=•Нет такого человека!')
                                    flag = False
                            else:
                                requests.get(base_url_str.format(
                                    confing.Token,
                                    'sendMessage') + '?chat_id=' + chat_id + '&text=•Запрос в виде {Поле значение}!')
                                flag = False

                        else:
                            requests.get(base_url_str.format(
                                confing.Token,
                                'sendMessage') + '?chat_id=' + chat_id + f'&text=•Бот занят пользователем {admin}!')

    return (current_offset1)


admins_list = requests.get(
    base_url_str.format(
        confing.Token,
        'getChatAdministrators'
    ),
    params={
        'chat_id': chat_id
    }
).json()
if admins_list['ok']:
    admin_list = [admin['user']['username']
                  for admin in admins_list['result']]


def help():
    requests.get(base_url_str.format(
        confing.Token,
        'sendMessage') + '?chat_id=' + chat_id + '&text=•Команды:\n/worker {Должность}\n/edit - команда для админов!')

requests.get(base_url_str.format(
    confing.Token,
    'sendMessage') + '?chat_id=' + chat_id + '&text=•Бот Готов!')
while True:
    res = requests.get(
        base_url_str.format(
            confing.Token,
            'getUpdates'
        ),
        params={
            'timeout': timeout,
            'offset': current_offset
        }
    ).json()
    if res['ok']:
        for message in res['result']:
            current_offset = message['update_id'] + 1
            if 'message' in message:
                message = message['message']
                if 'text' in message:
                    date = dt.datetime.utcfromtimestamp(message['date'])
                    print(date, '|', message['from']['username'], ':', message['text'])
                    command = message['text'].split('@')[0]
                    command = command.split(' ')[0]
                    if '/' in command:
                        if command == '/worker':
                            try:
                                message_ = message['text'].split(' ', maxsplit=1)[1]
                                search_user(message_)
                            except IndexError:
                                requests.get(base_url_str.format(
                                    confing.Token,
                                    'sendMessage') + '?chat_id=' + chat_id + '&text=•Неверная команда!')
                        elif command == '/edit':
                            show_keyboard(message['from']['username'])
                        elif command == '/help':
                            help()
                        else:
                            requests.get(base_url_str.format(
                                confing.Token,
                                'sendMessage') + '?chat_id=' + chat_id + '&text=•Неверная команда!')
                    if message['from']['username'] in admin_list:
                        admin = message['from']['username']
                        if message['text'] == 'Добавить':
                            current_offset = add_user(current_offset, admin)
                        elif message['text'] == 'Редактировать':
                            current_offset = redactor_user(current_offset, admin)
                        elif message['text'] == 'Удалить':
                            current_offset = remove_user(current_offset, admin)
