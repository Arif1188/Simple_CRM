from locust import HttpUser, task, between

class CRMUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://16.170.231.182:8000"  # Your EC2 public IP and port

    @task
    def view_home(self):
        self.client.get("/")

    @task
    def view_catalogue(self):
        self.client.get("/catalogue")

    @task
    def create_lead(self):
        self.client.post("/leads", json={
            "name": "Test",
            "email": "test@example.com",
            "message": "Locust test"
        })
