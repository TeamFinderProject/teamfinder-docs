\# API Contracts v1



\*\*Статус:\*\* v1 (для первого чекпоинта)



\*\*Владелец документа:\*\* Участник 1 (Team Lead / Backend / DevOps)



\*\*Reviewer:\*\* Участник 2 (PM / System Analyst)



\*\*Связанные документы:\*\*

\- `architecture-v1.md`

\- `use-cases.md`

\- `ui-design.md`



\---



\## 1. Назначение



API Contracts v1 определяет соглашение между frontend и backend TeamFinder.



Документ фиксирует:



\- HTTP-методы и URL endpoint'ов;

\- входные данные запросов;

\- форматы успешных ответов;

\- основные HTTP-коды и ошибки;

\- ключевые бизнес-ограничения, влияющие на API.



Контракты описывают интерфейс взаимодействия компонентов системы и не являются реализацией backend.



\---



\## 2. Общие соглашения



\### 2.1. Формат API



Базовый префикс API:



```text

/api

```



Для передачи данных используется JSON.



Пример:



```json

{

&#x20; "title": "TeamFinder",

&#x20; "description": "Сервис для поиска участников в проекты"

}

```



\### 2.2. Авторизация



Часть endpoint'ов доступна только авторизованным пользователям.



Конкретный механизм авторизации (например, token-based authentication или cookie-based authentication) определяется при реализации backend и не фиксируется данным контрактом.



Backend должен определять текущего пользователя на основании данных авторизации, а не принимать `userId` от frontend там, где действие выполняется от имени текущего пользователя.



\### 2.3. Основные HTTP-коды



| Код | Значение |

|---|---|

| `200 OK` | Запрос успешно выполнен |

| `201 Created` | Ресурс успешно создан |

| `204 No Content` | Действие выполнено, тело ответа отсутствует |

| `400 Bad Request` | Некорректные входные данные |

| `401 Unauthorized` | Пользователь не авторизован |

| `403 Forbidden` | Пользователь не имеет прав на действие |

| `404 Not Found` | Ресурс не найден |

| `409 Conflict` | Действие конфликтует с текущим состоянием системы |



\### 2.4. Формат ошибки



Общий формат ошибки:



```json

{

&#x20; "code": "ERROR\_CODE",

&#x20; "message": "Описание ошибки"

}

```



Для ошибок валидации допускается дополнительное поле `errors`:



```json

{

&#x20; "code": "VALIDATION\_ERROR",

&#x20; "message": "Некорректные входные данные",

&#x20; "errors": {

&#x20;   "email": \[

&#x20;     "Некорректный формат email"

&#x20;   ]

&#x20; }

}

```



\---



\# 3. Auth



\## 3.1. Регистрация



```http

POST /api/auth/register

```



Создаёт нового пользователя TeamFinder.



\### Request



```json

{

&#x20; "email": "user@example.com",

&#x20; "password": "password",

&#x20; "displayName": "Evgen"

}

```



\### Response — `201 Created`



```json

{

&#x20; "id": 7,

&#x20; "email": "user@example.com",

&#x20; "displayName": "Evgen"

}

```



\### Ошибки



\- `400 Bad Request` — некорректные данные;

\- `409 Conflict` — пользователь с таким email уже существует.



Пароль не должен храниться в базе данных в открытом виде.



\---



\## 3.2. Вход



```http

POST /api/auth/login

```



Выполняет аутентификацию пользователя.



\### Request



```json

{

&#x20; "email": "user@example.com",

&#x20; "password": "password"

}

```



\### Response — `200 OK`



```json

{

&#x20; "user": {

&#x20;   "id": 7,

&#x20;   "email": "user@example.com",

&#x20;   "displayName": "Evgen"

&#x20; }

}

```



Данные, необходимые для поддержания авторизованной сессии, зависят от выбранного механизма авторизации.



\### Ошибки



\- `400 Bad Request` — некорректный запрос;

\- `401 Unauthorized` — неверный email или пароль.



\---



\## 3.3. Выход



```http

POST /api/auth/logout

```



Завершает текущую авторизованную сессию.



Конкретная серверная логика зависит от выбранного механизма авторизации.



\### Response — `204 No Content`



\---



\# 4. Profile



\## 4.1. Получить свой профиль



```http

GET /api/profile

```



Возвращает профиль текущего авторизованного пользователя.



\### Response — `200 OK`



```json

{

&#x20; "id": 7,

&#x20; "displayName": "Evgen",

&#x20; "about": "Backend developer",

&#x20; "interestedRoles": \[

&#x20;   "Backend Developer"

&#x20; ],

&#x20; "skills": \[

&#x20;   {

&#x20;     "skillId": 1,

&#x20;     "name": "C#",

&#x20;     "level": "Intermediate"

&#x20;   }

&#x20; ]

}

```



\### Ошибки



\- `401 Unauthorized` — пользователь не авторизован.



\---



\## 4.2. Изменить профиль



```http

PATCH /api/profile

```



Частично изменяет профиль текущего пользователя.



\### Request



Пример:



```json

{

&#x20; "displayName": "Evgen",

&#x20; "about": "Backend developer, изучаю ASP.NET Core",

&#x20; "interestedRoleTypeIds": \[1],

&#x20; "skills": \[

&#x20;   {

&#x20;     "skillId": 1,

&#x20;     "level": "Intermediate"

&#x20;   },

&#x20;   {

&#x20;     "skillId": 2,

&#x20;     "level": "Beginner"

&#x20;   }

&#x20; ]

}

```



Уровни навыков v1:



```text

Beginner

Intermediate

Advanced

```



\### Response — `200 OK`



Возвращается обновлённый профиль.



\### Ошибки



\- `400 Bad Request` — некорректные данные;

\- `401 Unauthorized` — пользователь не авторизован;

\- `404 Not Found` — указанный skill или role type не существует;

\- `409 Conflict` — один skill указан в профиле несколько раз.



\---



\# 5. Dictionaries



\## 5.1. Получить список навыков



```http

GET /api/skills

```



\### Response — `200 OK`



```json

\[

&#x20; {

&#x20;   "id": 1,

&#x20;   "name": "C#"

&#x20; },

&#x20; {

&#x20;   "id": 2,

&#x20;   "name": "ASP.NET Core"

&#x20; },

&#x20; {

&#x20;   "id": 3,

&#x20;   "name": "PostgreSQL"

&#x20; }

]

```



\---



\## 5.2. Получить типы ролей



```http

GET /api/role-types

```



\### Response — `200 OK`



```json

\[

&#x20; {

&#x20;   "id": 1,

&#x20;   "name": "Backend Developer"

&#x20; },

&#x20; {

&#x20;   "id": 2,

&#x20;   "name": "Frontend Developer"

&#x20; },

&#x20; {

&#x20;   "id": 3,

&#x20;   "name": "Designer"

&#x20; }

]

```



\---



\# 6. Projects



\## 6.1. Получить каталог проектов



```http

GET /api/projects

```



Возвращает проекты, доступные для просмотра в каталоге.



Поддерживаются query parameters для фильтрации.



Пример:



```http

GET /api/projects?type=PET\_PROJECT\&skillId=1

```



\### Response — `200 OK`



```json

\[

&#x20; {

&#x20;   "id": 42,

&#x20;   "title": "TeamFinder",

&#x20;   "description": "Сервис для поиска участников в проекты",

&#x20;   "type": "PET\_PROJECT",

&#x20;   "state": "RECRUITING"

&#x20; }

]

```



\---



\## 6.2. Получить проект



```http

GET /api/projects/{projectId}

```



Возвращает информацию о конкретном проекте и его ролях.



\### Response — `200 OK`



```json

{

&#x20; "id": 42,

&#x20; "title": "TeamFinder",

&#x20; "description": "Сервис для поиска участников в проекты",

&#x20; "type": "PET\_PROJECT",

&#x20; "state": "RECRUITING",

&#x20; "owner": {

&#x20;   "id": 7,

&#x20;   "displayName": "Evgen"

&#x20; },

&#x20; "roles": \[

&#x20;   {

&#x20;     "id": 15,

&#x20;     "name": "Backend Developer",

&#x20;     "capacity": 1,

&#x20;     "acceptedCount": 0

&#x20;   }

&#x20; ]

}

```



\### Ошибки



\- `404 Not Found` — проект не найден.



\---



\## 6.3. Создать проект



```http

POST /api/projects

```



Создаёт новый проект.



Текущий авторизованный пользователь автоматически становится владельцем проекта.



Начальное состояние проекта:



```text

DRAFT

```



\### Request



```json

{

&#x20; "title": "TeamFinder",

&#x20; "description": "Сервис для поиска участников в проекты",

&#x20; "type": "PET\_PROJECT"

}

```



\### Response — `201 Created`



```json

{

&#x20; "id": 42,

&#x20; "title": "TeamFinder",

&#x20; "description": "Сервис для поиска участников в проекты",

&#x20; "type": "PET\_PROJECT",

&#x20; "state": "DRAFT",

&#x20; "ownerId": 7

}

```



\### Ошибки



\- `400 Bad Request` — некорректные данные;

\- `401 Unauthorized` — пользователь не авторизован.



\---



\## 6.4. Изменить проект



```http

PATCH /api/projects/{projectId}

```



Изменяет основные данные проекта.



Доступно владельцу проекта.



\### Request



```json

{

&#x20; "title": "TeamFinder v1",

&#x20; "description": "Обновлённое описание проекта"

}

```



\### Response — `200 OK`



Возвращается обновлённый проект.



\### Ошибки



\- `400 Bad Request` — некорректные данные;

\- `401 Unauthorized` — пользователь не авторизован;

\- `403 Forbidden` — пользователь не является владельцем;

\- `404 Not Found` — проект не найден.



\---



\# 7. Project Roles



\## 7.1. Создать роль проекта



```http

POST /api/projects/{projectId}/roles

```



Создаёт роль, на которую проект ищет участников.



Доступно владельцу проекта.



\### Request



```json

{

&#x20; "roleTypeId": 1,

&#x20; "name": "Backend Developer",

&#x20; "description": "Разработка backend на ASP.NET Core",

&#x20; "capacity": 1,

&#x20; "requiredSkills": \[

&#x20;   {

&#x20;     "skillId": 1,

&#x20;     "level": "Intermediate"

&#x20;   }

&#x20; ],

&#x20; "niceToHaveSkills": \[

&#x20;   {

&#x20;     "skillId": 3,

&#x20;     "level": "Beginner"

&#x20;   }

&#x20; ]

}

```



\### Response — `201 Created`



```json

{

&#x20; "id": 15,

&#x20; "projectId": 42,

&#x20; "roleTypeId": 1,

&#x20; "name": "Backend Developer",

&#x20; "description": "Разработка backend на ASP.NET Core",

&#x20; "capacity": 1

}

```



\### Ошибки



\- `400 Bad Request` — некорректные данные;

\- `401 Unauthorized` — пользователь не авторизован;

\- `403 Forbidden` — пользователь не является владельцем проекта;

\- `404 Not Found` — проект, skill или role type не найден.



\---



\## 7.2. Изменить роль проекта



```http

PATCH /api/project-roles/{roleId}

```



Изменяет параметры роли.



После появления заявок ключевые требования роли блокируются от изменения.



Описание роли может изменяться.



`capacity` может быть увеличен, но не может быть установлен ниже количества уже принятых участников.



\### Ошибки



\- `400 Bad Request` — некорректные данные;

\- `401 Unauthorized` — пользователь не авторизован;

\- `403 Forbidden` — пользователь не является владельцем проекта;

\- `404 Not Found` — роль не найдена;

\- `409 Conflict` — изменение нарушает текущее состояние роли.



\---



\# 8. Matching



\## 8.1. Получить matching для роли



```http

GET /api/project-roles/{roleId}/match

```



Сравнивает навыки текущего пользователя с требованиями конкретной роли.



Matching является рекомендательным и не принимает решение за владельца проекта.



В v1 не используется ML и не рассчитывается искусственный процент соответствия.



\### Response — `200 OK`



```json

{

&#x20; "required": \[

&#x20;   {

&#x20;     "skill": "C#",

&#x20;     "requiredLevel": "Intermediate",

&#x20;     "userLevel": "Intermediate",

&#x20;     "matched": true

&#x20;   },

&#x20;   {

&#x20;     "skill": "PostgreSQL",

&#x20;     "requiredLevel": "Beginner",

&#x20;     "userLevel": "Intermediate",

&#x20;     "matched": true

&#x20;   }

&#x20; ],

&#x20; "niceToHave": \[

&#x20;   {

&#x20;     "skill": "Docker",

&#x20;     "requiredLevel": "Beginner",

&#x20;     "userLevel": null,

&#x20;     "matched": false

&#x20;   }

&#x20; ],

&#x20; "summary": {

&#x20;   "requiredMatched": 2,

&#x20;   "requiredTotal": 2,

&#x20;   "niceToHaveMatched": 0,

&#x20;   "niceToHaveTotal": 1

&#x20; }

}

```



\### Ошибки



\- `401 Unauthorized` — пользователь не авторизован;

\- `404 Not Found` — роль не найдена.



\---



\# 9. Applications



\## 9.1. Подать заявку



```http

POST /api/project-roles/{roleId}/applications

```



Создаёт заявку текущего пользователя на конкретную роль.



\### Request



```json

{

&#x20; "comment": "Хочу присоединиться к проекту и заниматься backend."

}

```



Комментарий является необязательным.



Начальное состояние заявки:



```text

PENDING

```



\### Response — `201 Created`



```json

{

&#x20; "id": 101,

&#x20; "projectRoleId": 15,

&#x20; "status": "PENDING",

&#x20; "comment": "Хочу присоединиться к проекту и заниматься backend."

}

```



\### Бизнес-правила



\- один пользователь может иметь только одну заявку на одну конкретную роль в v1;

\- пользователь может подать заявки на разные роли одного проекта;

\- отклонённую, отозванную или закрытую заявку на ту же роль нельзя создать повторно в v1;

\- создание заявки не занимает место в `capacity`;

\- отсутствие части required skills само по себе не запрещает подачу заявки.



\### Ошибки



\- `400 Bad Request` — некорректные данные;

\- `401 Unauthorized` — пользователь не авторизован;

\- `404 Not Found` — роль не найдена;

\- `409 Conflict` — заявка на эту роль уже существует или набор на неё недоступен.



\---



\## 9.2. Получить свои заявки



```http

GET /api/applications/mine

```



Возвращает заявки текущего пользователя.



\### Response — `200 OK`



```json

\[

&#x20; {

&#x20;   "id": 101,

&#x20;   "projectId": 42,

&#x20;   "projectTitle": "TeamFinder",

&#x20;   "projectRoleId": 15,

&#x20;   "roleName": "Backend Developer",

&#x20;   "status": "PENDING"

&#x20; }

]

```



\### Ошибки



\- `401 Unauthorized` — пользователь не авторизован.



\---



\## 9.3. Отозвать заявку



```http

POST /api/applications/{applicationId}/withdraw

```



Позволяет кандидату отозвать свою заявку.



Отозвать можно только заявку, для которой это разрешено текущим состоянием.



\### Response — `200 OK`



```json

{

&#x20; "id": 101,

&#x20; "status": "WITHDRAWN"

}

```



\### Ошибки



\- `401 Unauthorized` — пользователь не авторизован;

\- `403 Forbidden` — заявка принадлежит другому пользователю;

\- `404 Not Found` — заявка не найдена;

\- `409 Conflict` — заявку нельзя отозвать в текущем состоянии.



\---



\## 9.4. Получить заявки проекта



```http

GET /api/projects/{projectId}/applications

```



Возвращает заявки на роли проекта.



Доступно владельцу проекта.



\### Response — `200 OK`



```json

\[

&#x20; {

&#x20;   "id": 101,

&#x20;   "status": "PENDING",

&#x20;   "role": {

&#x20;     "id": 15,

&#x20;     "name": "Backend Developer"

&#x20;   },

&#x20;   "candidate": {

&#x20;     "id": 12,

&#x20;     "displayName": "Alex"

&#x20;   },

&#x20;   "comment": "Хочу заниматься backend."

&#x20; }

]

```



\### Ошибки



\- `401 Unauthorized` — пользователь не авторизован;

\- `403 Forbidden` — пользователь не является владельцем проекта;

\- `404 Not Found` — проект не найден.



\---



\## 9.5. Принять заявку



```http

POST /api/applications/{applicationId}/accept

```



Принимает заявку кандидата.



Доступно владельцу проекта.



При успешном принятии:



1\. заявка получает состояние `ACCEPTED`;

2\. создаётся `Membership`;

3\. место в `capacity` считается занятым;

4\. другие `PENDING`-заявки этого пользователя на роли того же проекта закрываются.



Проверка `capacity` должна выполняться непосредственно при принятии заявки, чтобы конкурентные запросы не могли переполнить роль.



\### Response — `200 OK`



```json

{

&#x20; "applicationId": 101,

&#x20; "status": "ACCEPTED",

&#x20; "membershipId": 55

}

```



\### Ошибки



\- `401 Unauthorized` — пользователь не авторизован;

\- `403 Forbidden` — пользователь не является владельцем проекта;

\- `404 Not Found` — заявка не найдена;

\- `409 Conflict` — заявка уже обработана, роль заполнена или принятие невозможно в текущем состоянии проекта.



\---



\## 9.6. Отклонить заявку



```http

POST /api/applications/{applicationId}/reject

```



Отклоняет заявку кандидата.



Доступно владельцу проекта.



\### Response — `200 OK`



```json

{

&#x20; "applicationId": 101,

&#x20; "status": "REJECTED"

}

```



\### Ошибки



\- `401 Unauthorized` — пользователь не авторизован;

\- `403 Forbidden` — пользователь не является владельцем проекта;

\- `404 Not Found` — заявка не найдена;

\- `409 Conflict` — заявка уже обработана или не может быть отклонена.



\---



\# 10. Team



\## 10.1. Получить команду проекта



```http

GET /api/projects/{projectId}/team

```



Возвращает владельца и участников проекта.



\### Response — `200 OK`



```json

{

&#x20; "owner": {

&#x20;   "id": 7,

&#x20;   "displayName": "Evgen"

&#x20; },

&#x20; "members": \[

&#x20;   {

&#x20;     "userId": 12,

&#x20;     "displayName": "Alex",

&#x20;     "roleId": 15,

&#x20;     "roleName": "Backend Developer"

&#x20;   }

&#x20; ]

}

```



Владелец проекта хранится отдельно и не занимает место в `capacity` роли автоматически.



\### Ошибки



\- `404 Not Found` — проект не найден.



\---



\## 10.2. Покинуть команду



```http

POST /api/projects/{projectId}/team/leave

```



Текущий участник покидает команду проекта.



\### Response — `204 No Content`



\### Ошибки



\- `401 Unauthorized` — пользователь не авторизован;

\- `404 Not Found` — проект или membership не найден;

\- `409 Conflict` — действие невозможно в текущем состоянии.



\---



\## 10.3. Удалить участника из команды



```http

DELETE /api/projects/{projectId}/members/{userId}

```



Владелец удаляет участника из команды проекта.



\### Response — `204 No Content`



\### Ошибки



\- `401 Unauthorized` — пользователь не авторизован;

\- `403 Forbidden` — пользователь не является владельцем проекта;

\- `404 Not Found` — проект или участник не найден;

\- `409 Conflict` — действие невозможно в текущем состоянии.



\---



\# 11. Project Lifecycle



Жизненный цикл проекта v1:



```text

DRAFT → RECRUITING → IN\_PROGRESS → COMPLETED

&#x20;  \\          \\             \\

&#x20;   └──────────┴─────────────→ CANCELLED

```



Владелец управляет состоянием проекта.



\## 11.1. Открыть набор



```http

POST /api/projects/{projectId}/recruiting

```



Переводит проект из `DRAFT` в `RECRUITING`.



\### Response — `200 OK`



```json

{

&#x20; "id": 42,

&#x20; "state": "RECRUITING"

}

```



\---



\## 11.2. Начать проект



```http

POST /api/projects/{projectId}/start

```



Переводит проект в `IN\_PROGRESS`.



Владелец может начать проект до заполнения всех ролей.



При завершении набора оставшиеся `PENDING`-заявки закрываются.



\### Response — `200 OK`



```json

{

&#x20; "id": 42,

&#x20; "state": "IN\_PROGRESS"

}

```



\---



\## 11.3. Завершить проект



```http

POST /api/projects/{projectId}/complete

```



Переводит проект в `COMPLETED`.



\### Response — `200 OK`



```json

{

&#x20; "id": 42,

&#x20; "state": "COMPLETED"

}

```



\---



\## 11.4. Отменить проект



```http

POST /api/projects/{projectId}/cancel

```



Переводит проект в `CANCELLED`.



Активные `PENDING`-заявки закрываются.



\### Response — `200 OK`



```json

{

&#x20; "id": 42,

&#x20; "state": "CANCELLED"

}

```



\### Общие ошибки операций жизненного цикла



\- `401 Unauthorized` — пользователь не авторизован;

\- `403 Forbidden` — пользователь не является владельцем проекта;

\- `404 Not Found` — проект не найден;

\- `409 Conflict` — переход из текущего состояния проекта недопустим.



\---



\# 12. Основные состояния



\## Project



```text

DRAFT

RECRUITING

IN\_PROGRESS

COMPLETED

CANCELLED

```



\## Application



```text

PENDING

ACCEPTED

REJECTED

WITHDRAWN

CLOSED

```



\## Skill Level



```text

Beginner

Intermediate

Advanced

```



\---



\# 13. Ключевые бизнес-ограничения API v1



1\. `Application` и `Membership` являются разными сущностями.

2\. Подача заявки не занимает место в роли.

3\. Место в `capacity` занимает только принятый участник (`Membership`).

4\. При принятии заявки backend повторно проверяет доступность места.

5\. Один пользователь не может создать несколько заявок на одну и ту же роль.

6\. Пользователь может подаваться на разные роли одного проекта.

7\. После принятия пользователя на одну роль остальные его `PENDING`-заявки в этом проекте закрываются.

8\. В v1 повторная заявка на ту же роль после `REJECTED`, `WITHDRAWN` или `CLOSED` не создаётся.

9\. После появления заявок ключевые требования роли не должны изменяться.

10\. `capacity` роли нельзя уменьшить ниже количества уже принятых участников.

11\. Владелец проекта хранится отдельно и автоматически не занимает место в роли.

12\. Владелец может начать проект до заполнения всех ролей.

13\. При завершении набора оставшиеся `PENDING`-заявки закрываются.

14\. Matching является рекомендательным и объяснимым.

15\. В v1 matching не использует ML и не рассчитывает процент соответствия.

16\. Контакт между участниками после формирования команды осуществляется через указанные внешние контактные данные; встроенный чат не входит в v1.



\---



\# 14. Границы API Contracts v1



В текущую версию API Contracts не входят:



\- встроенный чат;

\- Telegram-автоматизация;

\- система рейтинга и репутации;

\- анализ токсичности и sentiment analysis;

\- ML-рекомендации;

\- сложный процентный matching;

\- автоматические skill tests;

\- внутренняя система задач и milestones;

\- расширенная система уведомлений.



Эти возможности могут быть добавлены в следующих версиях после стабилизации основного сценария TeamFinder.

