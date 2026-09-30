# EduPage — этап 1

Школьная информационная система на Django. Реализованы вход и выход, профиль пользователя, роли и администраторское управление пользователями, классами, предметами, учениками и учителями. Электронный журнал позволяет вести оценки и посещаемость; доступ учителя ограничивается назначенными классами и предметами. Расписание доступно ученикам по классу и учителям по их урокам, а редактируется администратором.

## Запуск

Требуются Python 3.11 или новее и pip.

```bash
cd main
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # Windows: copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Откройте `http://127.0.0.1:8000/`. Django Admin доступен по `/admin/`, школьные справочники — в меню администратора после входа.

Раздел журнала доступен по `/journal/grades/` и `/journal/attendance/`. Расписание находится по `/schedule/`; назначить классы и предметы учителю можно через управление учителями. Выход выполняется POST-запросом из защищённой формы в навигационной панели.

## Проверка

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
```

По умолчанию используется SQLite. Для PostgreSQL установите `DB_ENGINE=postgresql` в `.env` и заполните `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.
