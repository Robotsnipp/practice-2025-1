import hashlib
import json
import random
import copy
import sys
from pprint import pprint


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.state = {}

    def hash_me(self, msg=""):
        """Хэширует данные с использованием SHA-256"""
        if not isinstance(msg, str):
            msg = json.dumps(msg, sort_keys=True)

        return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()

    def make_transaction(self, max_value=3):
        """Создает случайную транзакцию между Alice и Bob"""
        sign = int(random.getrandbits(1)) * 2 - 1  # Случайный знак: -1 или 1
        amount = random.randint(1, max_value)
        alice_pays = sign * amount
        bob_pays = -alice_pays
        return {"Alice": alice_pays, "Bob": bob_pays}

    def update_state(self, txn, state):
        """Обновляет состояние (балансы) на основе транзакции"""
        state = copy.deepcopy(state)
        for key in txn:
            if key in state:
                state[key] += txn[key]
            else:
                state[key] = txn[key]
        return state

    def is_valid_transaction(self, txn, state):
        """Проверяет, корректна ли транзакция"""
        if sum(txn.values()) != 0:
            return False  # Транзакция должна быть сбалансированной

        for key in txn:
            balance = state.get(key, 0)
            if balance + txn[key] < 0:
                return False  # Недостаточно средств
        return True

    def create_genesis_block(self):
        """Создает генезис-блок"""
        genesis_txns = [self.make_transaction() for _ in range(10)]
        genesis_contents = {
            "blockNumber": 0,
            "parentHash": None,
            "txnCount": len(genesis_txns),
            "txns": genesis_txns
        }
        genesis_hash = self.hash_me(genesis_contents)
        return {"hash": genesis_hash, "contents": genesis_contents}

    def add_block(self, txns):
        """Добавляет новый блок в цепочку"""
        parent_block = self.chain[-1]
        block_number = parent_block["contents"]["blockNumber"] + 1
        block_contents = {
            "blockNumber": block_number,
            "parentHash": parent_block["hash"],
            "txnCount": len(txns),
            "txns": []
        }

        # Проверяем и добавляем только валидные транзакции
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

    def check_block_hash(self, block):
        """Проверяет, совпадает ли хеш с содержимым блока"""
        expected_hash = self.hash_me(block["contents"])
        if block["hash"] != expected_hash:
            raise Exception(f"Неверный хеш в блоке {block['contents']['blockNumber']}")

    def check_block_validity(self, block, parent_block, state):
        """Проверяет корректность одного блока"""
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

    def check_chain_validity(self):
        """Проверяет целостность всей цепочки"""
        try:
            temp_state = {}
            # Проверяем генезис-блок
            for txn in self.chain[0]["contents"]["txns"]:
                temp_state = self.update_state(txn, temp_state)
            self.check_block_hash(self.chain[0])

            parent = self.chain[0]
            current_state = temp_state

            # Проверяем остальные блоки
            for block in self.chain[1:]:
                current_state = self.check_block_validity(block, parent, current_state)
                parent = block

            return current_state
        except Exception as e:
            print("Ошибка проверки цепочки:", e)
            return False

    def print_chain(self):
        """Выводит текущую цепочку блоков"""
        for i, block in enumerate(self.chain):
            print(f"\nБлок {i}")
            pprint(block)

    def get_current_state(self):
        """Возвращает текущее состояние системы (балансы)"""
        return self.state
