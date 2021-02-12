import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        return sum(r.amount for r in self.records if r.date == dt.date.today())

    def get_week_stats(self):
        week_ago = dt.date.today() - dt.timedelta(days=7)
        gen = [r.amount for r in self.records
               if week_ago < r.date <= dt.date.today()]
        return sum(gen)

    def get_balance_for_today(self):
        return self.limit - self.get_today_stats()


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()

    def __str__(self):
        return self.comment


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        balance = self.get_balance_for_today()
        if balance > 0:
            return ('Сегодня можно съесть что-нибудь ещё,'
                    f' но с общей калорийностью не более {balance} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 74.30
    EURO_RATE = 89.57

    def get_today_cash_remained(self, currency):
        balance = self.get_balance_for_today()
        if balance == 0:
            return 'Денег нет, держись'
        value, ending = self.convert_currency(balance, currency)
        if balance > 0:
            return f'На сегодня осталось {value:.2f} {ending}'
        value = -value
        return f'Денег нет, держись: твой долг - {value:.2f} {ending}'

    def convert_currency(self, rub_value, currency):
        if currency == 'usd':
            result = rub_value / self.USD_RATE, 'USD'
        elif currency == 'eur':
            result = rub_value / self.EURO_RATE, 'Euro'
        else:
            result = rub_value, 'руб'
        return result
