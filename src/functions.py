import json
from datetime import datetime
import os

current_path = os.path.dirname(os.path.realpath(__file__))

operations_file_path = os.path.join(current_path, '..', 'operations.json')


def read_file(file_path: str = operations_file_path) -> list:
    """
    Читает файл, возвращает данные
    :param file_path: путь к открываемому файлу
    :return: список словарей с данными
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data


def show_last_operations(data: list) -> str:
    """
    Показывает последние операции
    :param data: список словарей с данными
    :return: строка с результатами
    """
    last_operations = [op for op in data if op.get("state") == "EXECUTED"]
    recent_operations = sorted(last_operations, key=lambda op: op["date"], reverse=True)[:5]

    result = []
    for op in recent_operations:
        op_date = datetime.strptime(op['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')
        op_amount = op['operationAmount']['amount']
        op_currency = op['operationAmount']['currency']['name']
        op_description = op['description']
        op_from = mask_card(op.get('from'))
        op_to = mask_account(op['to'])

        result.append(f'{op_date} {op_description}\n{op_from} -> {op_to}\n{op_amount} {op_currency}\n')
    return "\n".join(result)


def mask_card(card_number: str) -> str:
    """
    Маскирует номер карты или счета откуда пришел перевод
    :param card_number: номер карты или счета
    :return: маскированный номер карты или счета
    """
    if card_number:
        card_name = ' '.join(card_number.split()[:-1])
        c_num = card_number.split()[-1]
        formatted_account = f"{c_num[:4]} {c_num[4:6]}{c_num[6:12].replace(c_num[6:12], '** ****')} {c_num[-4:]}"
        return f'{card_name} {formatted_account}'


def mask_account(account_number: str) -> str:
    """
    Маскирует номер карты или счета на который пришел перевод
    :param account_number: номер карты или счета
    :return: маскированный номер карты или счета
    """
    if account_number:
        acc_name = ' '.join(account_number.split()[:-1])
        a_num = account_number.split()[-1]
        return f'{acc_name} **{a_num[-4:]}'
