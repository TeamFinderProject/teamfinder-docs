# Работа с Git и GitHub

- Владелец: Участник 1 (Team Lead / DevOps)
- Применяется к: `teamfinder-docs`, `teamfinder-backend`, `teamfinder-frontend`

## 1. Почему меняем процесс

На checkpoint 2 у нас висело несколько веток, которые так и не влили, а часть работы (например, `migration/teamfinder-schema-v2` в backend) вообще осталась мимо `main`. Ветки из worktree тоже лежали отдельно. Договорились так: всё вливаем в `develop` через PR, а в `main` попадает только то, что показываем на checkpoint.

## 2. Ветки

```mermaid
gitGraph
    commit id: "v0.1"
    branch develop
    checkout develop
    branch feature/backend-auth
    commit id: "auth: JWT + refresh"
    checkout develop
    merge feature/backend-auth
    branch feature/projects-with-roles
    commit id: "POST /projects с ролями"
    checkout develop
    merge feature/projects-with-roles
    checkout main
    merge develop tag: "v0.3"
```

| Ветка | Назначение | Кто пишет |
|---|---|---|
| `main` | Только версии, которые показываем на checkpoint. Защищена: прямой push запрещён | Только merge из `develop` |
| `develop` | Текущая интеграционная ветка. Всегда собирается и проходит тесты | Merge из feature-веток через PR |
| `feature/<коротко-о-задаче>` | Одна задача = одна ветка | Автор задачи |
| `fix/<коротко>` | Исправление ошибки | Автор |
| `docs/<коротко>` | Изменение документации | Автор |

Ветки, созданные через `git worktree`, проходят тот же процесс: PR в `develop`, review и merge. Worktree — дополнительная рабочая папка того же репозитория, обычно с отдельной веткой. Изменения в ней тоже нужно коммитить.

### Про слэш в названии ветки

Ветку `feature/backend-auth` git хранит как файл `refs/heads/feature/backend-auth`, то есть `feature` превращается в папку. Отсюда две вещи:

- нельзя одновременно иметь ветку `feature` и ветки `feature/...`: git, а при push и GitHub, откажет с ошибкой `cannot lock ref`. Поэтому ветку с именем просто `feature`, `fix` или `docs` не создаём;
- слэш группирует ветки: GitHub показывает их по префиксу, а правило защиты можно повесить сразу на маску вроде `feature/*`.

Имена пишем так: `тип/коротко-о-задаче`, маленькими латинскими буквами через дефис, например `feature/projects-with-roles`, `fix/withdraw-status`, `docs/api-contracts`.

## 3. Процесс

```text
Issue → Assignee → ветка от develop → коммиты → PR в develop → review → CI зелёный → merge → удалить ветку
```

1. Задача создаётся в GitHub Project как Issue, назначается исполнитель.
2. Ветка создаётся от `develop`: `git switch develop && git pull && git switch -c feature/backend-auth`.
3. Коммиты по смыслу, сообщения в виде `тип: что сделано` (`feat`, `fix`, `docs`, `test`, `refactor`, `ci`).
4. PR в `develop`, в описании — `Closes #<номер issue>` и как проверить.
5. Review делает другой участник. Автор должен уметь объяснить каждое изменение.
6. После merge ветка удаляется (кнопка «Delete branch» в PR).
7. Перед checkpoint: PR `develop → main` и тег версии: `v0.3` для checkpoint 3 (MVP), `v1.0` для защиты.

## 4. Проверка веток перед checkpoint 3

Выполняет Участник 1. Перед изменениями обновить сведения о ветках:

```bash
git fetch origin --prune
git branch -r
git branch -r --merged origin/develop
```

- Если `develop` уже существует, повторно создавать её не нужно. Новые задачи начинаются от актуальной `develop`.
- Ветки со слитыми PR можно удалить после проверки целевой ветки.
- Невлитую ветку нельзя удалять только потому, что подготовлены новые файлы. Сначала сравнить изменения, договориться с автором и проверить, что нужная работа сохранена.
- Общую `feature/checkpoint-3-backend` сохраняем до добавления частей обоих участников, проверок и merge общего PR. Каждый участник делает собственные коммиты.
- Документация и frontend DevOps идут отдельными PR. Слияние этих PR не означает завершения общей backend-задачи или экранов frontend.

### Настройки GitHub (Settings → Branches)

- Default branch: `develop`.
- Branch protection для `main` и `develop`: Require a pull request before merging, Require approvals: 1, Require status checks to pass: в backend проверка `build-test`, во frontend `build` (они появятся в списке после первого запуска CI).
- Settings → General → Automatically delete head branches: ветка удаляется сама после merge.
- Вкладка Actions: проверить, что GitHub Actions включены, иначе CI не запустится.
