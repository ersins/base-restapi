import datetime

from rest_framework import response, status
from rest_framework.views import APIView

from expenses.models import Expense
from income.models import Income


class ExpenseSummaryStats(APIView):
    def get_category(self, expense):
        return expense.category

    def get_amount_for_category(self, expense_list, category):
        expenses = expense_list.filter(category=category)
        amount = 0
        for expense in expenses:
            amount += expense.amount
        return {'amount': str(amount)}

    def get(self, request):
        todays_date = datetime.date.today()
        a_year_ago = todays_date - datetime.timedelta(days=30 * 12)
        expenses = Expense.objects.filter(owner=request.user, date__gte=a_year_ago, date__lte=todays_date)

        final_data = {}
        categories = list(set(map(self.get_category, expenses)))

        for expense in expenses:
            for category in categories:
                final_data[category] = self.get_amount_for_category(expenses, category)

        return response.Response({'category_data': final_data}, status=status.HTTP_200_OK)

class IncomeSummaryStats(APIView):
    def get_source(self, income):
        return income.source

    def get_amount_for_category(self, income_list, source):
        incomes = income_list.filter(source=source)
        amount = 0
        for income in incomes:
            amount += income.amount
        return {'amount': str(amount)}

    def get(self, request):
        todays_date = datetime.date.today()
        a_year_ago = todays_date - datetime.timedelta(days=30 * 12)
        incomes = Income.objects.filter(owner=request.user, date__gte=a_year_ago, date__lte=todays_date)

        final_data = {}
        sources = list(set(map(self.get_source, incomes)))

        for income in incomes:
            for source in sources:
                final_data[source] = self.get_amount_for_category(incomes, source)

        return response.Response({'source_data': final_data}, status=status.HTTP_200_OK)
