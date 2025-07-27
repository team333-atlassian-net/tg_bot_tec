import asyncio
from datetime import date, time
from db import async_session_maker
from sqlalchemy import select, func
from models import FAQ, Canteen, CanteenMenu, CompanyInfo, ExcursionMaterial, FAQKeyWords, Event, Guide, OrganizationalStructure, VirtualExcursion
# from models import Feedback, FeedbackAttachments


### Данные без фотографий\файлов

async def add_faq_data():
    async with async_session_maker() as session:
        count = await session.scalar(select(func.count()).select_from(FAQ))
        if count > 0:
            print("FAQ уже заполнены — пропуск")
            return
        
        faqs = [
            {
                "question": "Как оформить отпуск?",
                "answer": "Заполните заявление и передайте его руководителю.",
                "category": "Кадры",
                "keywords": ["отпуск", "заявление", "оформление"]
            },
            {
                "question": "Как получить справку 2-НДФЛ?",
                "answer": "Обратитесь в бухгалтерию или оформите через портал.",
                "category": "Бухгалтерия",
                "keywords": ["справка", "2-НДФЛ", "бухгалтерия"]
            },
            {
                "question": "Можно ли работать удалённо?",
                "answer": "Удалённый формат возможен по согласованию с руководителем.",
                "category": "HR",
                "keywords": ["удалёнка", "работа из дома", "дистанционно"]
            },
        ]

        for entry in faqs:
            faq = FAQ(
                question=entry["question"],
                answer=entry["answer"],
                category=entry["category"]
            )
            session.add(faq)
            await session.flush()  # получить ID до коммита

            for word in entry["keywords"]:
                keyword = FAQKeyWords(faq_id=faq.id, word=word)
                session.add(keyword)

        await session.commit()
        print("FAQ и ключевые слова добавлены")

async def add_events_data():
    async with async_session_maker() as session:
        count = await session.scalar(select(func.count()).select_from(Event))
        if count > 0:
            print("Мероприятия уже заполнены — пропуск")
            return
        
        events = [
            {
                "title": "День открытых дверей",
                "description": "Приглашаем всех желающих посетить наш офис и познакомиться с командой."
            },
            {
                "title": "Тимбилдинг на природе",
                "description": "Командный выезд за город с играми и мастер-классами."
            },
            {
                "title": "Вебинар: Карьера в IT",
                "description": "Онлайн-встреча с экспертами по карьерному росту."
            },
            {
                "title": "Курс по безопасности",
                "description": "Обязательный тренинг по информационной безопасности для всех сотрудников."
            },
        ]

        for event in events:
            event = Event(
                title=event["title"],
                description=event["description"]
            )
            session.add(event)

        await session.commit()
        print("Мероприятия добавлены")

async def add_canteen_info():
    async with async_session_maker() as session:
        count = await session.scalar(select(func.count()).select_from(Canteen))

        if count > 0:
            print("Информация о столовой уже заполнена — пропуск")
            return
        canteen = Canteen(
            start_time=time(8, 0),         
            end_time=time(18, 0),         
            description="Столовая работает в будни. Оплата по карте или QR."
        )
        session.add(canteen)

        count_menu = await session.scalar(select(func.count()).select_from(CanteenMenu))
        if count > 0:
            count_menu("Меню уже заполнено — пропуск")
            await session.commit()
            return
        
        canteen_menu = [
            {
                "date": date(2025, 8, 1),
                "file_id": "AgACAgIAAxkBAAIL6WiAq9pmf6OvsHnMK47M-_aArvIYAAJYITIbO9wBSKmd52XhmEmMAQADAgADeQADNgQ",
                "file_type":"PHOTO",
                "menu": None,
            },
            {
                "date": date(2025, 8, 3),
                "file_id": None,
                "file_type": None,
                "menu": "1. Борщ\n2. Котлета с пюре\n3. Компот",
            },
        ]

        for menu in canteen_menu:
            cm = CanteenMenu(
                date=menu["date"],
                file_id=menu["file_id"],
                file_type=menu["file_type"],
                menu=menu["menu"]
            )
            session.add(cm)
        await session.commit()
        print("Данные о столовой добавлены")


### Данные с файлами

async def add_company_info():
    async with async_session_maker() as session:
        count = await session.scalar(select(func.count()).select_from(CompanyInfo))
        if count > 0:
            print("Информация о компании уже заполнена — пропуск")
            return
        company_info = [
            {
                "title": "Мы - компания ТЭК",
                "content": None,
                "file_path": None,
                "image_path": None
            },
            {
                "title": "История компании",
                "content": "В 1999 году было создано Научно-производственное предприятие «Томская электронная компания» (ООО НПП «ТЭК»).",
                "file_path": None,
                "image_path": "AgACAgIAAxkBAAIGHGhszK1aI148H61tpMPsbmdZru79AALY6zEbnvdoSxURqvUNs-ApAQADAgADeQADNgQ"
            },
            {
                "title": "Карта офиса",
                "content": "Расположение офисов по этажам наглядно показано в файле",
                "file_path": "BQACAgIAAxkBAAIGP2hs1RbDHLYUTVAd0GHVf8bSJeFhAAICcQACnvdoS0uJqaJjglXsNgQ",
                "image_path": None
            },
        ]

        for ci in company_info:
            comp_info = CompanyInfo(
                title=ci["title"],
                content=ci["content"],
                file_path=ci["file_path"],
                image_path=ci["image_path"]
            )
            session.add(comp_info)

        await session.commit()
        print("Информация о компании добавлена")


# async def add_feedback_data():
#     async with async_session_maker() as session:
        # count = await session.scalar(select(func.count()).select_from(Feedback))

        # if count > 0:
        #     print("Экскурсии уже заполнены — пропуск")
        #     return
#         user_id = await session.scalar(
#             select(User).where(User.pin_code == "12345")
#         )

#         feedback1 = Feedback(
#             user_id=user_id,
#             text="Бот работает отлично, но хотелось бы больше интерактива.",
#             is_read=False
#         )
#         await session.flush()

#         attachments1 = [
#             FeedbackAttachments(
#                 feedback_id=feedback1.id,
#                 file_id=None
#             )
#         ]

#         # Отзыв без вложений
#         feedback2 = Feedback(
#             user_id=user_id,
#             text="Спасибо за бота! Очень полезная штука.",
#             is_read=True
#         )

#         session.add(feedback1)
#         session.add(feedback2)
#         await session.commit()
#         print("Отзывы добавлены")

async def add_virtex_data():
    async with async_session_maker() as session:
        count = await session.scalar(select(func.count()).select_from(VirtualExcursion))

        if count > 0:
            print("Экскурсии уже заполнены — пропуск")
            return
        
        excursion1 = VirtualExcursion(
            title="Виртуальная экскурсия по офису",
            description="Познакомьтесь с офисом и инфраструктурой компании."
        )
        session.add(excursion1)
        await session.flush()

        materials1 = [
            ExcursionMaterial(
                excursion_id=excursion1.id,
                telegram_file_id="BQACAgIAAxkBAAIGP2hs1RbDHLYUTVAd0GHVf8bSJeFhAAICcQACnvdoS0uJqaJjglXsNgQ",
                name="Фасад офиса",
                text=None
            ),
            ExcursionMaterial(
                excursion_id=excursion1.id,
                telegram_file_id=None,
                name="Планировка этажей",
                text="Вот такая планировка этажей"
            )
        ]

        excursion2 = VirtualExcursion(
            title="Завод и производственные цеха",
            description="Узнайте, как устроено наше производство."
        )
        session.add(excursion2)
        await session.flush()

        materials2 = ExcursionMaterial(
                excursion_id=excursion2.id,
                telegram_file_id=None,
                name="Описание технологического процесса",
                text="Цех №1 занимается обработкой металла, далее изделие поступает на сборочную линию..."
            )

        session.add_all(materials1)
        session.add(materials2)
        await session.commit()
        print("Экскурсии и материалы добавлены")

async def add_org_structure():
    async with async_session_maker() as session:
        count = await session.scalar(select(func.count()).select_from(OrganizationalStructure))
        if count > 0:
            print("Оргструктура уже заполнена — пропуск")
            return
        org_structure = OrganizationalStructure(
            title="Структура компании",         
            content="Описание организационной структуры компании: отделы, подразделения, руководство.",         
            file_id=None
        )
        session.add(org_structure)
        await session.commit()
        print("Организационная структура добавлена")

async def add_guides_data():
    async with async_session_maker() as session:
        count = await session.scalar(select(func.count()).select_from(Guide))
        if count > 0:
            print("Гайды уже заполнены — пропуск")
            return
        guides = [
            {
                "document": "Заявление на отпуск",
                "title": "Шаблон заявления на отпуск",
                "text": None,
                "file_id": "BQACAgIAAxkBAAIMbGiGG_WQ2FljxM83sQABwyCe8jHuAwAC4HsAApUNMEiKQaGM6t9G0DYE"
            },
            {
                "document": "Заявление на отпуск",
                "title": "Инструкция по заполнению",
                "text": "1. берем заявление 2. и заполняем",
                "file_id": None
            }
        ]
        for guide in guides:
            g = Guide(
                document=guide["document"],
                title=guide["title"],
                text=guide["text"],
                file_id=guide["file_id"],
            )
            session.add(g)
        await session.commit()
        print("Гайды добавлены")


if __name__ == "__main__":
    async def main():
        await add_faq_data()
        await add_events_data()
        await add_canteen_info()
        await add_company_info()
        await add_virtex_data()
        await add_org_structure()
        await add_guides_data()
        # await add_feedback_data()

    asyncio.run(main())
