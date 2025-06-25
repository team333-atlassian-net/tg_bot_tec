import io
import pandas as pd
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from dao.faq import add_faq, add_faq_with_excel, find_categories, search_faqs, search_faqs_by_category
from models import FAQ
from utils.auth import require_admin, require_auth

router = Router()

class AddFAQStates(StatesGroup):
    """Состояние для добавления вопроса и ответа в БД"""
    choose_mode = State()
    question = State()
    answer = State()
    category = State()
    waiting_for_file = State()

########################################################################
# Добавление вопроса и ответа в базу
@router.message(F.text.lower() == "добавить faq")
async def start_add_faq(message: Message, state: FSMContext):
    await require_admin(message)

    await message.answer(
        "Как вы хотите добавить FAQ?\n\n"
        "Введите <b>вручную</b> или <b>excel</b>.",
        parse_mode="HTML"
    )
    await state.set_state(AddFAQStates.choose_mode)

@router.message(AddFAQStates.choose_mode)
async def handle_faq_mode_choice(message: Message, state: FSMContext):
    text = message.text.lower()

    if text == "вручную":
        await message.answer("Введите вопрос:")
        await state.set_state(AddFAQStates.question)

    elif text == "excel":
        await message.answer("Пожалуйста, отправьте Excel-файл с вопросами (колонки: question, answer, category).")
        await state.set_state(AddFAQStates.waiting_for_file)

    else:
        await message.answer("❌ Неверный выбор. Введите <b>вручную</b> или <b>excel</b>.", parse_mode="HTML")

############################################################################
@router.message(AddFAQStates.question)
async def faq_question_input(message: Message, state: FSMContext):
    await require_admin(message)
    await state.update_data(question=message.text.strip())
    await message.answer("Введите ответ:")
    await state.set_state(AddFAQStates.answer)

@router.message(AddFAQStates.answer)
async def faq_answer_input(message: Message, state: FSMContext):
    await require_admin(message)
    await state.update_data(answer=message.text.strip())
    await message.answer("Введите категорию (или '-' если без категории):")
    await state.set_state(AddFAQStates.category)

@router.message(AddFAQStates.category)
async def faq_category_input(message: Message, state: FSMContext):
    await require_admin(message)
    data = await state.get_data()
    category = message.text.strip()
    if category == "-":
        category = None

    faq = FAQ(
        question=data["question"],
        answer=data["answer"],
        category=category
    )

    await add_faq(faq)

    await message.answer("✅ Вопрос добавлен в базу.")
    await state.clear()
    
@router.message(AddFAQStates.waiting_for_file, F.document)
async def handle_excel_file(message: Message, state: FSMContext):
    await require_admin(message)
    file = message.document
    if not file.file_name.endswith(".xlsx"):
        await message.answer("Пожалуйста, отправьте Excel-файл с расширением .xlsx")
        return

    file_bytes = await message.bot.download(file)
    df = pd.read_excel(io.BytesIO(file_bytes.read()))

    required_columns = {"question", "answer", "category"}
    if not required_columns.issubset(df.columns):
        await message.answer("❌ В Excel-файле должны быть колонки: question, answer, category")
        return

    added = await add_faq_with_excel(df)

    await message.answer(f"✅ Загружено {added} новых вопросов из Excel.")
##########################################################################
# Поиск по словам и категории
@router.message(F.text.startswith("faq"))
async def handle_faq_search(message: Message):
    await require_auth(message)
    query_text = message.text.strip()[3:].strip()  # Удаляем "faq" и пробел

    if not query_text:
        await message.answer("❓ Введите ваш вопрос после `faq`. Пример: `faq как подать заявление`")
        return

    results = await search_faqs(query_text)

    if not results:
        await message.answer("😔 Не нашлось подходящих ответов. Попробуйте переформулировать запрос.")
        return

    # Показываем максимум 5 результатов
    for faq in results[:5]:
        text = f"❓ <b>{faq.question}</b>\n\n💬 {faq.answer}"
        await message.answer(text, parse_mode="HTML")

#############################################################
# Просмотре всех категорий и вопросов/ответов в ней
@router.message(F.text == "/faq")
async def show_faq_categories(message: Message):
    await require_auth(message)
    categories_raw = await find_categories()

    # Преобразуем: None → "Нет категории"
    categories = [cat if cat is not None else "Нет категории" for cat in categories_raw]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=cat, callback_data=f"faq_category:{cat}")]
        for cat in categories
    ])

    text = (
        "📚 <b>Выберите категорию FAQ:</b>\n\n"
        "🔎 Или введите свой вопрос в формате:\n"
        "<code>faq как оформить отпуск</code>"
    )

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")



@router.callback_query(F.data.startswith("faq_category:"))
async def handle_faq_category(callback: CallbackQuery):
    category = callback.data.split("faq_category:")[1]

    faqs = await search_faqs_by_category(category)

    if not faqs:
        await callback.message.answer(f"❌ В категории «{category}» пока нет вопросов.")
        return

    await callback.message.answer(f"📖 Вопросы в категории: <b>{category}</b>", parse_mode="HTML")

    for faq in faqs:
        text = f"❓ <b>{faq.question}</b>\n\n💬 {faq.answer}"
        await callback.message.answer(text, parse_mode="HTML")

    await callback.answer()
