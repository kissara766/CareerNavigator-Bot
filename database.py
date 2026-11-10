import aiosqlite
from config import DB_NAME


# ── Создание таблицы ───────────────────────────────────────────────
async def init_db():
    """Создаёт таблицу careers, если её ещё нет."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS careers (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                title           TEXT NOT NULL,
                category        TEXT NOT NULL,
                target_audience TEXT NOT NULL,
                description     TEXT NOT NULL,
                skills_required TEXT NOT NULL,
                avg_salary      TEXT NOT NULL,
                first_steps     TEXT NOT NULL
            )
        """)
        await db.commit()


# ── Стартовое наполнение ───────────────────────────────────────────
INITIAL_CAREERS = [
    # IT
    ("Python-разработчик", "IT", "all",
     "Пишет бэкенд для сайтов, ботов и сервисов, автоматизирует рутину.",
     "Python, Git, SQL",
     "от 80 000 ₽",
     "1. Выучить базовый синтаксис Python\n2. Написать Telegram-бота\n3. Освоить Git и выложить код на GitHub"),
    ("Frontend-разработчик", "IT", "teen",
     "Делает то, что видит пользователь в браузере: кнопки, анимации, формы.",
     "HTML, CSS, JavaScript, React",
     "от 70 000 ₽",
     "1. Сверстать статичную страницу на HTML/CSS\n2. Оживить её на JavaScript\n3. Собрать мини-проект на React"),
    ("Аналитик данных", "IT", "adult",
     "Превращает сырые данные в графики и выводы, на которых бизнес принимает решения.",
     "SQL, Excel, Python, статистика",
     "от 90 000 ₽",
     "1. Освоить SQL и сводные таблицы в Excel\n2. Научиться строить дашборды\n3. Разобрать реальный датасет и сделать отчёт"),

    # Design
    ("UX/UI-дизайнер", "Design", "all",
     "Проектирует удобные и красивые интерфейсы приложений и сайтов.",
     "Figma, основы типографики, UX-исследования",
     "от 75 000 ₽",
     "1. Изучить Figma\n2. Повторить 3 чужих интерфейса\n3. Собрать первый кейс в портфолио"),
    ("Графический дизайнер", "Design", "teen",
     "Создаёт логотипы, баннеры и фирменный стиль для брендов.",
     "Photoshop, Illustrator, насмотренность",
     "от 55 000 ₽",
     "1. Освоить базовые инструменты редактора\n2. Нарисовать логотип для вымышленного бренда\n3. Выложить работы на Behance"),
    ("Motion-дизайнер", "Design", "adult",
     "Оживляет графику: анимация для рекламы, соцсетей и интерфейсов.",
     "After Effects, основы анимации, тайминг",
     "от 80 000 ₽",
     "1. Изучить After Effects\n2. Сделать короткую анимацию логотипа\n3. Собрать шоурил из 3-4 работ"),

    # Management
    ("Проект-менеджер", "Management", "adult",
     "Ведёт проект от идеи до запуска: сроки, команда, бюджет.",
     "Планирование, коммуникация, Jira/Trello",
     "от 95 000 ₽",
     "1. Изучить методологии (Agile, Scrum)\n2. Повести учебный проект в Trello\n3. Получить сертификат по управлению проектами"),
    ("Продакт-менеджер", "Management", "all",
     "Отвечает за продукт целиком: что делать, для кого и зачем.",
     "Аналитика, работа с гипотезами, коммуникация",
     "от 110 000 ₽",
     "1. Разобрать любимый продукт по методу CustDev\n2. Научиться формулировать гипотезы\n3. Сделать мини-исследование рынка"),
    ("SMM-менеджер", "Management", "teen",
     "Развивает соцсети брендов: контент, реклама, вовлечение аудитории.",
     "Контент-план, копирайтинг, аналитика соцсетей",
     "от 45 000 ₽",
     "1. Завести тематический блог и вести его\n2. Изучить таргетированную рекламу\n3. Собрать статистику роста как кейс"),
]


async def populate_initial_data():
    """Заполняет таблицу стартовыми профессиями один раз (если она пустая)."""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM careers")
        (count,) = await cursor.fetchone()
        if count == 0:
            await db.executemany("""
                INSERT INTO careers
                    (title, category, target_audience, description,
                     skills_required, avg_salary, first_steps)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, INITIAL_CAREERS)
            await db.commit()


# ── Выборка с персонализацией ──────────────────────────────────────
async def get_careers_by_category(category: str, audience: str = "all"):
    """
    Возвращает профессии по категории.
    Персонализация: показываем профессии для конкретной аудитории
    (teen или adult) + универсальные (all).
    """
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT title, description, avg_salary, first_steps
            FROM careers
            WHERE category = ?
              AND target_audience IN (?, 'all')
        """, (category, audience))
        return await cursor.fetchall()


    #─── Профиль пользвателя ─────────────────────────────────────────────
    async def init_user():
        """Таблица для хранения профиля пользователя (если понадобится)."""
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_profile (
                    user_id         INTEGER PRIMARY KEY,
                    name
                    track           TEXT,
                    category        TEXT
                )
            """)
            await db.commit()
