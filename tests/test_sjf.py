import unittest
import sys
import os

# src klasöründeki kodları import edebilmek için yol tanımı yapıyoruz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.process import Process
from src.sjf import run_sjf

class TestSJFAlgorithm(unittest.TestCase):

    def test_sjf_shortest_job_first(self):
        """Kısa olan prosesin öne geçme durumunu (SJF mantığını) test eder."""
        # Senin verdiğin örnek:
        # P1: AT=0, BT=5
        # P2: AT=0, BT=2  <- Aynı anda geldiler, P2 daha kısa olduğu için önce başlamalı
        # P3: AT=1, BT=3
        processes = [
            Process("P1", 0, 5),
            Process("P2", 0, 2),
            Process("P3", 1, 3)
        ]
        
        completed, gantt = run_sjf(processes)
        
        # Gantt şeması sırası P2 -> P3 -> P1 şeklinde olmalı
        execution_order = [item[0] for item in gantt]
        self.assertEqual(execution_order, ["P2", "P3", "P1"], "SJF sıralaması hatalı! Kısa olan iş öne geçmedi.")
        
        # Proses bazlı metrik kontrolleri
        # P2: Zaman 0'da başlar, 2'de biter. WT = 0
        p2 = next(p for p in completed if p.PID == "P2")
        self.assertEqual(p2.completion_time, 2)
        self.assertEqual(p2.waiting_time, 0)
        
        # P3: Zaman 2'de başlar, 3 birim çalışır, 5'te biter. WT = 2 - 1 = 1
        p3 = next(p for p in completed if p.PID == "P3")
        self.assertEqual(p3.completion_time, 5)
        self.assertEqual(p3.waiting_time, 1)
        
        # P1: Zaman 5'te başlar, 5 birim çalışır, 10'da biter. WT = 5 - 0 = 5
        p1 = next(p for p in completed if p.PID == "P1")
        self.assertEqual(p1.completion_time, 10)
        self.assertEqual(p1.waiting_time, 5)

    def test_sjf_cpu_idle_case(self):
        """CPU'nun ilk başta boş kaldığı ve sonradan kısa işin seçildiği senaryoyu test eder."""
        processes = [
            Process("P1", 3, 4), # Zaman 3'te geliyor
            Process("P2", 4, 1)  # Zaman 4'te geliyor (P1 çalışırken gelecek ama kesintisiz olduğu için bekleyecek)
        ]
        
        completed, gantt = run_sjf(processes)
        
        # İlk başta IDLE olmalı (0 ile 3 arası)
        self.assertEqual(gantt[0], ("IDLE", 0, 3), "CPU boş kalma (IDLE) durumu Gantt şemasına yanlış yansımış.")
        
        # P1 zaman 3'ten 7'ye kadar çalışır
        p1 = next(p for p in completed if p.PID == "P1")
        self.assertEqual(p1.completion_time, 7)

if __name__ == "__main__":
    unittest.main()
