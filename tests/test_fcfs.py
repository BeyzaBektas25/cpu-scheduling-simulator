import unittest
import sys
import os

# src klasöründeki kodları import edebilmek için yol tanımı yapıyoruz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.process import Process
from src.fcfs import run_fcfs

class TestFCFSAlgorithm(unittest.TestCase):

    def test_normal_case(self):
        """Kağıt üzerinde çözdüğümüz standart senaryoyu test eder."""
        processes = [
            Process("P1", 0, 5),
            Process("P2", 1, 3),
            Process("P3", 2, 2)
        ]
        
        completed, _ = run_fcfs(processes)
        
        # P1 için kontroller
        self.assertEqual(completed[0].completion_time, 5)
        self.assertEqual(completed[0].turnaround_time, 5)
        self.assertEqual(completed[0].waiting_time, 0)
        
        # P2 için kontroller
        self.assertEqual(completed[1].completion_time, 8)
        self.assertEqual(completed[1].turnaround_time, 7)
        self.assertEqual(completed[1].waiting_time, 4)
        
        # P3 için kontroller
        self.assertEqual(completed[2].completion_time, 10)
        self.assertEqual(completed[2].turnaround_time, 8)
        self.assertEqual(completed[2].waiting_time, 6)

    def test_cpu_idle_case(self):
        """CPU'nun arada boş (idle) kaldığı senaryoyu test eder."""
        processes = [
            Process("P1", 0, 3),
            Process("P2", 5, 2)  # P1 bittikten (zaman 3) sonra 2 birim zaman CPU boş kalmalı
        ]
        
        completed, gantt = run_fcfs(processes)
        
        # Gantt şemasında IDLE durumu oluşmuş mu kontrol et
        has_idle = any(item[0] == "IDLE" for item in gantt)
        self.assertTrue(has_idle, "CPU boş kalma durumu Gantt şemasına yansımamış!")
        
        # P2 zaman 5'te başlayıp 2 birim çalışmalı, yani 7'de bitmeli
        self.assertEqual(completed[1].completion_time, 7)
        self.assertEqual(completed[1].waiting_time, 0)

if __name__ == "__main__":
    unittest.main()

