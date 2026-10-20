def run_sjf(process_list):
    """
    Non-preemptive SJF (Shortest Job First) CPU Scheduling simülasyonu.
    """
    current_time = 0
    completed_processes = []
    gantt_chart = []
    
    # Orijinal listenin kopyasını alıyoruz
    remaining = process_list.copy()

    while remaining:
        # Şu anda çalışabilecek (gelmiş olan) prosesleri bul
        available = []
        for process in remaining:
            if process.Arrival_Time <= current_time:
                available.append(process)

        # Eğer o anda henüz hiçbir proses gelmediyse, zamanı en yakın prosesin varışına atlat
        if not available:
            next_arrival = min(p.Arrival_Time for p in remaining)
            gantt_chart.append(("IDLE", current_time, next_arrival))
            current_time = next_arrival
            continue

        # Available listesindeki proseslerden Burst_Time'ı en kısa olanı seç (Tie-break dahil)
        selected = min(available, key=lambda p: (p.Burst_Time, p.Arrival_Time, p.PID))

        # Prosesi çalıştır
        start_time = current_time
        current_time += selected.Burst_Time
        
        # Metrikleri güncelle
        selected.response_time = start_time - selected.Arrival_Time
        selected.completion_time = current_time
        selected.calculate_metrics()  # TAT ve WT hesaplar

        # Gantt şeması için bilgiyi sakla
        gantt_chart.append((selected.PID, start_time, current_time))

        # Tamamlanan prosesi listeler arası taşı
        completed_processes.append(selected)
        remaining.remove(selected)

    return completed_processes, gantt_chart
