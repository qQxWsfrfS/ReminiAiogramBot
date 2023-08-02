from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup 













go_admin_btn : InlineKeyboardButton = InlineKeyboardButton(text = 'Админ панель', callback_data = 'go_admin')
no_admin_btn : InlineKeyboardButton = InlineKeyboardButton(text = 'Вернуться', callback_data = 'back_admin')

coming_admin_mrkp : InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard = [[go_admin_btn, no_admin_btn]])



button_add_user : InlineKeyboardButton = InlineKeyboardButton(text = 'Добавить пользователя', callback_data = 'add_user')
button_remove_user : InlineKeyboardButton = InlineKeyboardButton(text = 'Удалить пользователя', callback_data = 'remove_user')

admin_mrkp : InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[button_add_user, button_remove_user]])



btn_back_admin : InlineKeyboardButton = InlineKeyboardButton(text= 'Назад', callback_data = 'back_to_admin')
back_mrkp : InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard= [[btn_back_admin]])





face_enhance_inline : InlineKeyboardButton = InlineKeyboardButton(text = 'Улучшение лица', callback_data= 'face_enhance')
background_enhance_inline : InlineKeyboardButton = InlineKeyboardButton(text = 'Улучшение фона', callback_data = 'background_enhance_inline')
color_enhance_inline : InlineKeyboardButton = InlineKeyboardButton(text = 'Улучшение цвета', callback_data= 'color_enhance')
back_menu_inline : InlineKeyboardButton = InlineKeyboardButton(text = 'Отменить редактирование', callback_data='back_menu')
generate_image : InlineKeyboardButton = InlineKeyboardButton(text = 'Сгенерировать✅', callback_data='generate')

enchance_markup : InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[face_enhance_inline], [background_enhance_inline], [color_enhance_inline], [back_menu_inline], [generate_image]])


back_to_settings_photo : InlineKeyboardButton = InlineKeyboardButton(text = 'Вернуться', callback_data='photo_settings')
back_to_settings_photo_markup : InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[back_to_settings_photo]])




#Улучшение лица 
face_enhance_base : InlineKeyboardButton = InlineKeyboardButton(text = 'Режим --base', callback_data='base_face_enhance')
face_enhance_beautify : InlineKeyboardButton = InlineKeyboardButton(text = 'Режим --beautify', callback_data='beautify_face_enchance')

face_enhance_markup : InlineKeyboardMarkup =InlineKeyboardMarkup(inline_keyboard=[[face_enhance_base], [face_enhance_beautify]])

#улучшение фона 
back_enhance_base : InlineKeyboardButton = InlineKeyboardButton(text = 'Режим --base', callback_data='base_back_enhance')
back_enhance_proffesional : InlineKeyboardButton = InlineKeyboardButton (text = 'Режим --professional', callback_data = 'professional_back_enhance')
back_enhance_markup : InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard =  [[back_enhance_base], [back_enhance_proffesional]]) 




#Улучшение цвета 
color_new_york : InlineKeyboardButton = InlineKeyboardButton(text = 'New York', callback_data='new-york_color')
color_jakarta : InlineKeyboardButton = InlineKeyboardButton(text = 'Jakarta', callback_data='jakarta_color')
color_naples : InlineKeyboardButton = InlineKeyboardButton(text = 'Naples', callback_data='naples_color')
color_mumbai : InlineKeyboardButton = InlineKeyboardButton(text = 'Mumbai', callback_data='mumbai_color')
color_chicago : InlineKeyboardButton = InlineKeyboardButton(text = 'Chicago', callback_data='chicago_color')
color_edinburgh : InlineKeyboardButton = InlineKeyboardButton(text = 'Edinburgh', callback_data='edinburgh_color')
color_madrid : InlineKeyboardButton = InlineKeyboardButton(text = 'Madrid', callback_data='madrid_color')

color_edit_markup : InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[[color_new_york, color_jakarta, color_naples], 
                                                                                    [color_mumbai, color_chicago, color_edinburgh], [color_madrid]])



