# TeamFinder — Use Case Diagram v1

- Версия: 1.1
- Владелец: Участник 3 (Business Analyst)
- Reviewer: Участник 2 (PM / System Analyst)
- Связанный документ: `use-cases.md`

Диаграмма отражает границу системы, акторов и сценарии UC-01 … UC-18. Telegram показан вторичным актором: через него приходят уведомления. Почта и push появятся в v1.0.

---

## 1. Диаграмма (Mermaid, рендерится в GitHub)

```mermaid
flowchart LR
    guest(["Гость"])
    user(["Пользователь"])
    owner(["Владелец проекта"])
    member(["Участник команды"])

    subgraph TF["Система TeamFinder"]
        UC01["UC-01 Регистрация"]
        UC02["UC-02 Вход в систему"]
        UC03["UC-03 Редактирование профиля"]
        UC04["UC-04 Создание проекта"]
        UC05["UC-05 Создание роли проекта"]
        UC06["UC-06 Просмотр каталога проектов"]
        UC07["UC-07 Просмотр соответствия роли"]
        UC08["UC-08 Подача заявки на роль"]
        UC09["UC-09 Отзыв заявки"]
        UC10["UC-10 Просмотр заявок на проект"]
        UC11["UC-11 Принятие заявки"]
        UC12["UC-12 Отклонение заявки"]
        UC13["UC-13 Выход из команды"]
        UC14["UC-14 Исключение участника"]
        UC15["UC-15 Перевод проекта в работу"]
        UC16["UC-16 Завершение или отмена проекта"]
        UC17["UC-17 Просмотр уведомлений"]
        UC18["UC-18 Подключение Telegram"]
    end

    tg(["Telegram"])

    guest --- UC01
    guest --- UC02

    user --- UC03
    user --- UC04
    user --- UC06
    user --- UC07
    user --- UC08
    user --- UC09

    owner --- UC05
    owner --- UC10
    owner --- UC11
    owner --- UC12
    owner --- UC14
    owner --- UC15
    owner --- UC16

    member --- UC13
    user --- UC17
    user --- UC18
    UC18 --- tg

    UC08 -.->|include| UC07
    UC11 -.->|include| UC10
    UC12 -.->|include| UC10
```

Наследование акторов: Владелец проекта и Участник команды являются частными случаями актора Пользователь, поэтому им доступны и сценарии UC-03, UC-06 … UC-09.

---

## 2. Та же диаграмма в нотации UML (PlantUML)

Используется для вставки в отчёт и для экспорта в изображение.

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle

actor "Гость" as Guest
actor "Пользователь" as User
actor "Владелец проекта" as Owner
actor "Участник команды" as Member

User <|-- Owner
User <|-- Member

rectangle "TeamFinder" {
  usecase "UC-01 Регистрация" as UC01
  usecase "UC-02 Вход в систему" as UC02
  usecase "UC-03 Редактирование профиля" as UC03
  usecase "UC-04 Создание проекта" as UC04
  usecase "UC-05 Создание роли проекта" as UC05
  usecase "UC-06 Просмотр каталога проектов" as UC06
  usecase "UC-07 Просмотр соответствия роли" as UC07
  usecase "UC-08 Подача заявки на роль" as UC08
  usecase "UC-09 Отзыв заявки" as UC09
  usecase "UC-10 Просмотр заявок на проект" as UC10
  usecase "UC-11 Принятие заявки" as UC11
  usecase "UC-12 Отклонение заявки" as UC12
  usecase "UC-13 Выход из команды" as UC13
  usecase "UC-14 Исключение участника" as UC14
  usecase "UC-15 Перевод проекта в работу" as UC15
  usecase "UC-16 Завершение или отмена проекта" as UC16
  usecase "UC-17 Просмотр уведомлений" as UC17
  usecase "UC-18 Подключение Telegram" as UC18
}

actor "Telegram" as Ext

Guest --> UC01
Guest --> UC02

User --> UC03
User --> UC04
User --> UC06
User --> UC07
User --> UC08
User --> UC09

Owner --> UC05
Owner --> UC10
Owner --> UC11
Owner --> UC12
Owner --> UC14
Owner --> UC15
Owner --> UC16

Member --> UC13
User --> UC17
User --> UC18
UC18 --> Ext

UC08 ..> UC07 : include
UC11 ..> UC10 : include
UC12 ..> UC10 : include
@enduml
```

---

## 3. Пояснения к связям

| Связь | Тип | Обоснование |
|---|---|---|
| UC-08 → UC-07 | include | Перед подачей заявки кандидату всегда показывается разбор соответствия роли |
| UC-11 → UC-10 | include | Принятие выполняется из карточки заявки, открытой в списке заявок проекта |
| UC-12 → UC-10 | include | Отклонение выполняется там же |
| UC-09 и UC-08 | нет связи | Отзыв — отдельный сценарий, который запускается позже и не встраивается в подачу заявки. То, что заявка должна быть подана и ждать решения, записано как предусловие UC-09. Поэтому `extend` тут не подходит |
