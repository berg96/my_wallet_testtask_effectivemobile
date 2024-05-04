import datetime
import os
from typing import Optional


class Record:
    """Финансовая запись с датой, категорией, суммой и описанием"""
    def __init__(
            self, date: str, category: str, amount: int, description: str
    ):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description


class FinanceManager:
    """Финансовый менеджер с основными функциями приложения"""
    def __init__(self):
        self.records: list[Record] = []

    def add_record(self, record: Record) -> None:
        """Добавляет запись в список всех записей"""
        self.records.append(record)

    def edit_record(self, index: int, record: Record) -> None:
        """Изменяет запись по индексу в списке записей"""
        self.records[index] = record

    def get_balance(self) -> tuple[int, int, int]:
        """Вывод баланса.
        Отдаёт кортеж с суммой доходов, суммой расходов и балансом"""
        total_income: int = sum(
            record.amount for record in self.records
            if record.category == 'Доход'
        )
        total_expense: int = sum(
            record.amount for record in self.records
            if record.category == 'Расход'
        )
        total_balance: int = total_income - total_expense
        return total_income, total_expense, total_balance

    def search_records(
            self, date: Optional[str] = '', category: Optional[str] = '',
            amount: Optional[str] = ''
    ) -> Optional[list[Record]]:
        """Поиск записей по дате, категории и сумме (опционально)"""
        result: list[Record] = []
        for record in self.records:
            if (
                (record.date == date or date == '')
                and (record.category == category or category == '')
                and (str(record.amount) == amount or amount == '')
            ):
                result.append(record)
        return result


class FileHandler:
    """Класс, работающий с файлом на чтение,
    перезапись, добавление и изменение"""
    def __init__(self, filename: str):
        self.filename = filename

    def save(self, records: list[Record]) -> None:
        """Перезапись файла всех данных"""
        with open(self.filename, 'w', encoding='utf-8') as file:
            data: str = '\n'.join(
                [
                    '\n'.join((
                        f'Дата: {record.date}',
                        f'Категория: {record.category}',
                        f'Сумма: {record.amount}',
                        f'Описание: {record.description}',
                        ''
                    )) for record in records
                ]
            )
            file.write(data)

    def load(self) -> Optional[list[str]]:
        """Чтение данных из файла"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                data: list[str] = file.readlines()
            return data

    def add(self, record: Record) -> None:
        """Добавление записи в конец файла"""
        with open(self.filename, 'a', encoding='utf-8') as file:
            data: str = '\n'.join(
                (
                    '',
                    f'Дата: {record.date}',
                    f'Категория: {record.category}',
                    f'Сумма: {record.amount}',
                    f'Описание: {record.description}',
                    ''
                )
            )
            file.write(data)

    def edit(self, index: int, record: Record) -> None:
        """Изменение файла по индексу записи"""
        with open(self.filename, 'r', encoding='utf-8') as file:
            lines: list[str] = file.readlines()
        with open(self.filename, 'w', encoding='utf-8') as file:
            interval: list[int] = list(range(index * 5, index * 5 + 5))
            num: int = 0
            while num < len(lines):
                if num in interval:
                    file.write('\n'.join(
                        (
                            f'Дата: {record.date}',
                            f'Категория: {record.category}',
                            f'Сумма: {record.amount}',
                            f'Описание: {record.description}',
                            '', ''
                        )
                    ))
                    num += 5
                else:
                    file.write(lines[num])
                    num += 1


class ConsoleUI:
    """Консольный пользовательский интерфейс"""
    def __init__(
            self, finance_manager: FinanceManager, file_handler: FileHandler
    ):
        self.finance_manager = finance_manager
        self.file_handler = file_handler

    @staticmethod
    def clear_screen() -> None:
        """Очистка консоли"""
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def show_menu() -> None:
        """Вывод в консоль меню приложения"""
        print('--- Учет личных доходов и расходов ---')
        print('1. Вывести баланс')
        print('2. Добавить запись')
        print('3. Редактировать запись')
        print('4. Поиск по записям')
        print('5. Выход')

    def load_data(self) -> None:
        """Загрузка данных из файла в Финансовый менеджер"""
        data: Optional[list[str]] = self.file_handler.load()
        if data:
            for row in data:
                if 'Дата: ' in row:
                    date = row.split('Дата: ')[1].strip()
                elif 'Категория: ' in row:
                    category = row.split('Категория: ')[1].strip()
                elif 'Сумма: ' in row:
                    amount = int(row.split('Сумма: ')[1].strip())
                elif 'Описание: ' in row:
                    description = row.split('Описание: ')[1].strip()
                else:
                    self.finance_manager.add_record(
                        Record(date, category, amount, description)
                    )
            self.finance_manager.add_record(
                Record(date, category, amount, description)
            )

    def handle_input(self) -> None:
        """Принимает и обрабатывает ввод пользователя"""
        choice: str = input('> ')
        if choice == '1':
            self.clear_screen()
            (
                total_income, total_expense, total_balance
            ) = self.finance_manager.get_balance()
            print(f'Доходы: {total_income}')
            print(f'Расходы: {total_expense}')
            print(f'Баланс: {total_balance}')
            input('Нажмите Enter для выхода в меню...')
        elif choice == '2':
            self.clear_screen()
            try:
                date: str = datetime.date.fromisoformat(
                    input('Дата (ГГГГ-ММ-ДД): ')
                ).isoformat()
                category: str = input(
                    'Категория (Доход/Расход): '
                ).capitalize()
                if category not in ['Доход', 'Расход']:
                    raise ValueError('Категория должна быть Доход или Расход.')
                amount: int = int(input('Сумма: '))
                if amount <= 0:
                    raise ValueError('Сумма должна быть положительной.')
                description: str = input('Описание: ')
                record: Record = Record(date, category, amount, description)
                self.finance_manager.add_record(record)
                self.file_handler.add(record)
                print('Запись добавлена.')
            except Exception as error:
                print(error)
            finally:
                input('Нажмите Enter для выхода в меню...')
        elif choice == '3':
            self.clear_screen()
            try:
                index: int = int(input('Индекс записи для редактирования: '))
                if index < 0 or index >= len(self.finance_manager.records):
                    raise ValueError('Такой записи не существует.')
                date: str = datetime.date.fromisoformat(
                    input('Дата (ГГГГ-ММ-ДД): ')
                ).isoformat()
                category: str = input(
                    'Категория (Доход/Расход): '
                ).capitalize()
                if category not in ['Доход', 'Расход']:
                    raise ValueError('Категория должна быть Доход или Расход.')
                amount: int = int(input('Сумма: '))
                if amount <= 0:
                    raise ValueError('Сумма должна быть положительной.')
                description: str = input('Описание: ')
                new_record: Record = Record(
                    date, category, amount, description
                )
                self.finance_manager.edit_record(index, new_record)
                self.file_handler.edit(index, new_record)
                print('Запись изменена.')
            except Exception as error:
                print(error)
            finally:
                input('Нажмите Enter для выхода в меню...')
        elif choice == '4':
            self.clear_screen()
            date: str = input('Дата (необязательно): ')
            category: str = input('Категория (необязательно): ').capitalize()
            amount: str = input('Сумма (необязательно): ')
            result: Optional[
                list[Record]
            ] = self.finance_manager.search_records(date, category, amount)
            print('Результаты поиска:')
            if result:
                for record in result:
                    print(f'Дата: {record.date}')
                    print(f'Категория: {record.category}')
                    print(f'Сумма: {record.amount}')
                    print(f'Описание: {record.description}')
                    print()
            else:
                print('Ничего не найдено.')
            input('Нажмите Enter для выхода в меню...')
        elif choice == '5':
            self.file_handler.save(self.finance_manager.records)
            exit()


def my_wallet() -> None:
    """Создает экземпляры классов FileHandler, FinanceManager и ConsoleUI,
    загружает данные, отображает меню и обрабатывает ввод пользователя"""
    file_handler: FileHandler = FileHandler('data.txt')
    finance_manager: FinanceManager = FinanceManager()
    ui: ConsoleUI = ConsoleUI(finance_manager, file_handler)
    ui.load_data()
    while True:
        ui.clear_screen()
        ui.show_menu()
        ui.handle_input()


if __name__ == '__main__':
    my_wallet()
