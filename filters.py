


from aiogram.types import Message 


def start_command(message : Message) ->bool:
    return message.text == '/start'


def admin_command(message : Message) -> bool:
    return message.text  == '/admin'