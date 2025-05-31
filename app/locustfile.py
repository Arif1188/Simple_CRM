from locust import HttpUser, task, between
import random
import string

class LeadUser(HttpUser):
    wait_time = between(1, 3)  # wait between 1-3 seconds between tasks
    
def random_email():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + "@example.com"

class LeadUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)  # weight of this task
    def list_leads(self):
        self.client.get("/leads")

    @task(1)
    def add_lead(self):
        self.client.post("/leads/add", data={
            "name": "Load Test User",
            "email": random_email(),
            "phone": "1234567890"
        })

    @task(2)
    def get_lead_detail(self):
        # Assuming lead with id=1 exists
        self.client.get("/leads/1")
