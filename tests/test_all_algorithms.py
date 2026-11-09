import unittest
from src.models.process import Process
from src.models.fcfs import run_fcfs
from src.models.sjf import run_sjf
from src.models.srtf import run_srtf
from src.models.priority import run_priority
from src.models.round_robin import round_robin


class TestCpuSchedulingAlgorithms(unittest.TestCase):
    def setUp(self):
        # Standart test süreçleri: (PID, Arrival_Time, Burst_Time, Priority)
        self.sample_processes = [
            Process(1, 0, 6, 2),
            Process(2, 1, 4, 1),
            Process(3, 2, 2, 3),
        ]

    def test_fcfs(self):
        completed, gantt = run_fcfs(self.sample_processes)
        self.assertEqual(len(completed), 3)
        # FCFS sırası: P1(0-6), P2(6-10), P3(10-12)
        p1 = next(p for p in completed if p.PID == 1)
        p2 = next(p for p in completed if p.PID == 2)
        p3 = next(p for p in completed if p.PID == 3)
        self.assertEqual(p1.completion_time, 6)
        self.assertEqual(p2.completion_time, 10)
        self.assertEqual(p3.completion_time, 12)
        self.assertTrue(len(gantt) >= 3)

    def test_sjf(self):
        completed, _ = run_sjf(self.sample_processes)
        # P1(0-6) bittikten sonra kısa olan P3(6-8), sonra P2(8-12) çalışır
        p3 = next(p for p in completed if p.PID == 3)
        p2 = next(p for p in completed if p.PID == 2)
        self.assertEqual(p3.completion_time, 8)
        self.assertEqual(p2.completion_time, 12)

    def test_srtf(self):
        completed, _ = run_srtf(self.sample_processes)
        # Preemptive: P1(0-1), P2(1-2), P3(2-4), P2(4-7), P1(7-12)
        p3 = next(p for p in completed if p.PID == 3)
        self.assertEqual(p3.completion_time, 4)

    def test_priority(self):
        completed, _ = run_priority(self.sample_processes)
        self.assertEqual(len(completed), 3)
        for p in completed:
            self.assertGreaterEqual(p.turnaround_time, p.Burst_Time)
            self.assertGreaterEqual(p.waiting_time, 0)

    def test_round_robin(self):
        completed, gantt = round_robin(self.sample_processes, quantum=2)
        self.assertEqual(len(completed), 3)
        # Quantum=2 olduğu için en az 6 zaman dilimi parçası oluşmalı
        self.assertGreaterEqual(len(gantt), 6)

    def test_round_robin_invalid_quantum(self):
        with self.assertRaises(ValueError):
            round_robin(self.sample_processes, quantum=0)


if __name__ == "__main__":
    unittest.main()
