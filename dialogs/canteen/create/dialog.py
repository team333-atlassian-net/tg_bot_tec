import logging
from datetime import datetime

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Back, Cancel, Row, Button

from dialogs.canteen.create.handlers import *
from dialogs.canteen.create.getters import *
from states import CanteenInfoCreationSG

logger = logging.getLogger(__name__)


choice_window = Window(
    Const("📚 Что вы хотите добавить?"),
    Row(
        Button(
            Const("🏢 Информация о столовой"),
            id="canteen",
            on_click=lambda c, b, m: m.switch_to(CanteenInfoCreationSG.start_time),
        ),
        Button(
            Const("📋 Меню"),
            id="menu",
            on_click=lambda c, b, m: m.switch_to(CanteenInfoCreationSG.menu_date),
        ),
    ),
    Cancel(Const("❌ Отмена")),
    state=CanteenInfoCreationSG.choice,
)

start_time_window = Window(
    Const("⏰ Введите время начала работы (в формате HH:MM):"),
    MessageInput(on_start_time_input),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back_to_choice",
            on_click=lambda c, b, m: m.switch_to(CanteenInfoCreationSG.choice),
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=CanteenInfoCreationSG.start_time,
)

end_time_window = Window(
    Const("⏰ Введите время окончания работы (в формате HH:MM):"),
    MessageInput(on_end_time_input),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back_to_start_time",
            on_click=lambda c, b, m: m.switch_to(CanteenInfoCreationSG.start_time),
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=CanteenInfoCreationSG.end_time,
)

canteen_description_window = Window(
    Const("✍️ Введите описание (необязательно):"),
    MessageInput(on_canteen_description_input),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back_to_end_time",
            on_click=lambda c, b, m: m.switch_to(CanteenInfoCreationSG.end_time),
        ),
        Button(
            Const("➡️ Пропустить"), id="skip_description", on_click=on_description_skip
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=CanteenInfoCreationSG.description,
)

canteen_confirm_window = Window(
    Format(
        "✅ Подтвердите информацию:\n\n"
        "Время начала: {start}\n"
        "Время окончания: {end}\n"
        "Описание: {description}"
    ),
    Button(Const("💾 Сохранить"), id="c_save", on_click=on_canteen_confirm),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back_to_description",
            on_click=lambda c, b, m: m.switch_to(CanteenInfoCreationSG.description),
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=CanteenInfoCreationSG.confirm_canteen,
    getter=get_canteen_confirm_data,
)

menu_date_window = Window(
    Const("📅 Введите дату меню (в формате ГГГГ-ММ-ДД):"),
    MessageInput(on_menu_date_input),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back_to_choice",
            on_click=lambda c, b, m: m.switch_to(CanteenInfoCreationSG.choice),
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=CanteenInfoCreationSG.menu_date,
)

menu_text_window = Window(
    Const("📃 Введите текст меню (необязательно):"),
    MessageInput(on_menu_text_input),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back_to_menu_date",
            on_click=lambda c, b, m: m.switch_to(CanteenInfoCreationSG.menu_date),
        ),
        Button(Const("➡️ Пропустить"), id="skip_menu", on_click=on_menu_skip),
        Cancel(Const("❌ Отмена")),
    ),
    state=CanteenInfoCreationSG.menu_text,
)

menu_file_window = Window(
    Const("📎 Отправьте файл меню (PDF, изображение и т.п.):"),
    MessageInput(on_menu_file_input),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back_to_menu_text",
            on_click=lambda c, b, m: m.switch_to(CanteenInfoCreationSG.menu_text),
        ),
        Button(Const("➡️ Пропустить"), id="skip_file", on_click=on_file_skip),
        Cancel(Const("❌ Отмена")),
    ),
    state=CanteenInfoCreationSG.menu_file,
)

menu_confirm_window = Window(
    Format(
        "✅ Подтвердите меню:\n\n" "Дата: {date}\n" "Меню: {menu}\n" "Файл: {file_name}"
    ),
    Button(Const("💾 Сохранить"), id="m_save", on_click=on_menu_confirm),
    Row(
        Button(
            Const("⬅️ Назад"),
            id="back_to_menu_file",
            on_click=lambda c, b, m: m.switch_to(CanteenInfoCreationSG.menu_file),
        ),
        Cancel(Const("❌ Отмена")),
    ),
    state=CanteenInfoCreationSG.confirm_menu,
    getter=get_menu_confirm_data,
)

dialog = Dialog(
    choice_window,
    start_time_window,
    end_time_window,
    canteen_description_window,
    canteen_confirm_window,
    menu_date_window,
    menu_text_window,
    menu_file_window,
    menu_confirm_window,
)
