import unittest
from unittest.mock import patch
from datetime import date, timedelta

import numpy as np
from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt

from converter import CurrencyConverter
from urllib import request


class CurrencyConverterTests(unittest.TestCase):

    def setUp(self):
        self.converter = CurrencyConverter()

    def test_get_dates(self):  # получение списка дат
        expected_dates = []
        first_day = date.today() - timedelta(days=15)
        for j in range(15):
            expected_dates.append(first_day)
            first_day += timedelta(days=1)

        result = self.converter.get_dates()

        self.assertEqual(result, expected_dates)

    def test_get_next_three(self):  # предсказание 3-х следующих значений
        values = [1, 2, 3, 4, 5]
        expected_next_values = [6, 7, 8]

        next_values = self.converter.get_next_three(values)

        self.assertTrue(np.array_equal(next_values, expected_next_values))

    def test_create_tab2(self):
        self.converter.create_tab2()
        self.assertEqual(len(self.converter.tab_control.tabs()), 3)

        expected_values = tuple(self.converter.name_list[1:])
        self.assertEqual(self.converter.combobox3["values"], expected_values)

        self.assertEqual(self.converter.combobox3.current(), 0)

        expected_period_values = tuple([(date.today() - relativedelta(months=0)).strftime("%B %Y")])
        self.assertEqual(self.converter.period_combobox2["values"], expected_period_values)

        self.assertEqual(self.converter.period_combobox2.current(), 0)
        self.assertIsInstance(self.converter.fig, plt.Figure)

    def test_create_tab1(self):
        self.assertEqual(len(self.converter.tab_control.tabs()), 2)
        self.assertEqual(self.converter.combobox1.get(), self.converter.name_list[0])
        self.assertEqual(self.converter.combobox2.get(), self.converter.name_list[11])
        self.assertEqual(self.converter.entry1.get(), "")

        self.assertIsNotNone(self.converter.conv_button)
        self.assertEqual(self.converter.conv_button["text"], "Конвертировать")

        self.assertIsNotNone(self.converter.label1)


if __name__ == '__main__':
    unittest.main()
