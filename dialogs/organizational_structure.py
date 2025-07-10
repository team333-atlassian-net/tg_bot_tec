import logging
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.api.protocols import DialogManager
from aiogram.types import Message
from aiogram_dialog.widgets.input import MessageInput
from aiogram.fsm.state import State, StatesGroup

from dao.organizational_structure import add_organizational_structure

logger = logging.getLogger(__name__)


class AddOrganizationalStructureSG(StatesGroup):
    """
    Состояния диалога для добавления информации об организационной структуре компании.
    """
    title = State() # ввод заголовка
    content = State() # ввод описания
    file = State() # загрузка файла


async def on_title_entered(message: Message, widget: TextInput, dialog_manager: DialogManager, value: str):
    """
    Обработчик успешного ввода заголовка.

    Сохраняет заголовок в dialog_data и переключается на состояние ввода описания.
    """
    dialog_manager.dialog_data["title"] = value
    await dialog_manager.switch_to(AddOrganizationalStructureSG.content)


async def on_content_entered(message: Message, widget: TextInput, dialog_manager: DialogManager, value: str):
    """
    Обработчик успешного ввода описания.

    Сохраняет описание в dialog_data, если введён "-", сохраняет None.
    Переключается на состояние загрузки файла.
    """
    content = value
    dialog_manager.dialog_data["content"] = None if content.strip() == "-" else content
    await dialog_manager.switch_to(AddOrganizationalStructureSG.file)

async def on_file_received(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    """
    Обработчик загрузки файла или символа "-" вместо файла.

    Если пользователь отправил "-", сохраняет None.
    Если отправлен файл, сохраняет file_id.
    Если ошибка — просит отправить корректный файл или "-".

    По завершении сохраняет всю собранную информацию в базу через add_organizational_structure.
    Завершает диалог.
    """
    if message.text and message.text.strip() == "-":
        dialog_manager.dialog_data["file_id"] = None
    elif message.document:
        dialog_manager.dialog_data["file_id"] = message.document.file_id
    else:
        await message.answer("❗ Отправьте документ или `-`")
        return

    await add_organizational_structure(
        title=dialog_manager.dialog_data["title"],
        content=dialog_manager.dialog_data["content"],
        file_id=dialog_manager.dialog_data.get("file_id"),
    )

    await message.answer("✅ Информация об организационной структуре компании добавлена.")
    logger.info("Администратор добавил информацию об организационной структуре компании")
    await dialog_manager.done()


add_org_structure_dialog = Dialog(
    Window(
        Const("✏️ Введите заголовок:"),
        TextInput(id="title_input", on_success=on_title_entered),
        state=AddOrganizationalStructureSG.title,
    ),
    Window(
        Const("📝 Введите описание или `-`, если описания нет:"),
        TextInput(id="content_input", on_success=on_content_entered),
        state=AddOrganizationalStructureSG.content,
    ),
    Window(
        Const("📎 Отправьте файл (PDF/видео) или `-`:"),
        MessageInput(on_file_received),
        state=AddOrganizationalStructureSG.file,
    )
)
