import logging

from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const
from aiogram.types import Message

from dialogs.auth.login.handlers import *
from states import AuthDialogSG

logger = logging.getLogger(__name__)


dialog = Dialog(
    Window(
        Const("Введите ваш ПИН-код для авторизации:"),
        TextInput(id="pin_input", on_success=on_pin_entered),
        state=AuthDialogSG.enter_pin,
    )
)
