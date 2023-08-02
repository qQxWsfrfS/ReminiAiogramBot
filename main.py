from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BotCommand, CallbackQuery, FSInputFile, Update, PreCheckoutQuery, BotCommand, ContentType, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import StateFilter, Text 
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
import asyncio 
import json 


from config import BOT_TOKEN, MARKUP
from filters import start_command,admin_command

from buttons import enchance_markup, face_enhance_markup, back_to_settings_photo_markup, back_enhance_markup,color_edit_markup, admin_mrkp, back_mrkp, coming_admin_mrkp
from fsm import FSMFillFormMode
from remini import ImageCreator

from aiogram.exceptions import TelegramBadRequest
import os 
import aiofiles 

bot:Bot = Bot(token = BOT_TOKEN)
dp: Dispatcher = Dispatcher()
 
ADMINS = [] # list for admins // Input telegram_id










button_cancel : InlineKeyboardButton = InlineKeyboardButton(text = 'Отменить ❌', callback_data='cancel')
button_generate : InlineKeyboardButton = InlineKeyboardButton(text='Сгенерировать ✅', callback_data = 'generate')



async def set_main_menu(bot:Bot):
    main_menu_commands = [
        BotCommand(command = '/admin', description='Admin panel'),
        BotCommand(command = '/start', description = 'Start command')

    ]
    await bot.set_my_commands(main_menu_commands)

@dp.callback_query(Text(text = ['back_admin']))
async def start_inline(callback : CallbackQuery):
    async with aiofiles.open('white_list.txt', 'r') as file:
        src = await file.read()
    users_list = list(map(lambda x : x[1:], src.split('\n')))
    await callback.message.delete_reply_markup()
    if callback.from_user.username not in users_list and callback.from_user.id not in ADMINS:
        await bot.send_message(chat_id = callback.from_user.id, text = 'Недостатоно прав доступа')
    else:
        await bot.send_message(chat_id = callback.from_user.id, text = 'Привет, данный бот поможет сделать изображения более качественными и детализированными\n\nотправьте боту изображение как файл (весом до 20 мегабайт)')



@dp.message(start_command)
async def start_message(message : Message):
    async with aiofiles.open('white_list.txt', 'r') as file:
        src = await file.read()
    users_list = list(map(lambda x : x[1:], src.split('\n')))
    if message.chat.username not in users_list and message.chat.id not in ADMINS:
        await bot.send_message(chat_id = message.chat.id, text = 'Недостатоно прав доступа')
    else:
        await bot.send_message(chat_id = message.chat.id, text = 'Привет, данный бот поможет сделать изображения более качественными и детализированными\n\nотправьте боту изображение как файл (весом до 20 мегабайт)')


@dp.message(admin_command)
async def get_admin_command(message : Message, state : FSMContext):
    if message.chat.id not in ADMINS:
        await bot.send_message(chat_id = message.chat.id, text = 'Недостаточно прав доступа')
    else:
        await bot.send_message(chat_id = message.chat.id, text=  'Перейти в админ панель?', reply_markup = coming_admin_mrkp)



@dp.callback_query(Text(text = ['go_admin', 'back_to_admin']))
async def get_admin_panel(callback : CallbackQuery, state : FSMContext):
    await state.set_state(FSMFillFormMode.admin_state)
    async with aiofiles.open('white_list.txt', 'r') as file:
        src = await file.read()
   

    admins_list = []
    for item in ADMINS:
        try:
            chat = await bot.get_chat(item)
            name = chat.username 
            admins_list.append(name)
        except TelegramBadRequest:


    if src == '':
        text_empty = 'Список разрешенных пользователей пуст'
    else:
        users = src.split('\n')
        all_users = "\n".join(users)
        text_empty = f'Список пользователей\n{all_users}'

    new_text = f'Администраторы: {",".join(admins_list)}\n{text_empty}'
    await callback.message.edit_text(text = new_text,reply_markup = admin_mrkp)

           
@dp.callback_query(Text(text=['add_user']))
async def add_user(callback : CallbackQuery, state : FSMContext):
    await callback.message.edit_text(text = 'Запишите юзернэйм пользователя, которого хотите добавить', reply_markup = back_mrkp)
    await state.set_state(FSMFillFormMode.input_user)

@dp.message(StateFilter(FSMFillFormMode.input_user))
async def process_add_user(message : Message, state : FSMContext):
    try:
        added_user = str(message.text)
        async with aiofiles.open('white_list.txt', 'a') as file:
            await file.write(f'\n{added_user}')
        dm = await bot.send_message(chat_id = message.chat.id , text = 'Пользователь успешно добавлен', reply_markup = back_mrkp)
    except Exception as ex:
        print(ex)
        await bot.send_message(chat_id = message.chat.id, text = 'Произошла ошибка сервера')




@dp.callback_query(Text(text=['remove_user']))
async def remove_user(callback : CallbackQuery, state : FSMContext):

    await state.set_state(FSMFillFormMode.remove_users_state)
    async with aiofiles.open('white_list.txt', 'r') as file:
        src = await file.read()
    all_users = src.split('\n')

    all_users = "\n".join(all_users).replace('@', '/')

    if all_users == '':
        text = 'Пользователи отсутствуют'
    else:
        text = f'Выберите пользователя, которого хотите удалить:\n{all_users.strip()}'
    

    await callback.message.edit_text(text = text, reply_markup = back_mrkp)


@dp.message(StateFilter(FSMFillFormMode.remove_users_state))
async def removing_user(message : Message, state : FSMContext):
    if message.text.startswith('/'):
        user_for_del = message.text.replace('/', '@')
        async with aiofiles.open('white_list.txt', 'r') as file:
            src = await file.read()

        list_users = src.split('\n')
        if user_for_del.strip() in list_users:
            list_users.remove(user_for_del.strip())
            async with aiofiles.open('white_list.txt', 'w') as file:
                await file.write('\n'.join(list_users))
          
            async with aiofiles.open('white_list.txt', 'r') as file:
                src = await file.read()
            wait_mes = await bot.send_message(chat_id = message.chat.id, text  = f'Пользователь {user_for_del} успешно удален')
            await asyncio.sleep(2)
            all_users = src.split('\n')
            all_users = " ".join(all_users).replace('@', '/')
            if all_users == '':
                text = 'Пользователи отсутствуют'
            else:
                text = f'Выберите пользователя, которого хотите удалить:\n{all_users.strip()}'
            await bot.send_message(chat_id = message.chat.id, text = text, reply_markup = back_mrkp)
            await bot.delete_message(chat_id = message.chat.id , message_id = wait_mes.message_id)






@dp.message(F.content_type == 'photo')
async def get_photo(message : Message, state : FSMContext):
    await bot.send_message(chat_id = message.chat.id, text = 'Пришли мне фотографию только в формате файла')
    



@dp.message(F.content_type != 'document')
async def get_other_format(message : Message):
    await bot.send_message(chat_id = message.chat.id, text = 'Необрабатываемый формат файла')




@dp.callback_query(Text(text = ['settings_photo']))
async def get_message_doc(callback : CallbackQuery, state : FSMContext):
        markup = MARKUP


        button_face_enhance : InlineKeyboardButton = InlineKeyboardButton(text = 'Face enhance', callback_data='space')

        base_face_text = 'Base ✅' if markup['Face enhance']['Base'] == 1 else 'Base 🚫' 
        beautify_face_text = 'Beautify ✅' if markup['Face enhance']['Beautify'] == 1 else 'Beautify 🚫'

        button_base_face : InlineKeyboardButton = InlineKeyboardButton(text = base_face_text, callback_data = 'base_face')
        button_beautify_face : InlineKeyboardButton = InlineKeyboardButton(text = beautify_face_text, callback_data='beautify_face')


        button_background_enhance : InlineKeyboardButton = InlineKeyboardButton(text = 'Background enhance', callback_data='space')

        base_background_text = 'Base ✅' if markup['Background enhance']['Base'] == 1 else 'Base 🚫'
        professional_background_text = 'Professional ✅' if markup['Background enhance']['Professional'] == 1 else 'Professional 🚫'


        button_base_background : InlineKeyboardButton = InlineKeyboardButton(text = base_background_text, callback_data='base_back')
        button_professional_background : InlineKeyboardButton = InlineKeyboardButton(text = professional_background_text, callback_data='professional_back')




        button_color_enhance : InlineKeyboardButton = InlineKeyboardButton(text = 'Color enhance', callback_data='space')


        none_color_text = 'None ✅' if markup['Color enhance']['none'] == 1 else 'None 🚫'
        new_york_color_text = 'New-York ✅' if markup['Color enhance']['new-york'] == 1 else 'New-York 🚫'
        jakarta_color_text = 'Jakarta ✅' if markup['Color enhance']['jakarta'] == 1 else 'Jakarta 🚫'
        naples_color_text = 'Naples ✅' if markup['Color enhance']['naples'] == 1 else 'Naples 🚫'
        mumbai_color_text = 'Mumbai ✅' if markup['Color enhance']['mumbai'] == 1 else 'Mumbai 🚫'
        chicago_color_text = 'Chicago ✅' if markup['Color enhance']['chicago'] == 1 else 'Chicago 🚫'
        edinburgh_color_text = 'Edinburgh ✅' if markup['Color enhance']['edinburgh'] == 1 else 'Edinburgh 🚫'
        madrid_color_text = 'Madrid ✅' if markup['Color enhance']['madrid'] == 1 else 'Madrid 🚫'



        none_color_button : InlineKeyboardButton = InlineKeyboardButton(text = none_color_text, callback_data= 'none_color')
        new_york_color_button : InlineKeyboardButton = InlineKeyboardButton(text = new_york_color_text, callback_data = 'new-york_color')
        jakarta_color_button : InlineKeyboardButton = InlineKeyboardButton(text = jakarta_color_text, callback_data = 'jakarta_color')
        naples_color_button : InlineKeyboardButton = InlineKeyboardButton(text = naples_color_text, callback_data = 'naples_color')
        mumbai_color_button : InlineKeyboardButton = InlineKeyboardButton(text = mumbai_color_text, callback_data = 'mumbai_color')
        chicago_color_button : InlineKeyboardButton = InlineKeyboardButton(text = chicago_color_text, callback_data = 'chicago_color')
        edinburgh_color_button : InlineKeyboardButton = InlineKeyboardButton(text = edinburgh_color_text, callback_data = 'edinburgh_color')
        madrid_color_button : InlineKeyboardButton = InlineKeyboardButton(text = madrid_color_text, callback_data = 'madrid_color')




        space_button : InlineKeyboardButton = InlineKeyboardButton(text = '              ', callback_data='space')

        await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard = [[button_face_enhance], 
                                                                                                    [button_base_face, button_beautify_face],       
                                                                                                    [button_background_enhance],  
                                                                                                    [button_base_background, button_professional_background], 
                                                                                                    [button_color_enhance],
                                                                                                    [new_york_color_button, jakarta_color_button,naples_color_button], 
                                                                                                    [mumbai_color_button,chicago_color_button,edinburgh_color_button], 
                                                                                                    [madrid_color_button, none_color_button], 
                                                                                                    [space_button], 
                                                                                                    [button_cancel], [button_generate]]))
        async with aiofiles.open(f'{callback.from_user.id}.json', mode = 'w', encoding='UTF-8') as file:
            await file.write(json.dumps(markup, ensure_ascii=False, indent=4))



@dp.message(F.content_type == 'document')
async def get_message_doc(message : Message, state : FSMContext):
    async with aiofiles.open('white_list.txt', 'r') as file:
        src = await file.read()
    users_list = list(map(lambda x : x[1:], src.split('\n')))
    if message.chat.username not in users_list and message.chat.id not in ADMINS:
        await bot.send_message(chat_id = message.chat.id, text = 'Недостаточно прав доступа')
    else:
        if 'image' in message.document.mime_type:
            data = await state.get_data()
            try:
                message_for_del = data.get('photo')
                await bot.delete_message(chat_id = message.chat.id, message_id = message_for_del.message_id)
            except Exception:
                print(f'_')
            markup = MARKUP 
            photo = message.document 
            file_info = await bot.get_file(photo.file_id)

            file_path = file_info.file_path
            await bot.download_file(file_path, f'{message.chat.id}.jpg')
            photo = photo.file_id
            await state.set_state(FSMFillFormMode.input_photo_state)


            button_face_enhance : InlineKeyboardButton = InlineKeyboardButton(text = 'Face enhance', callback_data='space')

        


            button_background_enhance : InlineKeyboardButton = InlineKeyboardButton(text = 'Background enhance', callback_data='space')

            


            button_color_enhance : InlineKeyboardButton = InlineKeyboardButton(text = 'Color enhance', callback_data='space')

            button_settings_photo : InlineKeyboardButton = InlineKeyboardButton(text = 'Настройки обработки', callback_data = 'settings_photo')
       





            space_button : InlineKeyboardButton = InlineKeyboardButton(text = '              ', callback_data='space')

            deleted_message = await bot.send_document(chat_id = message.chat.id, document=photo, caption='Ваша фотография успешно загружена и готова к обработке', reply_markup=InlineKeyboardMarkup(inline_keyboard = [[button_settings_photo], 
                                                                                                                                                                                                                        [button_cancel], [button_generate]]))
            async with aiofiles.open(f'{message.chat.id}.json', mode = 'w', encoding='UTF-8') as file:
                await file.write(json.dumps(markup, ensure_ascii=False, indent=4))
            await state.update_data(photo = deleted_message)


        else:
            await bot.send_message(chat_id = message.chat.id, text = 'Данный формат файла не поддерживается. Пожалуйста пришлите файл с изображением (JPG, PNG, TIFF, HEIC, GIF)')




'''face calls'''
@dp.callback_query(Text(text = ['base_face', 'beautify_face']))
async def get_face(callback : CallbackQuery, state : FSMContext):

    current_face = callback.data.split('_')[0]
    async with aiofiles.open(f'{callback.from_user.id}.json', mode = 'r', encoding = 'UTF-8') as file:
        data = await file.read()
        markup = json.loads(data)


    for k,v in markup['Face enhance'].items():
        if k.lower() == current_face:
            markup['Face enhance'][k] = 1 
        else:
            markup['Face enhance'][k] = 0


    button_face_enhance : InlineKeyboardButton = InlineKeyboardButton(text = 'Face enhance', callback_data='space')

    base_face_text = 'Base ✅' if markup['Face enhance']['Base'] == 1 else 'Base 🚫' 
    beautify_face_text = 'Beautify ✅' if markup['Face enhance']['Beautify'] == 1 else 'Beautify 🚫'

    button_base_face : InlineKeyboardButton = InlineKeyboardButton(text = base_face_text, callback_data = 'base_face')
    button_beautify_face : InlineKeyboardButton = InlineKeyboardButton(text = beautify_face_text, callback_data='beautify_face')







    button_background_enhance : InlineKeyboardButton = InlineKeyboardButton(text = 'Background enhance', callback_data='space')

    base_background_text = 'Base ✅' if markup['Background enhance']['Base'] == 1 else 'Base 🚫'
    professional_background_text = 'Professional ✅' if markup['Background enhance']['Professional'] == 1 else 'Professional 🚫'


    button_base_background : InlineKeyboardButton = InlineKeyboardButton(text = base_background_text, callback_data='base_back')
    button_professional_background : InlineKeyboardButton = InlineKeyboardButton(text = professional_background_text, callback_data='professional_back')






    button_color_enhance : InlineKeyboardButton = InlineKeyboardButton(text = 'Color enhance', callback_data='space')


    none_color_text = 'None ✅' if markup['Color enhance']['none'] == 1 else 'None 🚫'
    new_york_color_text = 'New-York ✅' if markup['Color enhance']['new-york'] == 1 else 'New-York 🚫'
    jakarta_color_text = 'Jakarta ✅' if markup['Color enhance']['jakarta'] == 1 else 'Jakarta 🚫'
    naples_color_text = 'Naples ✅' if markup['Color enhance']['naples'] == 1 else 'Naples 🚫'
    mumbai_color_text = 'Mumbai ✅' if markup['Color enhance']['mumbai'] == 1 else 'Mumbai 🚫'
    chicago_color_text = 'Chicago ✅' if markup['Color enhance']['chicago'] == 1 else 'Chicago 🚫'
    edinburgh_color_text = 'Edinburgh ✅' if markup['Color enhance']['edinburgh'] == 1 else 'Edinburgh 🚫'
    madrid_color_text = 'Madrid ✅' if markup['Color enhance']['madrid'] == 1 else 'Madrid 🚫'


    none_color_button : InlineKeyboardButton = InlineKeyboardButton(text = none_color_text, callback_data= 'none_color')
    new_york_color_button : InlineKeyboardButton = InlineKeyboardButton(text = new_york_color_text, callback_data = 'new-york_color')
    jakarta_color_button : InlineKeyboardButton = InlineKeyboardButton(text = jakarta_color_text, callback_data = 'jakarta_color')
    naples_color_button : InlineKeyboardButton = InlineKeyboardButton(text = naples_color_text, callback_data = 'naples_color')
    mumbai_color_button : InlineKeyboardButton = InlineKeyboardButton(text = mumbai_color_text, callback_data = 'mumbai_color')
    chicago_color_button : InlineKeyboardButton = InlineKeyboardButton(text = chicago_color_text, callback_data = 'chicago_color')
    edinburgh_color_button : InlineKeyboardButton = InlineKeyboardButton(text = edinburgh_color_text, callback_data = 'edinburgh_color')
    madrid_color_button : InlineKeyboardButton = InlineKeyboardButton(text = madrid_color_text, callback_data = 'madrid_color')

    space_button : InlineKeyboardButton = InlineKeyboardButton(text = '              ', callback_data='space')


    reply_markup=InlineKeyboardMarkup(inline_keyboard = [[button_face_enhance], 
                                                        [button_base_face, button_beautify_face],       
                                                        [button_background_enhance],  
                                                        [button_base_background, button_professional_background], 
                                                        [button_color_enhance],
                                                        [new_york_color_button, jakarta_color_button,naples_color_button], 
                                                        [mumbai_color_button,chicago_color_button,edinburgh_color_button], 
                                                        [madrid_color_button, none_color_button], 
                                                        [space_button], [button_cancel], [button_generate]])
    
    #await callback.message.delete_reply_markup()
    await callback.message.edit_reply_markup(reply_markup=reply_markup)

    async with aiofiles.open(f'{callback.from_user.id}.json', mode = 'w', encoding='UTF-8') as file:
            await file.write(json.dumps(markup, ensure_ascii=False, indent=4))








@dp.callback_query(Text(text = ['base_back', 'professional_back']))
async def get_back(callback : CallbackQuery, state : FSMContext):

    current_face = callback.data.split('_')[0]
    async with aiofiles.open(f'{callback.from_user.id}.json', mode = 'r', encoding = 'UTF-8') as file:
        data = await file.read()
        markup = json.loads(data)


    for k,v in markup['Background enhance'].items():
        if k.lower() == current_face:
            markup['Background enhance'][k] = 1 
        else:
            markup['Background enhance'][k] = 0


    button_face_enhance : InlineKeyboardButton = InlineKeyboardButton(text = 'Face enhance', callback_data='space')

    base_face_text = 'Base ✅' if markup['Face enhance']['Base'] == 1 else 'Base 🚫' 
    beautify_face_text = 'Beautify ✅' if markup['Face enhance']['Beautify'] == 1 else 'Beautify 🚫'

    button_base_face : InlineKeyboardButton = InlineKeyboardButton(text = base_face_text, callback_data = 'base_face')
    button_beautify_face : InlineKeyboardButton = InlineKeyboardButton(text = beautify_face_text, callback_data='beautify_face')







    button_background_enhance : InlineKeyboardButton = InlineKeyboardButton(text = 'Background enhance', callback_data='space')

    base_background_text = 'Base ✅' if markup['Background enhance']['Base'] == 1 else 'Base 🚫'
    professional_background_text = 'Professional ✅' if markup['Background enhance']['Professional'] == 1 else 'Professional 🚫'


    button_base_background : InlineKeyboardButton = InlineKeyboardButton(text = base_background_text, callback_data='base_back')
    button_professional_background : InlineKeyboardButton = InlineKeyboardButton(text = professional_background_text, callback_data='professional_back')






    button_color_enhance : InlineKeyboardButton = InlineKeyboardButton(text = 'Color enhance', callback_data='space')


    none_color_text = 'None ✅' if markup['Color enhance']['none'] == 1 else 'None 🚫'
    new_york_color_text = 'New-York ✅' if markup['Color enhance']['new-york'] == 1 else 'New-York 🚫'
    jakarta_color_text = 'Jakarta ✅' if markup['Color enhance']['jakarta'] == 1 else 'Jakarta 🚫'
    naples_color_text = 'Naples ✅' if markup['Color enhance']['naples'] == 1 else 'Naples 🚫'
    mumbai_color_text = 'Mumbai ✅' if markup['Color enhance']['mumbai'] == 1 else 'Mumbai 🚫'
    chicago_color_text = 'Chicago ✅' if markup['Color enhance']['chicago'] == 1 else 'Chicago 🚫'
    edinburgh_color_text = 'Edinburgh ✅' if markup['Color enhance']['edinburgh'] == 1 else 'Edinburgh 🚫'
    madrid_color_text = 'Madrid ✅' if markup['Color enhance']['madrid'] == 1 else 'Madrid 🚫'



    none_color_button : InlineKeyboardButton = InlineKeyboardButton(text = none_color_text, callback_data= 'none_color')
    new_york_color_button : InlineKeyboardButton = InlineKeyboardButton(text = new_york_color_text, callback_data = 'new-york_color')
    jakarta_color_button : InlineKeyboardButton = InlineKeyboardButton(text = jakarta_color_text, callback_data = 'jakarta_color')
    naples_color_button : InlineKeyboardButton = InlineKeyboardButton(text = naples_color_text, callback_data = 'naples_color')
    mumbai_color_button : InlineKeyboardButton = InlineKeyboardButton(text = mumbai_color_text, callback_data = 'mumbai_color')
    chicago_color_button : InlineKeyboardButton = InlineKeyboardButton(text = chicago_color_text, callback_data = 'chicago_color')
    edinburgh_color_button : InlineKeyboardButton = InlineKeyboardButton(text = edinburgh_color_text, callback_data = 'edinburgh_color')
    madrid_color_button : InlineKeyboardButton = InlineKeyboardButton(text = madrid_color_text, callback_data = 'madrid_color')

    space_button : InlineKeyboardButton = InlineKeyboardButton(text = '              ', callback_data='space')


    reply_markup=InlineKeyboardMarkup(inline_keyboard = [[button_face_enhance], 
                                                        [button_base_face, button_beautify_face],       
                                                        [button_background_enhance],  
                                                        [button_base_background, button_professional_background], 
                                                        [button_color_enhance],
                                                        [new_york_color_button, jakarta_color_button,naples_color_button], 
                                                        [mumbai_color_button,chicago_color_button,edinburgh_color_button], 
                                                        [madrid_color_button, none_color_button], 
                                                        [space_button], [button_cancel], [button_generate]])
    
    #await callback.message.delete_reply_markup()
    await callback.message.edit_reply_markup(reply_markup=reply_markup)

    async with aiofiles.open(f'{callback.from_user.id}.json', mode = 'w', encoding='UTF-8') as file:
            await file.write(json.dumps(markup, ensure_ascii=False, indent=4))





'''color'''
@dp.callback_query(Text(text = ['none_color', 'new-york_color', 'jakarta_color', 'naples_color','mumbai_color', 'chicago_color', 'edinburgh_color', 'madrid_color']))
async def get_color(callback : CallbackQuery, state : FSMContext):

    current_face = callback.data.split('_')[0]
    async with aiofiles.open(f'{callback.from_user.id}.json', mode = 'r', encoding = 'UTF-8') as file:
        data = await file.read()
        markup = json.loads(data)


    for k,v in markup['Color enhance'].items():
        if k.lower() == current_face:
            markup['Color enhance'][k] = 1 
        else:
            markup['Color enhance'][k] = 0


    button_face_enhance : InlineKeyboardButton = InlineKeyboardButton(text = 'Face enhance', callback_data='space')

    base_face_text = 'Base ✅' if markup['Face enhance']['Base'] == 1 else 'Base 🚫' 
    beautify_face_text = 'Beautify ✅' if markup['Face enhance']['Beautify'] == 1 else 'Beautify 🚫'

    button_base_face : InlineKeyboardButton = InlineKeyboardButton(text = base_face_text, callback_data = 'base_face')
    button_beautify_face : InlineKeyboardButton = InlineKeyboardButton(text = beautify_face_text, callback_data='beautify_face')







    button_background_enhance : InlineKeyboardButton = InlineKeyboardButton(text = 'Background enhance', callback_data='space')

    base_background_text = 'Base ✅' if markup['Background enhance']['Base'] == 1 else 'Base 🚫'
    professional_background_text = 'Professional ✅' if markup['Background enhance']['Professional'] == 1 else 'Professional 🚫'


    button_base_background : InlineKeyboardButton = InlineKeyboardButton(text = base_background_text, callback_data='base_back')
    button_professional_background : InlineKeyboardButton = InlineKeyboardButton(text = professional_background_text, callback_data='professional_back')






    button_color_enhance : InlineKeyboardButton = InlineKeyboardButton(text = 'Color enhance', callback_data='space')



    none_color_text = 'None ✅' if markup['Color enhance']['none'] == 1 else 'None 🚫'
    new_york_color_text = 'New-York ✅' if markup['Color enhance']['new-york'] == 1 else 'New-York 🚫'
    jakarta_color_text = 'Jakarta ✅' if markup['Color enhance']['jakarta'] == 1 else 'Jakarta 🚫'
    naples_color_text = 'Naples ✅' if markup['Color enhance']['naples'] == 1 else 'Naples 🚫'
    mumbai_color_text = 'Mumbai ✅' if markup['Color enhance']['mumbai'] == 1 else 'Mumbai 🚫'
    chicago_color_text = 'Chicago ✅' if markup['Color enhance']['chicago'] == 1 else 'Chicago 🚫'
    edinburgh_color_text = 'Edinburgh ✅' if markup['Color enhance']['edinburgh'] == 1 else 'Edinburgh 🚫'
    madrid_color_text = 'Madrid ✅' if markup['Color enhance']['madrid'] == 1 else 'Madrid 🚫'

    none_color_button : InlineKeyboardButton = InlineKeyboardButton(text = none_color_text, callback_data= 'none_color')
    new_york_color_button : InlineKeyboardButton = InlineKeyboardButton(text = new_york_color_text, callback_data = 'new-york_color')
    jakarta_color_button : InlineKeyboardButton = InlineKeyboardButton(text = jakarta_color_text, callback_data = 'jakarta_color')
    naples_color_button : InlineKeyboardButton = InlineKeyboardButton(text = naples_color_text, callback_data = 'naples_color')
    mumbai_color_button : InlineKeyboardButton = InlineKeyboardButton(text = mumbai_color_text, callback_data = 'mumbai_color')
    chicago_color_button : InlineKeyboardButton = InlineKeyboardButton(text = chicago_color_text, callback_data = 'chicago_color')
    edinburgh_color_button : InlineKeyboardButton = InlineKeyboardButton(text = edinburgh_color_text, callback_data = 'edinburgh_color')
    madrid_color_button : InlineKeyboardButton = InlineKeyboardButton(text = madrid_color_text, callback_data = 'madrid_color')

    space_button : InlineKeyboardButton = InlineKeyboardButton(text = '              ', callback_data='space')


    reply_markup=InlineKeyboardMarkup(inline_keyboard = [[button_face_enhance], 
                                                        [button_base_face, button_beautify_face],       
                                                        [button_background_enhance],  
                                                        [button_base_background, button_professional_background], 
                                                        [button_color_enhance],
                                                        [new_york_color_button, jakarta_color_button,naples_color_button], 
                                                        [mumbai_color_button,chicago_color_button,edinburgh_color_button], 
                                                        [madrid_color_button, none_color_button], 
                                                        [space_button], [button_cancel], [button_generate]])
    
    #await callback.message.delete_reply_markup()
    await callback.message.edit_reply_markup(reply_markup=reply_markup)

    async with aiofiles.open(f'{callback.from_user.id}.json', mode = 'w', encoding='UTF-8') as file:
            await file.write(json.dumps(markup, ensure_ascii=False, indent=4))


@dp.callback_query(Text(text = ['space']))
async def reply_space(callback : CallbackQuery):
    await callback.answer()





@dp.callback_query(Text(text = ['cancel']))
async def cancel_image(callback : CallbackQuery):
    await callback.message.delete_reply_markup()
    if os.path.isfile(f'{callback.from_user.id}.jpg'):
        os.remove(f'{callback.from_user.id}.jpg')
    if os.path.isfile(f'{callback.from_user.id}.json'):
        os.remove(f'{callback.from_user.id}.json')
    await bot.send_message(chat_id = callback.from_user.id, text = 'Привет, данный бот поможет сделать изображения более качественными и детализированными\n\nотправьте боту изображение как файл (весом до 20 мегабайт)')
     


@dp.callback_query(Text(text = ['generate']))
async def generate_image(callback : CallbackQuery):
    await callback.message.delete_reply_markup()
    await callback.answer()
    async with aiofiles.open(f'{callback.from_user.id}.json', mode = 'r', encoding = 'UTF-8') as file:
        data = await file.read()
        variables = json.loads(data)
    for k,v in variables['Face enhance'].items():
        if v == 1:
            current_face = k.lower()  
    for k,v in variables['Background enhance'].items():
        if v == 1:
            current_back = k.lower()  
    for k,v in variables['Color enhance'].items():
        if v == 1:
            current_color = k.lower()
    message_wait = await bot.send_message(chat_id = callback.from_user.id, text = 'Обрабатываю ваше изображение. Ожидайте...')
    photo_path = await ImageCreator()._generate(callback.from_user.id, current_face, current_back, current_color)
    if photo_path is not False:
        photo = FSInputFile(photo_path)
        await bot.send_document(chat_id = callback.from_user.id, document = photo)
        print(f'[+] Обработал изображение пользователя {callback.from_user.username}')
        await asyncio.sleep(2)
        await bot.send_message(chat_id = callback.from_user.id, text = 'Для обработки следующего изображения пришлите его в виде файла')
        await bot.delete_message(chat_id = callback.from_user.id, message_id = message_wait.message_id)
        if os.path.isfile(f'{callback.from_user.id}.jpg'):
            os.remove(f'{callback.from_user.id}.jpg')
        if os.path.isfile(f'{callback.from_user.id}.json'):
            os.remove(f'{callback.from_user.id}.json')
    else:
        await bot.send_message(chat_id = callback.from_user.id, text = 'Недостаточно кредитов. Пополните счет')
        await bot.delete_message(chat_id = callback.from_user.id, message_id = message_wait.message_id)





if __name__ == '__main__':
    print(f'Бот запущен')
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)