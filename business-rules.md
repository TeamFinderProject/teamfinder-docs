# Бизнес-правила MVP

Документ описывает основные ограничения текущего backend. Подробные поля и коды ошибок — в [контракте API](api-contracts-v1.md), пользовательские действия — в [Use Cases](use-cases.md). Это краткая сводка, а не новый набор идентификаторов RULE-*.

| Область | Правило | Реализация в backend |
|---|---|---|
| Заявка | Подаётся на конкретную ProjectRole. Повторная заявка того же пользователя на эту роль запрещена, включая завершённые заявки | Applications/ApplicationService.cs, Data/TeamFinderDbContext.cs |
| Подача | Владелец не подаётся в свой проект; нужны открытый набор, открытая роль и свободное место | Applications/ApplicationService.cs |
| Отзыв и решение | Отзыв доступен автору, принятие/отклонение — владельцу; обрабатывается только Pending | Applications/ApplicationService.cs |
| Capacity | Application не занимает место; учитываются Membership с EndedAt = null | Applications/ApplicationService.cs |
| Принятие | В транзакции проверяется capacity, создаётся Membership, закрываются другие Pending-заявки кандидата в этом проекте. При заполнении роли закрываются остальные Pending-заявки на роль | Applications/ApplicationService.cs |
| Конкурентность | Изменения одного проекта используют блокировку строки проекта в PostgreSQL | Common/ProjectLock.cs |
| Команда | Состав и внешний контакт доступны владельцу и действующим участникам; выход/исключение прекращает Membership и освобождает место | Teams/TeamService.cs |
| История участия | Текущая реализация запрещает повторное вступление после завершённого Membership в том же проекте | Applications/ApplicationService.cs |
| Завершение | В завершённом или отменённом проекте состав команды не меняется | Teams/TeamService.cs |
| Matching | Объяснение совпавших и отсутствующих навыков; решение о приёме остаётся владельцу | Projects/MatchingService.cs |

Исходники: [Applications](https://github.com/TeamFinderProject/teamfinder-backend/tree/develop/src/TeamFinder.Api/Applications), [Teams](https://github.com/TeamFinderProject/teamfinder-backend/tree/develop/src/TeamFinder.Api/Teams), [ProjectLock](https://github.com/TeamFinderProject/teamfinder-backend/blob/develop/src/TeamFinder.Api/Common/ProjectLock.cs).

Закрытие заявки сохраняет причину: принят на другую роль, роль заполнена, роль закрыта, набор завершён или проект отменён. Финальные статусы не переводятся обратно в Pending.
