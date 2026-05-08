"""
Нагрузочное тестирование API (Locust).

Запуск (предварительно поднять приложение, БД и Redis):
  locust -f tests/load/locustfile.py --host=http://127.0.0.1:8000

Веб-интерфейс: http://localhost:8089
"""

from __future__ import annotations

from locust import HttpUser, between, task


class TradingApiUser(HttpUser):
    wait_time = between(0.5, 2.0)

    @task(3)
    def trading_dates(self) -> None:
        self.client.get("/api/v1/trading/dates/", params={"last_days": 10})

    @task(2)
    def trading_dynamics(self) -> None:
        self.client.get(
            "/api/v1/trading/dynamics/",
            params={"start_date": "2026-01-01", "end_date": "2026-01-31"},
        )

    @task(2)
    def trading_results(self) -> None:
        self.client.get("/api/v1/trading/results/", params={"limit": 50})

    @task(1)
    def health(self) -> None:
        self.client.get("/health")
