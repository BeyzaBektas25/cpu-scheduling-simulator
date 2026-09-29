class Process:
    def _init_(self, pid: int, arrival_time: int, burst_time: int):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        
        # Çalışma sırasında hesaplanacak metrikler
        self.remaining_time = burst_time  
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = -1  # Henüz CPU'yu almadığını gösterir
        
    def calculate_metrics(self):
        self.turnaround_time = self.completion_time - self.arrival_time
        self.waiting_time = self.turnaround_time - self.burst_time

    def _repr_(self):
        return f"Process(PID={self.pid}, AT={self.arrival_time}, BT={self.burst_time})"
