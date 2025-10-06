from locust import HttpUser, task, between

class ProjectUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        """Simulates user login."""
        self.client.post("/showSummary", {"email": "admin@irontemple.com"})

    @task
    def view_leaderboard(self):
        """Simulates viewing the leaderboard."""
        self.client.get("/leaderboard")

    @task
    def book_competition(self):
        """Simulates booking one place in a competition."""
        self.client.post("/purchasePlaces", {
            "club": "Iron Temple",
            "competition": "Spring Festival",
            "places": "1"
        })