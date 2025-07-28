
from aiogram_dialog import Window, StartMode, Dialog
from aiogram_dialog.widgets.kbd import Start, SwitchTo, Button, Cancel
from aiogram_dialog.widgets.text import Const

from dialogs.auth.logout.handlers import on_logout_click
from states import LogoutSG

logout_window = Window(
    Const("Уверены, что хотите выйти?"),
    Button(Const("Да, выйти"), id="logout_btn", on_click=on_logout_click),
    Cancel(Const("❌ Отмена")),
    state=LogoutSG.logout
)

dialog = Dialog(logout_window)