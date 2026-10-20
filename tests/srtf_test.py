import unittest
import sys
import os

# src klasöründeki kodları import edebilmek için yol tanımı
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.process import Process
from src.models.srtf import run_srtf  # Yazdığınız SRTF fonksiyonu

class TestSRTFAlgorithm(unittest.TestCase):

    def test_srtf_preemption_and_metrics(self):
        """
        Senaryo:
        - P1: AT=0, BT=8  (0'da başlar, 2'de kesilir. Kalan: 6)
        - P2: AT=2, BT=3  (2'de başlar, 3'te kesilir. Kalan: 2)
        - P3: AT=3, BT=1  (3'te başlar, 4'te biter. CT = 4)
        - P2: 4'te tekrar başlar, 6'da biter. CT = 6
        - P1: 6'da tekrar başlar, 12'de biter. CT = 12
        """
        processes = [
            Process("P1", 0, 8),
            Process("P2", 2, 3),
            Process("P3", 3, 1)
        ]
        
        completed, gantt = run_srtf(processes)
        
        # Gantt şeması akış kontrolü
        expected_gantt = [
            ("P1", 0, 2),
            ("P2", 2, 3),
            ("P3", 3, 4),
            ("P2", 4, 6),
            ("P1", 6, 12)
        ]
        self.assertEqual(gantt, expected_gantt, "SRTF Gantt şeması akışı hatalı!")
        
        # P3 Kontrolleri (İlk biten, CT = 4)
        p3 = next(p for p in completed if p.PID == "P3")
        self.assertEqual(p3.completion_time, 4)
        self.assertEqual(p3.turnaround_time, 1)  # 4 - 3 = 1
        self.assertEqual(p3.waiting_time, 0)     # 1 - 1 = 0
        self.assertEqual(p3.response_time, 0)    # 3 - 3 = 0 (İlk CPU alış anı - AT)

        # P2 Kontrolleri (İkinci biten, CT = 6)
        p2 = next(p for p in completed if p.PID == "P2")
        self.assertEqual(p2.completion_time, 6)
        self.assertEqual(p2.turnaround_time, 4)  # 6 - 2 = 4
        self.assertEqual(p2.waiting_time, 1)     # 4 - 3 = 1
        self.assertEqual(p2.response_time, 0)    # 2 - 2 = 0

        # P1 Kontrolleri (En son biten, CT = 12)
        p1 = next(p for p in completed if p.PID == "P1")
        self.assertEqual(p1.completion_time, 12)
        self.assertEqual(p1.turnaround_time, 12) # 12 - 0 = 12
        self.assertEqual(p1.waiting_time, 4)     # 12 - 8 = 4
        self.assertEqual(p1.response_time, 0)    # 0 - 0 = 0

    def test_srtf_cpu_idle_case(self):
        """CPU'nun ilk başta boşta kaldığı (IDLE) senaryoyu test eder."""
        processes = [
            Process("P1", 3, 4) # Zaman 3'te geliyor
        ]
        
        completed, gantt = run_srtf(processes)
        
        # 0 ile 3 arası IDLE olmalı
        self.assertEqual(gantt[0], ("IDLE", 0, 3), "CPU IDLE durumu Gantt şemasına yanlış yansımış.")
        self.assertEqual(gantt[1], ("P1", 3, 7))
        
        p1 = next(p for p in completed if p.PID == "P1")
        self.assertEqual(p1.completion_time, 7)

    def test_srtf_tie_break(self):
        """Kalan süreleri aynı olduğunda deterministik tie-break kuralının (Arrival_Time -> PID) çalıştığını test eder."""
        processes = [
            Process("P2", 0, 4),
            Process("P1", 0, 4)
        ]

        completed, gantt = run_srtf(processes)

        # İkisinin de AT=0 ve remaining_time=4 olduğu başlangıçta PID'si küçük olan (P1) seçilmeli
        self.assertEqual(gantt[0][0], "P1", "Eşitlik durumunda (tie-break) küçük PID seçilmedi!")


if __name__ == "__main__":
    unittest.main()