import datetime
from sklearn.linear_model import LinearRegression
from tkinter import *
from tkinter.ttk import Notebook, Frame, Combobox
from tkinter import messagebox as me
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
import urllib.request
import xml.dom.minidom
import locale
import matplotlib.pyplot as plt
import matplotlib

locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')


class CurrencyConverter:
    def __init__(self):
        self.value_list = [1]  # словарь, который хранит значения валют на сегодняшний день
        self.name_list = ["Российский рубль"]  # список с названиями валют
        self.fetch_today_values()
        self.create_window()
        self.start()

    def start(self):
        self.window.mainloop()

    def fetch_today_values(self):
        today_response = urllib.request.urlopen(
            "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + date.today().strftime("%d/%m/%Y"))
        dom = xml.dom.minidom.parse(today_response)
        dom.normalize()
        nodeArray = dom.getElementsByTagName("Valute")
        for node in nodeArray:
            val_nominal = 1
            childList = node.childNodes
            for child in childList:
                if child.nodeName == "Name":
                    self.name_list.append(child.childNodes[0].nodeValue)
                if child.nodeName == "Nominal":
                    val_nominal = float(child.childNodes[0].nodeValue)
                if child.nodeName == "Value":
                    self.value_list.append(float(child.childNodes[0].nodeValue.replace(',', '.')) / val_nominal)

        self.dict_valute = dict(
            zip(self.name_list, self.value_list))  # словарь - название валюты : значение валюты на сегодняшний день
        return

    def create_tab1(self):

        self.tab1 = Frame(self.window)  # первая вкладка
        self.tab_control.add(self.tab1, text="Калькулятор валют")

        self.combobox1 = Combobox(self.tab1, state="readonly")  # Первый комбобокс для выбора валюты
        self.combobox1["values"] = self.name_list
        self.combobox1.current(0)
        self.combobox1.grid(column=1, row=1, padx=20, pady=15)

        self.combobox2 = Combobox(self.tab1, state="readonly")  # Второй комбобокс для выбора валюты
        self.combobox2["values"] = self.name_list
        self.combobox2.current(11)
        self.combobox2.grid(column=1, row=2, pady=5)

        self.entry1 = Entry(self.tab1, text="")  # Поле для ввода значения
        self.entry1.grid(column=2, row=1, padx=20)

        self.conv_button = Button(self.tab1, text="Конвертировать",
                                  command=self.conv_button_click)  # кнопка КОНВЕРТИРОВАТЬ
        self.conv_button.grid(column=3, row=1, padx=20)

        self.label1 = Label(self.tab1)  # конвертированная валюта
        self.label1.grid(column=2, row=2)

    def create_tab2(self):
        self.tab2 = Frame(self.window)  # вторая вкладка
        self.tab_control.add(self.tab2, text="Динамика курса")

        # надписи во второй вкладке
        label_val = Label(self.tab2, text="Валюта")
        label_val.grid(column=1, row=1)
        label_choice_per = Label(self.tab2, text="Выбор периода")
        label_choice_per.grid(column=3, row=1)

        self.combobox3 = Combobox(self.tab2,
                                  state="readonly")  # комбобокс с выбором валюты для графика (вторая вкладка)

        self.combobox3["values"] = self.name_list[1:]
        self.combobox3.current(0)
        self.combobox3.grid(column=1, row=2, pady=5, padx=20)
        # Выбор периода
        self.var_period = IntVar()
        self.var_period.set(0)

        # Создаем списки с периодами для комбобоксов
        list2 = []
        list2.append((date.today() - relativedelta(months=0)).strftime("%B %Y"))

        self.period_combobox2 = Combobox(self.tab2, state="readonly", value=list2)
        self.period_combobox2.current(0)
        self.period_combobox2.grid_forget()
        self.period_combobox2.grid(column=3, row=2)

        # кнопка построить график
        self.graph_button = Button(self.tab2, text="Построить график", command=self.graph_button_click)
        self.graph_button.grid(row=3, column=1, padx=50)
        # график
        matplotlib.use("TkAgg")
        self.fig = plt.figure(figsize=(13, 6))

    def create_window(self):
        self.window = Tk()
        self.window.title("Конвертер валют")  # Название окна
        self.window.geometry("520x180")
        self.tab_control = Notebook(self.window)
        self.tab_control.pack(expand=True, fill=BOTH)
        self.create_tab1()
        self.create_tab2()

    def conv_button_click(self):  # (кнопка КОНВЕРТИРОВАТЬ)
        try:
            answ = float(self.entry1.get().replace(',', '.')) * self.dict_valute[self.combobox1.get()] / \
                   self.dict_valute[self.combobox2.get()]
            self.label1.config(text=str(answ))
        except ValueError:
            me.showerror("Ошибка", "Ошибка ввода")

    def get_dates(self):
        dates = []
        first_day = date.today() - timedelta(days=15)
        for j in range(15):
            dates.append(first_day)
            first_day += timedelta(days=1)
        return dates

    def get_next_three(self, values):
        # Создание массива признаков X и массива целевых значений y
        X = [[i] for i in range(len(values))]
        y = values

        # Создание и обучение модели линейной регрессии
        model = LinearRegression()
        model.fit(X, y)

        # Прогнозирование следующих трех значений
        next_values = model.predict([[len(values)], [len(values) + 1], [len(values) + 2]])
        return next_values

    def graph_button_click(self):  # построить график
        currency = self.combobox3.get()
        list_days, list_values = [], []  # список со значениями дней, валют
        self.window.geometry("1550x830")
        number = self.name_list.index(currency) - 1
        dates = self.get_dates()
        list_days = []
        for d in dates:
            list_days.append(d.strftime("%d/%m"))
            date_response = urllib.request.urlopen(
                "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + d.strftime("%d/%m/%Y"))
            dom = xml.dom.minidom.parse(date_response)
            nodeValueArray = dom.getElementsByTagName("Value")
            nodeNominalArray = dom.getElementsByTagName("Nominal")
            list_values.append(float((nodeValueArray[number].firstChild.nodeValue).replace(',', '.')) / float(
                nodeNominalArray[number].firstChild.nodeValue))

        next_values = self.get_next_three(list_values)
        for i in range(3):
            dates.append(dates[-1] + timedelta(days=1))
            list_days.append(dates[-1].strftime("%d/%m"))
            list_values.append(next_values[i])

        canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.fig, master=self.tab2)
        gr_widget = canvas.get_tk_widget()
        self.fig.clear()
        plt.plot(list_days, list_values, "black")
        plt.grid()
        gr_widget.grid(column=10, row=6, padx=10, pady=45)


c = CurrencyConverter()
