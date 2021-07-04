from django.urls import path
from userstats import views

urlpatterns = [
    path('expenses-category/', views.ExpenseSummaryStats.as_view(), name="expenses-category"),
    path('incomes-source/', views.IncomeSummaryStats.as_view(), name="incomes-source"),
]
