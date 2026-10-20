import unittest
import sys
import os

# Proje klasörünü Python path'ine ekliyoruz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.process import Process
from src.models.round_robin import round_robin


class TestRoundRobinAlgorithm(unittest.TestCase):

    def test_round_robin_normal_case(self):
        """Round Robin'in quantum kullanarak prosesleri sırayla çalıştırmasını test eder."""

        processes = [
            Process("P1", 0, 5),
            Process("P2", 0, 3),
            Process("P3", 1, 2)
        ]

        completed, gantt = round_robin(processes, quantum=2)

        # Beklenen çalışma sırası:
        # P1: 0-2
        # P2: 2-4
        # P3: 4-6
        # P1: 6-8
        # P2: 8-9
        # P1: 9-10

        execution_order = [item[0] for item in gantt]

        self.assertEqual(
            execution_order,
            ["P1", "P2", "P3", "P1", "P2", "P1"]
        )

        # P1 kontrolleri
        p1 = next(p for p in completed if p.PID == "P1")
        self.assertEqual(p1.completion_time, 10)
        self.assertEqual(p1.turnaround_time, 10)
        self.assertEqual(p1.waiting_time, 5)
        self.assertEqual(p1.response_time, 0)

        # P2 kontrolleri
        p2 = next(p for p in completed if p.PID == "P2")
        self.assertEqual(p2.completion_time, 9)
        self.assertEqual(p2.turnaround_time, 9)
        self.assertEqual(p2.waiting_time, 6)
        self.assertEqual(p2.response_time, 2)

        # P3 kontrolleri
        p3 = next(p for p in completed if p.PID == "P3")
        self.assertEqual(p3.completion_time, 6)
        self.assertEqual(p3.turnaround_time, 5)
        self.assertEqual(p3.waiting_time, 3)
        self.assertEqual(p3.response_time, 3)


    def test_round_robin_cpu_idle_case(self):
        """İlk proses gelmeden önce CPU'nun IDLE kalmasını test eder."""

        processes = [
            Process("P1", 3, 4),
            Process("P2", 5, 2)
        ]

        completed, gantt = round_robin(processes, quantum=2)

        # CPU 0-3 arasında boş olmalı
        self.assertEqual(
            gantt[0],
            ("IDLE", 0, 3)
        )

        # P1: 3-5
        # P2: 5-7
        # P1: 7-9

        execution_order = [item[0] for item in gantt]

        self.assertEqual(
            execution_order,
            ["IDLE", "P1", "P2", "P1"]
        )

        p1 = next(p for p in completed if p.PID == "P1")
        p2 = next(p for p in completed if p.PID == "P2")

        self.assertEqual(p1.completion_time, 9)
        self.assertEqual(p2.completion_time, 7)


    def test_invalid_quantum(self):
        """Quantum değerinin 0 veya negatif olmasını engeller."""

        processes = [
            Process("P1", 0, 5)
        ]

        with self.assertRaises(ValueError):
            round_robin(processes, quantum=0)


if __name__ == "__main__":
    unittest.main()