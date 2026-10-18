from tkinter import CURRENT

def run_priority(process_list):
    #küçük priority değeri daha önce işleneceği anlamına gelir.

    current_time = 0
    completed_processes = []
    gantt_chart = []

    remaining = process_list.copy() #orjinal listenin kopyasını al.

    while remaining:
        #şu anda çalışabilecek processleri bul.

        available = []
        for process in remaining:
            if process.Arrival_Time <= current_time:
                available.append(process)

        # Henüz hiçbir process gelmediyse zamanı en yakın varışa atlat.
        if not available:
            next_arrival = min(p.Arrival_Time for p in remaining)
            gantt_chart.append(("IDLE", current_time, next_arrival))
            continue

        # Priority değeri en küçük olan processi seç
        selected = min(available, key=lambda p: (p.Priority, p.Arrival_Time, p.PID))

        #process tamamlanana kadar çalıştır (non-preemptive)
        start_time = current_time
        current_time = current_time + selected.Burst_Time

        #process metriklerini güncelle
        selected.response_time = start_time - selected.Arrival_Time 
        selected.completion_time = current_time
        selected.calculate_metrics()

        #gantt şemasını ekle
        gantt_chart.append((selected.PID, start_time, current_time))

        #tamamlanan processi listelerden çıkar
        completed_processes.append(selected)
        remaining.remove(selected)

    #güncellenmiş processleri ve gantt şemasını döndür
    return completed_processes, gantt_chart
