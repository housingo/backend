import time
from locust import HttpUser, task, between


guest_acc = {
    "username": "guest",
    "password": "guestpass123",
}


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    # @task
    # def register(self):
    #     self.client.post(url="/api/users/register")

    @task
    def register(self):
        self.client.get(url="/")

    @task
    def login(self):
        self.client.post(url="/api/users/login", json=guest_acc)
