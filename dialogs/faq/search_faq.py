
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Back, Cancel, Row, Select,Radio, ScrollingGroup
from dao.faq import search_faq
from dialogs.faq.view_faq import detail_window_getter


class FAQSearchSG(StatesGroup):
    search_input = State()
    search_results = State()
    detail = State()

async def on_search_input(message: Message, widget, dialog_manager: DialogManager):
    query = message.text.strip()
    if not query:
        await message.answer("❗ Введите поисковый запрос.")
        return
    faqs = await search_faq(query)
    dialog_manager.dialog_data["search_results"] = [(str(f.id), f.question) for f in faqs]
    dialog_manager.dialog_data["query"] = query
    await dialog_manager.switch_to(FAQSearchSG.search_results)


async def get_search_results(dialog_manager: DialogManager, **kwargs):
    return {
        "faqs": dialog_manager.dialog_data.get("search_results", []),
        "query": dialog_manager.dialog_data.get("query", "")
    }

async def on_search_result_selected(callback, widget: Select, manager: DialogManager, selected_id: str):
    manager.dialog_data["selected_faq_id"] = int(selected_id)
    await manager.switch_to(FAQSearchSG.detail)



# Окно ввода запроса
search_input_window = Window(
    Const("🔍 Введите ключевое слово или фразу для поиска FAQ:"),
    MessageInput(on_search_input),
    Cancel(Const("❌ Отмена")),
    state=FAQSearchSG.search_input,
)

# Окно результатов
search_results_window = Window(
    Format("🔎 Результаты по запросу: <b>{query}</b>"),
    ScrollingGroup(
        Radio(
            Format("{item[1]}"),
            Format("{item[1]}"),
            id="search_results_radio",
            items="faqs",
            item_id_getter=lambda x: x[0],
            on_click=on_search_result_selected,
        ),
        id="search_scroll",
        width=1,
        height=5,
    ),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Отмена")),
    ),
    getter=get_search_results,
    state=FAQSearchSG.search_results,
)

# Окно деталей FAQ
search_faq_detail_window = Window(
    Format("📌 <b>{faq.question}</b>\n\n{faq.answer}"),
    Row(
        Back(Const("⬅️ Назад")),
        Cancel(Const("❌ Закрыть"))
    ),
    state=FAQSearchSG.detail,
    getter=detail_window_getter,  # можно переиспользовать
)

faq_search_dialog = Dialog(
    search_input_window,
    search_results_window,
    search_faq_detail_window,
)
