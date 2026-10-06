import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.process import Process
from src.round_robin import run_round_robin

class TestRoundRobinAlgorithm(unittest.TestCase):

    def test_round_robin_basic(self):
        """Round Robin algoritmasının zaman dilimlerine göre bölünmesini test eder."""
        # Zaman Kuantumu (Time Quantum) = 2 olsun
        # P1: AT=0, BT=5 -> Zaman 0-2 arası çalışır, kalan 3 olur. Sıranın arkasına geçer.
        # P2: AT=1, BT=3 -> Zaman 2-4 arası çalışır, kalan 1 olur. Sıranın arkasına geçer.
        processes = [
            Process("P1", 0, 5),
            Process("P2", 1, 3)
        ]
        
        completed, gantt = run_round_robin(processes, time_quantum=2)
        
        # Gantt şeması sırasıyla: P1(0-2) -> P2(2-4) -> P1(4-6) -> P2(6-7) -> P1(7-8) olmalı
        expected_gantt = [
            ("P1", 0, 2),
            ("P2", 2, 4),
            ("P1", 4, 6),
            ("P2", 4, 7), # Not: Kodun yapısına göre tam aralıklar eşleşmeli
        ]
        
        # Gantt şemasında ilk iki adımın doğruluğunu teyit edelim
        self.assertEqual(gantt[0], ("P1", 0, 2))
        self.assertEqual(gantt[1], ("P2", 2, 4))
        
        # P2 prosesinin bitiş zamanı kontrolü: 
        # P1(0-2) -> P2(2-4) -> P1(4-6) -> P2(6-7) -> P2 burada biter (CT=7)
        p2 = next(p for p in completed if p.PID == "P2")
        self.assertEqual(p2.completion_time, 7)
        # TAT = CT - AT = 7 - 1 = 6
        # WT = TAT - BT = 6 - 3 = 3
        self.assertEqual(p2.waiting_time, 3)

if __name__ == "__main__":
    unittest.main()

