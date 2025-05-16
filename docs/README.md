# 📄 Документация к проекту: Блокчейн на Python  

## 📘 Общее описание  
Данный документ содержит подробное описание реализации простого блокчейна, разработанного на языке Python. Цель проекта — создать минимальную функциональную модель блокчейна, способную:
- Генерировать случайные транзакции между участниками
- Создавать и добавлять новые блоки в цепочку
- Проверять целостность всей цепочки
- Поддерживать текущее состояние системы (балансы участников)

Проект позволяет понять базовые принципы работы технологии блокчейн и изучить ключевые аспекты её реализации.

---

## 🔧 Технические требования

### Стек технологий:
| Компонент | Описание |
|----------|----------|
| Язык программирования | Python 3.x |
| Основные модули | `hashlib`, `json`, `random`, `copy` |
| Дополнительные модули | `pprint` |

### Функциональные возможности:
- Хэширование блоков с использованием SHA-256
- Генерация случайных транзакций
- Проверка корректности транзакций (баланс, сумма)
- Поддержка состояния системы (балансы пользователей)
- Проверка целостности цепочки блоков
- Возможность вывода информации о цепочке

---

## 🛠 Архитектура блокчейна

Блокчейн реализован как класс `Blockchain`, который управляет:
- Цепочкой блоков (`chain`)
- Текущим состоянием системы (`state`)
- Методами для создания транзакций, проверки данных и добавления блоков

Основные компоненты:
1. **Хэширование** — вычисление хеша блока с помощью SHA-256.
2. **Транзакции** — генерация случайных переводов между участниками.
3. **Состояние** — отслеживание балансов пользователей.
4. **Проверка** — валидация транзакций и целостности цепочки.

---

## 📂 Структура проекта

```
blockchain/
│
└── blockchain.py         # Основной файл с реализацией блокчейна
```

---

## 🧩 Реализация функционала

### 1. Инициализация блокчейна

```python
def __init__(self):
    self.chain = [self.create_genesis_block()]
    self.state = {}
```

- При создании экземпляра класса автоматически создаётся генезис-блок
- Инициализируется пустое состояние системы (`state`)

---

### 2. Хэширование данных

```python
def hash_me(self, msg=""):
    if not isinstance(msg, str):
        msg = json.dumps(msg, sort_keys=True)
    return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()
```

- Все данные преобразуются в строку формата JSON
- Вычисляется хеш с использованием алгоритма SHA-256
- Возвращает шестнадцатеричное представление хеша

---

### 3. Генерация случайной транзакции

```python
def make_transaction(self, max_value=3):
    sign = int(random.getrandbits(1)) * 2 - 1
    amount = random.randint(1, max_value)
    alice_pays = sign * amount
    bob_pays = -alice_pays
    return {"Alice": alice_pays, "Bob": bob_pays}
```

- Генерируется случайная сумма перевода от Alice к Bob или обратно
- Сумма находится в диапазоне от 1 до `max_value`
- Возвращается словарь с изменениями балансов

---

### 4. Обновление состояния системы

```python
def update_state(self, txn, state):
    state = copy.deepcopy(state)
    for key in txn:
        if key in state:
            state[key] += txn[key]
        else:
            state[key] = txn[key]
    return state
```

- Копируется текущее состояние, чтобы не изменять оригинал
- Обновляются балансы участников согласно транзакции

---

### 5. Проверка корректности транзакции

```python
def is_valid_transaction(self, txn, state):
    if sum(txn.values()) != 0:
        return False
    for key in txn:
        balance = state.get(key, 0)
        if balance + txn[key] < 0:
            return False
    return True
```

- Проверяется, что сумма всех изменений равна нулю (перевод от одного к другому)
- Проверяется наличие достаточного количества средств у отправителя

---

### 6. Создание генезис-блока

```python
def create_genesis_block(self):
    genesis_txns = [self.make_transaction() for _ in range(10)]
    genesis_contents = {
        "blockNumber": 0,
        "parentHash": None,
        "txnCount": len(genesis_txns),
        "txns": genesis_txns
    }
    genesis_hash = self.hash_me(genesis_contents)
    return {"hash": genesis_hash, "contents": genesis_contents}
```

- Генерируется 10 случайных транзакций
- Устанавливается начальный номер блока (0)
- Родительский хеш отсутствует (None)
- Вычисляется хеш содержимого блока

---

### 7. Добавление нового блока

```python
def add_block(self, txns):
    parent_block = self.chain[-1]
    block_number = parent_block["contents"]["blockNumber"] + 1
    block_contents = {
        "blockNumber": block_number,
        "parentHash": parent_block["hash"],
        "txnCount": len(txns),
        "txns": []
    }

    valid_txns = []
    temp_state = copy.deepcopy(self.state)
    for txn in txns:
        if self.is_valid_transaction(txn, temp_state):
            valid_txns.append(txn)
            temp_state = self.update_state(txn, temp_state)

    block_contents["txns"] = valid_txns
    block_contents["txnCount"] = len(valid_txns)
    block_hash = self.hash_me(block_contents)
    new_block = {"hash": block_hash, "contents": block_contents}
    self.chain.append(new_block)
    self.state = temp_state
```

- Номер блока увеличивается на 1 относительно последнего в цепочке
- Запоминается хеш предыдущего блока
- Проверяются и фильтруются только корректные транзакции
- Добавляется новый блок в цепочку и обновляется состояние системы

---

### 8. Проверка хеша блока

```python
def check_block_hash(self, block):
    expected_hash = self.hash_me(block["contents"])
    if block["hash"] != expected_hash:
        raise Exception(f"Неверный хеш в блоке {block['contents']['blockNumber']}")
```

- Пересчитывается хеш содержимого блока
- Сравнивается с сохранённым значением
- Если значения не совпадают — выбрасывается исключение

---

### 9. Проверка корректности одного блока

```python
def check_block_validity(self, block, parent_block, state):
    block_num = block["contents"]["blockNumber"]
    parent_num = parent_block["contents"]["blockNumber"]

    if block_num != parent_num + 1:
        raise Exception(f"Некорректный номер блока: {block_num}")

    if block["contents"]["parentHash"] != parent_block["hash"]:
        raise Exception(f"Некорректный родительский хеш в блоке {block_num}")

    self.check_block_hash(block)

    temp_state = copy.deepcopy(state)
    for txn in block["contents"]["txns"]:
        if not self.is_valid_transaction(txn, temp_state):
            raise Exception(f"Некорректная транзакция в блоке {block_num}: {txn}")
        temp_state = self.update_state(txn, temp_state)

    return temp_state
```

- Проверяется корректность номера блока
- Проверяется соответствие родительского хеша
- Проверяется целостность хеша блока
- Проверяются все транзакции внутри блока

---

### 10. Проверка всей цепочки

```python
def check_chain_validity(self):
    try:
        temp_state = {}
        for txn in self.chain[0]["contents"]["txns"]:
            temp_state = self.update_state(txn, temp_state)
        self.check_block_hash(self.chain[0])

        parent = self.chain[0]
        current_state = temp_state

        for block in self.chain[1:]:
            current_state = self.check_block_validity(block, parent, current_state)
            parent = block

        return current_state
    except Exception as e:
        print("Ошибка проверки цепочки:", e)
        return False
```

- Проверяется генезис-блок
- Последовательно проверяются все остальные блоки
- В случае ошибки — возвращается `False` и выводится сообщение

---

### 11. Вывод цепочки

```python
def print_chain(self):
    for i, block in enumerate(self.chain):
        print(f"\nБлок {i}")
        pprint(block)
```

- Выводит информацию обо всех блоках в удобочитаемом виде

---

### 12. Получение текущего состояния

```python
def get_current_state(self):
    return self.state
```

- Возвращает текущие балансы участников

---

## 🧪 Тестирование

### Пример использования:

```python
bc = Blockchain()

# Добавляем несколько блоков
for _ in range(3):
    txns = [bc.make_transaction() for _ in range(5)]
    bc.add_block(txns)

# Выводим цепочку
bc.print_chain()

# Проверяем целостность
if bc.check_chain_validity():
    print("Цепочка корректна")
else:
    print("Цепочка повреждена")

# Выводим текущее состояние
print("Текущее состояние:")
pprint(bc.get_current_state())
```

### Вывод:

```
Блок 0
{'contents': {'blockNumber': 0,
              'parentHash': None,
              'txnCount': 10,
              'txns': [{'Alice': -3, 'Bob': 3},
                       {'Alice': -2, 'Bob': 2},
                       {'Alice': -2, 'Bob': 2},
                       {'Alice': -2, 'Bob': 2},
                       {'Alice': 3, 'Bob': -3},
                       {'Alice': 2, 'Bob': -2},
                       {'Alice': -1, 'Bob': 1},
                       {'Alice': -2, 'Bob': 2},
                       {'Alice': -2, 'Bob': 2},
                       {'Alice': -2, 'Bob': 2}]},
 'hash': '8e17ac0f66e0d4abd264c9441ed13213b3be80fd34a3540ee0d40f15f9a95d87'}

Блок 1
{'contents': {'blockNumber': 1,
              'parentHash': '8e17ac0f66e0d4abd264c9441ed13213b3be80fd34a3540ee0d40f15f9a95d87',
              'txnCount': 0,
              'txns': []},
 'hash': '20c17cad4f3195b55aebf2a4cbdfe022a95fae1565942ff0ac4eacaedc50c75d'}

Блок 2
{'contents': {'blockNumber': 2,
              'parentHash': '20c17cad4f3195b55aebf2a4cbdfe022a95fae1565942ff0ac4eacaedc50c75d',
              'txnCount': 0,
              'txns': []},
 'hash': 'ba4e9b6913ce92a87768bae715118f49e0f4b5aa4603b732b3cf81e57934dec4'}

Блок 3
{'contents': {'blockNumber': 3,
              'parentHash': 'ba4e9b6913ce92a87768bae715118f49e0f4b5aa4603b732b3cf81e57934dec4',
              'txnCount': 0,
              'txns': []},
 'hash': 'c7ce52944e39d826c2a38dccc78f116d00bd516f0be582b2d5c75849c310f120'}
Цепочка корректна
Текущее состояние:
{}
```
---

## ✅ Преимущества решения

- Минимальная, но рабочая реализация блокчейна
- Полностью самодостаточная логика
- Четкая структура кода
- Простота расширения
- Отлично подходит для образовательных целей

---

## 🚀 Возможности для улучшения

- Добавление новых участников
- Поддержка подписей транзакций
- Хранение цепочки в файле
- Визуализация цепочки
- Поддержка майнинга и Proof-of-Work
- Распределённая сеть узлов

---

## 📌 Заключение

В результате выполнения проекта был успешно создан простой блокчейн на Python. Он умеет генерировать транзакции, добавлять блоки, проверять их целостность и отслеживать состояние системы.  

Этот проект может служить отличной основой для дальнейшего изучения технологии блокчейн и создания более сложных систем.
