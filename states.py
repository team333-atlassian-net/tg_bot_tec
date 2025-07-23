from aiogram.fsm.state import State, StatesGroup


class ExcursionCreationSG(StatesGroup):
    title = State()
    description = State()
    confirm = State()
    material_name = State()
    upload_materials = State()
    material_end = State()


class ExcursionViewSG(StatesGroup):
    list = State()
    detail = State()
    material = State()


class ExcursionEditSG(StatesGroup):
    list = State()
    detail = State()
    material = State()
    edit_title = State()
    edit_description = State()
    edit_material_name = State()
    edit_material = State()
    delete_virtex = State()
    delete_material = State()
