# Spimex Trading API

FastAPI-сервис для работы с данными торгов (`spimex_trading_results`), кэшированием в Redis и асинхронным доступом к PostgreSQL.

## Требования

- [Docker](https://docs.docker.com/get-docker/) и Docker Compose
- Для сценария с БД на компьютере: установленный PostgreSQL и имеющаяся БД

Склонировать репозиторий:

```sh 
git clone https://github.com/Igor39-dev/FastAPI-section
```

## Подготовка переменных окружения

Скопируйте пример и отредактируйте значения:

```sh
cp .env.example .env
```

Файл `.env` должен лежать в корне проекта рядом с `docker-compose.yml`.

Общие для обоих сценариев переменные:

| Переменная | Описание |
|------------|----------|
| `REDIS_URL` | Для compose по умолчанию: `redis://redis:6379/0` |
| `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | Параметры подключения к PostgreSQL |
| `CACHE_TIMEZONE` | Часовой пояс для логики кэша (например `Europe/Moscow`) |

---

## Вариант 1: PostgreSQL на вашем компьютере, API и Redis в Docker

Подходит, когда Postgres уже установлен локально и в нём нужная база и таблицы.

### Настройка `.env`

- `DB_HOST=host.docker.internal` — адрес хоста из контейнера (Docker Desktop на Windows/macOS; на Linux в compose для сервиса `api` задан `extra_hosts`).
- Остальные `DB_*` — как у вашей локальной базы.

### Настройка PostgreSQL на хосте

Разрешите подключения из Docker к вашему Postgres:

- В `postgresql.conf`: параметр `listen_addresses` (часто достаточно `*` или `localhost` в зависимости от версии и способа установки).
- В `pg_hba.conf`: правило для подсети Docker (например для Docker Desktop часто используются диапазоны вроде `172.16.0.0/12`; точное значение можно уточнить при ошибке подключения по логам).

Без этого контейнер `api` не сможет достучаться до БД на ПК.

### Запуск

Из корня репозитория:

```bash
docker compose up --build -d
```

Поднимутся сервисы **api** и **redis** (контейнер Postgres не используется).

### Остановка

```bash
docker compose down
```

---

## Вариант 2: PostgreSQL, Redis и API в Docker

Все три компонента в контейнерах.

### Настройка `.env`

Раскомментируйте и задайте блок **POSTGRES_*** и согласуйте его с **`DB_*`** (одинаковые пользователь, пароль и имя базы):

```env
POSTGRES_USER=spimex
POSTGRES_PASSWORD=spimex
POSTGRES_DB=spimex

DB_HOST=db
DB_PORT=5432
DB_NAME=spimex
DB_USER=spimex
DB_PASSWORD=spimex

REDIS_URL=redis://redis:6379/0
```

`DB_HOST` должен быть **`db`** — это имя сервиса PostgreSQL в сети Compose.

### Запуск

```bash
docker compose --profile bundled-postgres up --build -d
```

### Первый запуск и данные

Скрипты из `docker/postgres/` выполняются только при **пустом** томе базы. Если том уже создан без таблиц, выполните SQL вручную или пересоздайте том (данные в контейнерной БД будут удалены):

```bash
docker compose --profile bundled-postgres down
docker volume rm fastapi-section_postgres_data_fastapi
```

Имя тома проверьте: `docker volume ls`.

### Остановка

```bash
docker compose --profile bundled-postgres down
```

---

## Проверка после запуска

| Что | Адрес |
|-----|--------|
| Swagger UI | http://localhost:8000/docs |
| OpenAPI JSON | http://localhost:8000/openapi.json |
| Health | http://localhost:8000/health |

Список контейнеров:


Логи API:

```sh
docker compose logs -f api
```

---

