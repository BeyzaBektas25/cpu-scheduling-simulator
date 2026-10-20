def run_srtf(process_list):
    """
    Preemptive SJF (Shortest Remaining Time First / SRTF) CPU Scheduling simülasyonu.
    """
    current_time = 0
    completed_processes = []
    gantt_chart = []
    
    # Orijinal proses nesnelerini ezmemek (yan etkileri önlemek) için 
    # simülasyona özel kopya nesneler oluşturuyoruz.
    sim_processes = []
    for p in process_list:
        new_p = Process(p.PID, p.Arrival_Time, p.Burst_Time, p.Priority)
        new_p.remaining_time = p.Burst_Time
        sim_processes.append(new_p)
        
    remaining = sim_processes.copy()

    last_executed_pid = None
    gantt_start_time = 0

    while remaining:
        # Şu anda çalışabilecek (gelmiş olan ve bitmemiş) prosesleri bul
        available = [
            p for p in remaining 
            if p.Arrival_Time <= current_time and p.remaining_time > 0
        ]

        if not available:
            # Eğer CPU boşta kalacaksa, önce devam eden aktif bir Gantt bloğu varsa kapat
            if last_executed_pid is not None:
                gantt_chart.append((last_executed_pid, gantt_start_time, current_time))
                last_executed_pid = None

            # Zamanı henüz gelmemiş en yakın prosesin varış zamanına atlat
            next_arrival = min(p.Arrival_Time for p in remaining if p.remaining_time > 0)
            gantt_chart.append(("IDLE", current_time, next_arrival))
            current_time = next_arrival
            continue

        # SRTF Seçimi (Preemption burada çalışır): 
        # Kalan süresi en az olan seçilir. Eşitlikte: Arrival_Time -> PID (Tie-break)
        selected = min(available, key=lambda p: (p.remaining_time, p.Arrival_Time, p.PID))

        # Gantt şeması için blok yönetimi (Aynı proses çalışmaya devam ediyorsa birleştirilir)
        if last_executed_pid != selected.PID:
            if last_executed_pid is not None:
                gantt_chart.append((last_executed_pid, gantt_start_time, current_time))
            last_executed_pid = selected.PID
            gantt_start_time = current_time

        # İlk kez CPU alıyorsa Response Time (RT) hesapla
        if selected.response_time == -1:
            selected.response_time = current_time - selected.Arrival_Time

        # 1 birim çalıştır
        selected.remaining_time -= 1
        current_time += 1

        # Proses tamamlandı mı kontrol et
        if selected.remaining_time == 0:
            selected.completion_time = current_time
            selected.calculate_metrics()  # TAT ve WT hesaplar
            completed_processes.append(selected)
            remaining.remove(selected)

    # Döngü bittiğinde son kalan prosesin Gantt bloğunu ekle
    if last_executed_pid is not None and last_executed_pid != "IDLE":
        gantt_chart.append((last_executed_pid, gantt_start_time, current_time))

    return completed_processes, gantt_chart