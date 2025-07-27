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


class GuideCreationSG(StatesGroup):
    document = State()
    title = State()
    upload_content = State()
    end = State()


class GuideViewSG(StatesGroup):
    documents = State()
    guides = State()
    guide = State()
    end = State()


class GuideEditSG(StatesGroup):
    documents = State()
    guides = State()
    guide = State()
    edit_title = State()
    edit_doc_name = State()
    edit_content = State()
    delete_doc = State()
    delete_guide = State()
    end = State()
