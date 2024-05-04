import unittest

from main import FinanceManager, Record


class TestFinanceManager(unittest.TestCase):
    def setUp(self):
        self.finance_manager = FinanceManager()
        record_income = Record('2024-04-10', 'Доход', 50000, 'Зарплата')
        record_expense = Record('2024-04-10', 'Расход', 15000, 'Аренда')
        self.finance_manager.add_record(record_income)
        self.finance_manager.add_record(record_expense)

    def test_balance(self):
        self.assertEqual(self.finance_manager.get_balance()[0], 50000)
        self.assertEqual(self.finance_manager.get_balance()[1], 15000)
        self.assertEqual(self.finance_manager.get_balance()[2], 35000)

    def test_add_record(self):
        new_record = Record('2024-04-25', 'Доход', 30000, 'Аванс')
        self.finance_manager.add_record(new_record)
        self.assertEqual(self.finance_manager.get_balance()[0], 80000)

    def test_edit_record(self):
        new_record = Record('2024-04-10', 'Доход', 80000, 'Зарплата')
        self.finance_manager.edit_record(0, new_record)
        self.assertEqual(self.finance_manager.get_balance()[0], 80000)

    def test_search_records(self):
        records = self.finance_manager.search_records(category='Доход')
        print(self.finance_manager.records[0].category)
        self.assertEqual(len(records), 1)
        records = self.finance_manager.search_records(date='2024-04-10')
        self.assertEqual(len(records), 2)
        records = self.finance_manager.search_records(amount='150000')
        self.assertEqual(len(records), 0)


if __name__ == 'main':
    unittest.main()
