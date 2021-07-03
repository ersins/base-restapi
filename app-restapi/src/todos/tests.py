from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from todos.models import Todo


class TestListCreateTodos(APITestCase):

    def authentication(self):
        self.client.post(reverse('register'),
                         {'username': 'username1', 'email': 'emai1l@gmail.com', 'password': 'password'})
        response = self.client.post(reverse('login'),
                                    {'username': 'username1', 'email': 'emai1l@gmail.com', 'password': 'password'})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")

    def test_should_not_create_todo_with_no_auth(self):
        sample_todo = {'title': 'title32mm', 'desc': 'açıklama'}
        response = self.client.post(reverse('todos'), sample_todo)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_create_todo(self):
        previous_todo_cont = Todo.objects.all().count()
        self.authentication()
        sample_todo = {'title': 'title32', 'desc': 'açıklama'}
        response = self.client.post(reverse('todos'), sample_todo)
        self.assertEqual(Todo.objects.all().count(), previous_todo_cont + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
