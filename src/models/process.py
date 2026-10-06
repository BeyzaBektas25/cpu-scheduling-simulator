class Process:
    def __init__(self, PID, Arrival_Time, Burst_Time, Priority=0):
        self.PID=PID
        self.Arrival_Time = Arrival_Time
        self.Burst_Time = Burst_Time
        self.Priority=Priority
        
        # Çalışma sırasında hesaplanacak metrikler
        self.remaining_time = burst_time  
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = -1  # Henüz CPU'yu almadığını gösterir
        
    def calculate_metrics(self):
        self.turnaround_time = self.completion_time - self.Arrival_Time
        self.waiting_time = self.turnaround_time - self.Burst_Time

   def __repr__(self):
        return f"Process({self.PID}, AT={self.Arrival_Time}, BT={self.Burst_Time})"
