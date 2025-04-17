from aiogram.dispatcher.filters.state import State, StatesGroup

class Form(StatesGroup):
    choose_language = State()
    full_name = State()
    job_title = State()
    expertise = State()
    help_offer = State()
    upload_photo = State()
    contact_phone = State()
    social_links = State()
    about_business = State()
    website_link = State()
    custom_link = State()
    done = State()
