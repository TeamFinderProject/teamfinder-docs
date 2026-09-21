# API Contracts v1

**Статус:** v1 (для первого чекпоинта)  
**Владелец документа:** Участник 1 (Team Lead / Backend / DevOps)  
**Reviewer:** Участник 2 (PM / System Analyst)

**Связанные документы:**
- `architecture-v1.md`
- `use-cases.md`
- `ui-design.md`

---

## 1. Назначение

API Contracts v1 фиксирует соглашение между frontend и backend TeamFinder.

Документ определяет:

- HTTP-методы и URL endpoint'ов;
- входные данные запросов;
- форматы успешных ответов;
- основные HTTP-коды ошибок;
- требования к авторизации;
- бизнес-правила, влияющие на поведение API.

Контракты описывают внешний интерфейс backend и не являются описанием его внутренней реализации.

---

## 2. Общие соглашения

### 2.1. Базовый префикс

Все endpoint'ы API используют префикс:

```text
/api
```

Пример:

```http
GET /api/projects
```

### 2.2. Формат данных

Основной формат обмена данными между frontend и backend — JSON.

Пример:

```json
{
  "title": "TeamFinder",
  "description": "Сервис для поиска участников в проекты"
}
```

### 2.3. Авторизация

Часть endpoint'ов доступна только авторизованным пользователям.

Backend должен определять текущего пользователя на основании данных авторизации. Frontend не передаёт `userId` для операций, выполняемых от имени текущего пользователя.

Конкретный механизм авторизации (например, token-based или cookie-based authentication) определяется на этапе реализации backend и данным контрактом не фиксируется.

### 2.4. Основные HTTP-коды

| Код | Значение |
|---|---|
| `200 OK` | Запрос успешно выполнен |
| `201 Created` | Новый ресурс успешно создан |
| `204 No Content` | Действие выполнено, тело ответа отсутствует |
| `400 Bad Request` | Некорректные входные данные |
| `401 Unauthorized` | Пользователь не аутентифицирован |
| `403 Forbidden` | Пользователь не имеет прав на действие |
| `404 Not Found` | Ресурс не найден |
| `409 Conflict` | Операция конфликтует с текущим состоянием системы |

### 2.5. Формат ошибки

```json
{
  "code": "ERROR_CODE",
  "message": "Описание ошибки"
}
```

Для ошибок валидации:

```json
{
  "code": "VALIDATION_ERROR",
  "message": "Некорректные входные данные",
  "errors": {
    "email": [
      "Некорректный формат email"
    ]
  }
}
```

---

## 3. Сводная таблица API

### 3.1. Auth и Profile

| Method | Endpoint | Назначение | Доступ |
|---|---|---|---|
| `POST` | `/api/auth/register` | Регистрация | Гость |
| `POST` | `/api/auth/login` | Вход | Гость |
| `POST` | `/api/auth/logout` | Выход | Авторизованный |
| `GET` | `/api/profile` | Получить свой профиль | Авторизованный |
| `PATCH` | `/api/profile` | Изменить свой профиль | Авторизованный |

### 3.2. Dictionaries

| Method | Endpoint | Назначение | Доступ |
|---|---|---|---|
| `GET` | `/api/skills` | Получить справочник навыков | Авторизованный |
| `GET` | `/api/role-types` | Получить справочник типов ролей | Авторизованный |

### 3.3. Projects и Project Roles

| Method | Endpoint | Назначение | Доступ |
|---|---|---|---|
| `GET` | `/api/projects` | Каталог проектов | Авторизованный |
| `GET` | `/api/projects/{projectId}` | Просмотр проекта | Авторизованный |
| `POST` | `/api/projects` | Создать проект | Авторизованный |
| `PATCH` | `/api/projects/{projectId}` | Изменить проект | Владелец |
| `POST` | `/api/projects/{projectId}/roles` | Создать роль проекта | Владелец |
| `PATCH` | `/api/project-roles/{roleId}` | Изменить роль проекта | Владелец |
| `GET` | `/api/project-roles/{roleId}/match` | Получить matching | Авторизованный |

### 3.4. Applications и Team

| Method | Endpoint | Назначение | Доступ |
|---|---|---|---|
| `POST` | `/api/project-roles/{roleId}/applications` | Подать заявку | Авторизованный |
| `GET` | `/api/applications/mine` | Получить свои заявки | Авторизованный |
| `POST` | `/api/applications/{applicationId}/withdraw` | Отозвать заявку | Автор заявки |
| `GET` | `/api/projects/{projectId}/applications` | Получить заявки проекта | Владелец |
| `POST` | `/api/applications/{applicationId}/accept` | Принять заявку | Владелец |
| `POST` | `/api/applications/{applicationId}/reject` | Отклонить заявку | Владелец |
| `GET` | `/api/projects/{projectId}/team` | Получить команду проекта | Владелец / участник |
| `POST` | `/api/projects/{projectId}/team/leave` | Покинуть команду | Участник |
| `DELETE` | `/api/projects/{projectId}/members/{userId}` | Удалить участника | Владелец |

### 3.5. Project Lifecycle

| Method | Endpoint | Назначение | Доступ |
|---|---|---|---|
| `POST` | `/api/projects/{projectId}/recruiting` | Открыть набор | Владелец |
| `POST` | `/api/projects/{projectId}/start` | Начать проект | Владелец |
| `POST` | `/api/projects/{projectId}/complete` | Завершить проект | Владелец |
| `POST` | `/api/projects/{projectId}/cancel` | Отменить проект | Владелец |

---

## 4. Auth

### 4.1. Регистрация

#### `POST /api/auth/register`

Создаёт нового пользователя TeamFinder.

**Доступ:** гость.

#### Request

| Поле | Тип | Обязательное | Описание |
|---|---|:---:|---|
| `email` | string | Да | Email пользователя |
| `password` | string | Да | Пароль пользователя |
| `displayName` | string | Да | Отображаемое имя |

```json
{
  "email": "user@example.com",
  "password": "password",
  "displayName": "Evgen"
}
```

#### Response — `201 Created`

```json
{
  "id": 7,
  "email": "user@example.com",
  "displayName": "Evgen"
}
```

#### Ошибки

| Код | Причина |
|---|---|
| `400 Bad Request` | Некорректные регистрационные данные |
| `409 Conflict` | Пользователь с таким email уже существует |

> Пароль не должен храниться в базе данных в открытом виде.

---

### 4.2. Вход

#### `POST /api/auth/login`

Выполняет аутентификацию пользователя.

**Доступ:** гость.

#### Request

| Поле | Тип | Обязательное | Описание |
|---|---|:---:|---|
| `email` | string | Да | Email пользователя |
| `password` | string | Да | Пароль пользователя |

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

#### Response — `200 OK`

```json
{
  "user": {
    "id": 7,
    "email": "user@example.com",
    "displayName": "Evgen"
  }
}
```

Данные для поддержания авторизованной сессии зависят от выбранного механизма авторизации.

#### Ошибки

| Код | Причина |
|---|---|
| `400 Bad Request` | Некорректный формат запроса |
| `401 Unauthorized` | Неверный email или пароль |

---

### 4.3. Выход

#### `POST /api/auth/logout`

Завершает текущую авторизованную сессию.

**Доступ:** авторизованный пользователь.

#### Response — `204 No Content`

---

## 5. Profile

### 5.1. Получить свой профиль

#### `GET /api/profile`

Возвращает профиль текущего пользователя.

**Доступ:** авторизованный пользователь.

#### Response — `200 OK`

```json
{
  "id": 7,
  "displayName": "Evgen",
  "about": "Backend developer",
  "interestedRoles": [
    {
      "roleTypeId": 1,
      "name": "Backend Developer"
    }
  ],
  "skills": [
    {
      "skillId": 1,
      "name": "C#",
      "level": "Intermediate"
    }
  ]
}
```

#### Ошибки

| Код | Причина |
|---|---|
| `401 Unauthorized` | Пользователь не авторизован |

---

### 5.2. Изменить профиль

#### `PATCH /api/profile`

Частично изменяет профиль текущего пользователя.

**Доступ:** авторизованный пользователь.

#### Request

| Поле | Тип | Обязательное | Описание |
|---|---|:---:|---|
| `displayName` | string | Нет | Отображаемое имя |
| `about` | string | Нет | Информация о пользователе |
| `interestedRoleTypeIds` | array | Нет | Интересующие типы ролей |
| `skills` | array | Нет | Навыки пользователя |

```json
{
  "displayName": "Evgen",
  "about": "Backend developer, изучаю ASP.NET Core",
  "interestedRoleTypeIds": [1],
  "skills": [
    {
      "skillId": 1,
      "level": "Intermediate"
    },
    {
      "skillId": 2,
      "level": "Beginner"
    }
  ]
}
```

Допустимые уровни навыков:

| Значение | Описание |
|---|---|
| `Beginner` | Начальный уровень |
| `Intermediate` | Средний уровень |
| `Advanced` | Продвинутый уровень |

#### Response — `200 OK`

Возвращает обновлённый профиль.

#### Ошибки

| Код | Причина |
|---|---|
| `400 Bad Request` | Некорректные данные |
| `401 Unauthorized` | Пользователь не авторизован |
| `404 Not Found` | Skill или role type не существует |
| `409 Conflict` | Один skill указан несколько раз |

---

## 6. Dictionaries

### 6.1. Получить навыки

#### `GET /api/skills`

Возвращает справочник доступных навыков.

**Доступ:** авторизованный пользователь.

#### Response — `200 OK`

```json
[
  {
    "id": 1,
    "name": "C#"
  },
  {
    "id": 2,
    "name": "ASP.NET Core"
  },
  {
    "id": 3,
    "name": "PostgreSQL"
  }
]
```

### 6.2. Получить типы ролей

#### `GET /api/role-types`

Возвращает справочник типов ролей.

**Доступ:** авторизованный пользователь.

#### Response — `200 OK`

```json
[
  {
    "id": 1,
    "name": "Backend Developer"
  },
  {
    "id": 2,
    "name": "Frontend Developer"
  },
  {
    "id": 3,
    "name": "Designer"
  }
]
```

---

## 7. Projects

### 7.1. Получить каталог проектов

#### `GET /api/projects`

Возвращает проекты, доступные в каталоге.

**Доступ:** авторизованный пользователь.

#### Query parameters

| Параметр | Тип | Обязательный | Описание |
|---|---|:---:|---|
| `type` | string | Нет | Фильтр по типу проекта |
| `skillId` | integer | Нет | Фильтр по требуемому навыку |

Пример:

```http
GET /api/projects?type=PET_PROJECT&skillId=1
```

#### Response — `200 OK`

```json
[
  {
    "id": 42,
    "title": "TeamFinder",
    "description": "Сервис для поиска участников в проекты",
    "type": "PET_PROJECT",
    "state": "RECRUITING"
  }
]
```

---

### 7.2. Получить проект

#### `GET /api/projects/{projectId}`

Возвращает информацию о проекте и его ролях.

**Доступ:** авторизованный пользователь.

#### Response — `200 OK`

```json
{
  "id": 42,
  "title": "TeamFinder",
  "description": "Сервис для поиска участников в проекты",
  "type": "PET_PROJECT",
  "state": "RECRUITING",
  "owner": {
    "id": 7,
    "displayName": "Evgen"
  },
  "roles": [
    {
      "id": 15,
      "name": "Backend Developer",
      "capacity": 1,
      "acceptedCount": 0
    }
  ]
}
```

#### Ошибки

| Код | Причина |
|---|---|
| `401 Unauthorized` | Пользователь не авторизован |
| `404 Not Found` | Проект не найден |

---

### 7.3. Создать проект

#### `POST /api/projects`

Создаёт новый проект.

**Доступ:** авторизованный пользователь.

Текущий пользователь автоматически становится владельцем проекта. Начальное состояние — `DRAFT`.

#### Request

| Поле | Тип | Обязательное | Описание |
|---|---|:---:|---|
| `title` | string | Да | Название проекта |
| `description` | string | Да | Описание проекта |
| `type` | string | Да | Тип проекта |

```json
{
  "title": "TeamFinder",
  "description": "Сервис для поиска участников в проекты",
  "type": "PET_PROJECT"
}
```

#### Response — `201 Created`

```json
{
  "id": 42,
  "title": "TeamFinder",
  "description": "Сервис для поиска участников в проекты",
  "type": "PET_PROJECT",
  "state": "DRAFT",
  "ownerId": 7
}
```

---

### 7.4. Изменить проект

#### `PATCH /api/projects/{projectId}`

Изменяет основные данные проекта.

**Доступ:** владелец проекта.

#### Request

```json
{
  "title": "TeamFinder v1",
  "description": "Обновлённое описание проекта"
}
```

#### Ошибки

| Код | Причина |
|---|---|
| `400 Bad Request` | Некорректные данные |
| `401 Unauthorized` | Пользователь не авторизован |
| `403 Forbidden` | Пользователь не является владельцем проекта |
| `404 Not Found` | Проект не найден |

---

## 8. Project Roles

### 8.1. Создать роль проекта

#### `POST /api/projects/{projectId}/roles`

Создаёт роль, на которую проект ищет участников.

**Доступ:** владелец проекта.

#### Request

| Поле | Тип | Обязательное | Описание |
|---|---|:---:|---|
| `roleTypeId` | integer | Да | Тип роли |
| `name` | string | Да | Название роли |
| `description` | string | Да | Описание роли |
| `capacity` | integer | Да | Количество мест |
| `requiredSkills` | array | Нет | Обязательные навыки |
| `niceToHaveSkills` | array | Нет | Желательные навыки |

```json
{
  "roleTypeId": 1,
  "name": "Backend Developer",
  "description": "Разработка backend на ASP.NET Core",
  "capacity": 1,
  "requiredSkills": [
    {
      "skillId": 1,
      "level": "Intermediate"
    }
  ],
  "niceToHaveSkills": [
    {
      "skillId": 3,
      "level": "Beginner"
    }
  ]
}
```

#### Response — `201 Created`

```json
{
  "id": 15,
  "projectId": 42,
  "roleTypeId": 1,
  "name": "Backend Developer",
  "description": "Разработка backend на ASP.NET Core",
  "capacity": 1
}
```

---

### 8.2. Изменить роль проекта

#### `PATCH /api/project-roles/{roleId}`

Изменяет параметры существующей роли.

**Доступ:** владелец проекта.

После появления заявок ключевые требования роли блокируются от изменения. Описание роли может изменяться. `capacity` можно увеличивать, но нельзя уменьшать ниже количества уже принятых участников.

#### Ошибки

| Код | Причина |
|---|---|
| `400 Bad Request` | Некорректные данные |
| `401 Unauthorized` | Пользователь не авторизован |
| `403 Forbidden` | Пользователь не является владельцем проекта |
| `404 Not Found` | Роль не найдена |
| `409 Conflict` | Изменение нарушает бизнес-правила роли |

---

## 9. Matching

### 9.1. Получить matching для роли

#### `GET /api/project-roles/{roleId}/match`

Сравнивает навыки текущего пользователя с требованиями конкретной роли.

**Доступ:** авторизованный пользователь.

Matching является рекомендательным. В v1 не используется ML и не рассчитывается искусственный процент соответствия.

#### Response — `200 OK`

```json
{
  "required": [
    {
      "skill": "C#",
      "requiredLevel": "Intermediate",
      "userLevel": "Intermediate",
      "matched": true
    },
    {
      "skill": "PostgreSQL",
      "requiredLevel": "Beginner",
      "userLevel": "Intermediate",
      "matched": true
    }
  ],
  "niceToHave": [
    {
      "skill": "Docker",
      "requiredLevel": "Beginner",
      "userLevel": null,
      "matched": false
    }
  ],
  "summary": {
    "requiredMatched": 2,
    "requiredTotal": 2,
    "niceToHaveMatched": 0,
    "niceToHaveTotal": 1
  }
}
```

---

## 10. Applications

### 10.1. Подать заявку

#### `POST /api/project-roles/{roleId}/applications`

Создаёт заявку текущего пользователя на роль.

**Доступ:** авторизованный пользователь.

#### Request

| Поле | Тип | Обязательное | Описание |
|---|---|:---:|---|
| `comment` | string | Нет | Комментарий кандидата |

```json
{
  "comment": "Хочу присоединиться к проекту и заниматься backend."
}
```

Начальное состояние заявки — `PENDING`.

#### Response — `201 Created`

```json
{
  "id": 101,
  "projectRoleId": 15,
  "status": "PENDING",
  "comment": "Хочу присоединиться к проекту и заниматься backend."
}
```

#### Бизнес-правила

- один пользователь может иметь только одну заявку на конкретную роль;
- пользователь может подавать заявки на разные роли одного проекта;
- повторная заявка на ту же роль после `REJECTED`, `WITHDRAWN` или `CLOSED` в v1 не создаётся;
- создание заявки не занимает место в `capacity`;
- отсутствие части required skills само по себе не запрещает подачу заявки.

---

### 10.2. Получить свои заявки

#### `GET /api/applications/mine`

Возвращает заявки текущего пользователя.

**Доступ:** авторизованный пользователь.

#### Response — `200 OK`

```json
[
  {
    "id": 101,
    "projectId": 42,
    "projectTitle": "TeamFinder",
    "projectRoleId": 15,
    "roleName": "Backend Developer",
    "status": "PENDING"
  }
]
```

---

### 10.3. Отозвать заявку

#### `POST /api/applications/{applicationId}/withdraw`

Позволяет кандидату отозвать свою заявку.

**Доступ:** автор заявки.

#### Response — `200 OK`

```json
{
  "id": 101,
  "status": "WITHDRAWN"
}
```

#### Ошибки

| Код | Причина |
|---|---|
| `401 Unauthorized` | Пользователь не авторизован |
| `403 Forbidden` | Заявка принадлежит другому пользователю |
| `404 Not Found` | Заявка не найдена |
| `409 Conflict` | Заявку нельзя отозвать в текущем состоянии |

---

### 10.4. Получить заявки проекта

#### `GET /api/projects/{projectId}/applications`

Возвращает заявки на роли проекта.

**Доступ:** владелец проекта.

#### Response — `200 OK`

```json
[
  {
    "id": 101,
    "status": "PENDING",
    "role": {
      "id": 15,
      "name": "Backend Developer"
    },
    "candidate": {
      "id": 12,
      "displayName": "Alex"
    },
    "comment": "Хочу заниматься backend."
  }
]
```

---

### 10.5. Принять заявку

#### `POST /api/applications/{applicationId}/accept`

Принимает заявку кандидата.

**Доступ:** владелец проекта.

При успешном принятии:

1. `Application` получает состояние `ACCEPTED`;
2. создаётся `Membership`;
3. место в `capacity` считается занятым;
4. другие `PENDING`-заявки пользователя в этом проекте закрываются.

Проверка свободного места выполняется непосредственно при принятии заявки.

#### Response — `200 OK`

```json
{
  "applicationId": 101,
  "status": "ACCEPTED",
  "membershipId": 55
}
```

#### Ошибки

| Код | Причина |
|---|---|
| `401 Unauthorized` | Пользователь не авторизован |
| `403 Forbidden` | Пользователь не является владельцем проекта |
| `404 Not Found` | Заявка не найдена |
| `409 Conflict` | Заявка обработана, роль заполнена или операция недоступна |

---

### 10.6. Отклонить заявку

#### `POST /api/applications/{applicationId}/reject`

Отклоняет заявку кандидата.

**Доступ:** владелец проекта.

#### Response — `200 OK`

```json
{
  "applicationId": 101,
  "status": "REJECTED"
}
```

---

## 11. Team

### 11.1. Получить команду проекта

#### `GET /api/projects/{projectId}/team`

Возвращает владельца и участников проекта.

**Доступ:** владелец проекта или участник команды.

#### Response — `200 OK`

```json
{
  "owner": {
    "id": 7,
    "displayName": "Evgen"
  },
  "members": [
    {
      "userId": 12,
      "displayName": "Alex",
      "roleId": 15,
      "roleName": "Backend Developer"
    }
  ]
}
```

Владелец хранится отдельно от `Membership` и автоматически не занимает место в `capacity` роли.

---

### 11.2. Покинуть команду

#### `POST /api/projects/{projectId}/team/leave`

Текущий участник покидает команду проекта.

**Доступ:** участник команды.

#### Response — `204 No Content`

---

### 11.3. Удалить участника

#### `DELETE /api/projects/{projectId}/members/{userId}`

Владелец удаляет участника из команды.

**Доступ:** владелец проекта.

#### Response — `204 No Content`

#### Ошибки

| Код | Причина |
|---|---|
| `401 Unauthorized` | Пользователь не авторизован |
| `403 Forbidden` | Пользователь не является владельцем проекта |
| `404 Not Found` | Проект или участник не найден |
| `409 Conflict` | Действие невозможно в текущем состоянии |

---

## 12. Project Lifecycle

### 12.1. Основной жизненный цикл

```text
DRAFT → RECRUITING → IN_PROGRESS → COMPLETED
```

Проект также может перейти в `CANCELLED`, если отмена разрешена из его текущего состояния.

### 12.2. Открыть набор

#### `POST /api/projects/{projectId}/recruiting`

Переводит проект из `DRAFT` в `RECRUITING`.

**Доступ:** владелец проекта.

#### Response — `200 OK`

```json
{
  "id": 42,
  "state": "RECRUITING"
}
```

### 12.3. Начать проект

#### `POST /api/projects/{projectId}/start`

Переводит проект из `RECRUITING` в `IN_PROGRESS`.

**Доступ:** владелец проекта.

Владелец может начать проект до заполнения всех ролей. После завершения набора оставшиеся `PENDING`-заявки закрываются.

#### Response — `200 OK`

```json
{
  "id": 42,
  "state": "IN_PROGRESS"
}
```

### 12.4. Завершить проект

#### `POST /api/projects/{projectId}/complete`

Переводит проект из `IN_PROGRESS` в `COMPLETED`.

**Доступ:** владелец проекта.

#### Response — `200 OK`

```json
{
  "id": 42,
  "state": "COMPLETED"
}
```

### 12.5. Отменить проект

#### `POST /api/projects/{projectId}/cancel`

Переводит проект в `CANCELLED`, если переход разрешён.

**Доступ:** владелец проекта.

Активные `PENDING`-заявки закрываются.

#### Response — `200 OK`

```json
{
  "id": 42,
  "state": "CANCELLED"
}
```

#### Общие ошибки lifecycle-операций

| Код | Причина |
|---|---|
| `401 Unauthorized` | Пользователь не авторизован |
| `403 Forbidden` | Пользователь не является владельцем проекта |
| `404 Not Found` | Проект не найден |
| `409 Conflict` | Переход из текущего состояния недопустим |

---

## 13. Состояния системы

### 13.1. Project State

| State | Значение |
|---|---|
| `DRAFT` | Проект создаётся и настраивается |
| `RECRUITING` | Открыт набор участников |
| `IN_PROGRESS` | Проект выполняется |
| `COMPLETED` | Проект завершён |
| `CANCELLED` | Проект отменён |

### 13.2. Application Status

| Status | Значение |
|---|---|
| `PENDING` | Заявка ожидает решения |
| `ACCEPTED` | Кандидат принят |
| `REJECTED` | Заявка отклонена |
| `WITHDRAWN` | Кандидат отозвал заявку |
| `CLOSED` | Заявка автоматически закрыта |

### 13.3. Skill Level

| Level | Значение |
|---|---|
| `Beginner` | Начальный |
| `Intermediate` | Средний |
| `Advanced` | Продвинутый |

---

## 14. Ключевые бизнес-правила

| № | Правило |
|---:|---|
| 1 | `Application` и `Membership` являются разными сущностями |
| 2 | Подача заявки не занимает место в роли |
| 3 | Место в `capacity` занимает только принятый участник (`Membership`) |
| 4 | При принятии заявки backend повторно проверяет наличие свободного места |
| 5 | Один пользователь не может создать несколько заявок на одну роль |
| 6 | Пользователь может подаваться на разные роли одного проекта |
| 7 | После принятия пользователя на одну роль остальные его `PENDING`-заявки в этом проекте закрываются |
| 8 | В v1 повторная заявка на ту же роль после `REJECTED`, `WITHDRAWN` или `CLOSED` не создаётся |
| 9 | После появления заявок ключевые требования роли блокируются от изменения |
| 10 | `capacity` нельзя уменьшить ниже количества уже принятых участников |
| 11 | Владелец проекта хранится отдельно и автоматически не занимает место в роли |
| 12 | Владелец может начать проект до заполнения всех ролей |
| 13 | После завершения набора оставшиеся `PENDING`-заявки закрываются |
| 14 | Matching является рекомендательным и объяснимым |
| 15 | Matching v1 не использует ML и не рассчитывает процент соответствия |
| 16 | Для коммуникации участников используются внешние контактные данные; встроенный чат не входит в v1 |

---

## 15. Границы API Contracts v1

| Возможность | Статус |
|---|---|
| Встроенный чат | Future |
| Telegram-автоматизация | Future |
| Система рейтинга и репутации | Future |
| Анализ токсичности / sentiment analysis | Future |
| ML-рекомендации | Future |
| Сложный процентный matching | Future |
| Автоматические skill tests | Future |
| Внутренние tasks / milestones | Future |
| Расширенная система уведомлений | Future |

---

## 16. Примечание по согласованию

После подготовки ERD v1 названия сущностей и полей API должны быть сверены с моделью данных.

При расхождениях между API Contracts v1, ERD v1, Use Cases v1 и UI Design v1 изменения согласуются отдельным commit / Pull Request.