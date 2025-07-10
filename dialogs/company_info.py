import logging
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.api.protocols import DialogManager
from aiogram.types import Message
from aiogram_dialog.widgets.input import MessageInput
from aiogram.fsm.state import State, StatesGroup

from dao.company_info import add_company_info

logger = logging.getLogger(__name__)


class AddCompanyInfoSG(StatesGroup):
    """
    Состояния диалога для добавления информации о компании.
    """
    title = State() # ввод заголовка
    content = State() # ввод описания
    file = State() # загрузка файла (PDF/видео)
    image = State() # загрузка изображения (JPG/PNG)


async def on_title_entered(message: Message, widget: TextInput, dialog_manager: DialogManager, value: str):
    """
    Обработчик успешного ввода заголовка.

    Сохраняет заголовок в dialog_data и переключается на состояние ввода описания.
    """
    dialog_manager.dialog_data["title"] = value
    await dialog_manager.switch_to(AddCompanyInfoSG.content)


async def on_content_entered(message: Message, widget: TextInput, dialog_manager: DialogManager, value: str):
    """
    Обработчик успешного ввода описания.

    Сохраняет описание в dialog_data, если введён "-", сохраняет None.
    Переключается на состояние загрузки файла.
    """
    content = value
    dialog_manager.dialog_data["content"] = None if content.strip() == "-" else content
    await dialog_manager.switch_to(AddCompanyInfoSG.file)


async def on_file_received(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    """
    Обработчик загрузки файла или символа "-" вместо файла.

    Если пользователь отправил "-", сохраняет None и переключается на состояние загрузки изображения.
    Если отправлен документ, сохраняет file_id и переключается на загрузку изображения.
    Иначе просит повторить ввод.
    """
    if message.text and message.text.strip() == "-":
        dialog_manager.dialog_data["file_path"] = None
        await dialog_manager.switch_to(AddCompanyInfoSG.image)
        return

    if message.document:
        dialog_manager.dialog_data["file_path"] = message.document.file_id
        await message.answer("✅ Файл сохранён. Теперь отправьте изображение или `-`")
        await dialog_manager.switch_to(AddCompanyInfoSG.image)
        return

    await message.answer("❗ Отправьте документ или `-`")


async def on_image_received(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    """
    Обработчик загрузки изображения или символа "-" вместо изображения.

    Если пользователь отправил "-", сохраняет None.
    Если отправлено фото, сохраняет file_id.
    Если ошибка — просит отправить корректное изображение или "-".

    По завершении сохраняет всю собранную информацию в базу через add_company_info.
    Завершает диалог.
    """
    if message.text and message.text.strip() == "-":
        dialog_manager.dialog_data["image_path"] = None
    elif message.photo:
        dialog_manager.dialog_data["image_path"] = message.photo[-1].file_id
    else:
        await message.answer("❗ Отправьте изображение или `-`")
        return

    await add_company_info(
        title=dialog_manager.dialog_data["title"],
        content=dialog_manager.dialog_data["content"],
        file_path=dialog_manager.dialog_data.get("file_path"),
        image_path=dialog_manager.dialog_data.get("image_path"),
    )

    await message.answer("✅ Информация о компании добавлена.")
    logger.info("Администратор добавил информацию о компании")
    await dialog_manager.done()


add_company_info_dialog = Dialog(
    Window(
        Const("✏️ Введите заголовок:"),
        TextInput(id="title_input", on_success=on_title_entered),
        state=AddCompanyInfoSG.title,
    ),
    Window(
        Const("📝 Введите описание или `-`, если описания нет:"),
        TextInput(id="content_input", on_success=on_content_entered),
        state=AddCompanyInfoSG.content,
    ),
    Window(
        Const("📎 Отправьте файл (PDF/видео) или `-`:"),
        MessageInput(on_file_received),
        state=AddCompanyInfoSG.file,
    ),
    Window(
        Const("🖼 Отправьте изображение (JPG/PNG) или `-`:"),
        MessageInput(on_image_received),
        state=AddCompanyInfoSG.image,
    )
)
