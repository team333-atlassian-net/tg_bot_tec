from aiogram_dialog import Window, Dialog, StartMode
from aiogram_dialog.widgets.kbd import Start, Next
from aiogram_dialog.widgets.text import Const, Format

from states import StartSG, MenuSG

start_window = Window(
    Const("Привет! Это бот для онбординга сотрудников компании ТЭК.\n"
          "Чтобы увидеть доступные команды, перейдите в меню"),
    Start(Const("Меню"), id="start_menu", state=MenuSG.menu, mode=StartMode.NORMAL),
    state=StartSG.start
)


dialog = Dialog(start_window)
