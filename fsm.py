from aiogram.filters.state import StatesGroup, State 



class FSMFillFormMode(StatesGroup):
	input_photo_state = State()
	admin_state = State()
	input_user = State()
	remove_users_state = State()