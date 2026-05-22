from locust import HttpUser, task, between


class STIEUser(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def health_check(self):
        self.client.get("/api/v1/health")

    @task(2)
    def list_reports(self):
        self.client.get("/api/v1/reports")

    @task(1)
    def search_reports(self):
        self.client.post("/api/v1/reports/search", json={"query": "satellite intrusion"})

    @task(1)
    def get_report(self):
        self.client.get("/api/v1/reports/STIE-TEST-001")

    @task(1)
    def network_status(self):
        self.client.get("/api/v1/network/status")

    @task(1)
    def analytics_summary(self):
        self.client.get("/api/v1/analytics/summary")
