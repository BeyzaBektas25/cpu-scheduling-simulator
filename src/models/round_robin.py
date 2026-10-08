from collections import deque

def round_robin(processes, quantum):
    if quantum <= 0:
        raise ValueError("Quantum pozitif olmalıdır.")

    ready_queue = deque() # boş kuyruk oluşturuluyor
    current_time = 0
    next_index = 0 # ilk process'in yeri
    gantt_chart = []

    # Arrival Time'a göre sırala
    processes = sorted(processes, key=lambda p: p.Arrival_Time)

    while next_index < len(processes) or ready_queue:

        # Kuyruk boşsa, zamanı bir sonraki process'in gelişine götür
        if not ready_queue:
            if current_time < processes[next_index].Arrival_Time:
                gantt_chart.append(
                    ("IDLE", current_time, processes[next_index].Arrival_Time)
                )
                current_time = processes[next_index].Arrival_Time

            ready_queue.append(processes[next_index])
            next_index += 1

        # Kuyruğun başındaki process alınıyor
        process = ready_queue.popleft()

        # İlk kez CPU alıyorsa response time hesapla
        if process.response_time == -1:
            process.response_time = current_time - process.Arrival_Time

        # Process'in bu turda ne kadar çalışacağını belirleniyor
        run_time = min(quantum, process.remaining_time)

        start_time = current_time  #başlangıç zamanını kaydediyoruz
        current_time += run_time
        process.remaining_time -= run_time

        # CPU'nun boş kaldığı zaman gantt'a ekleniyor
        gantt_chart.append(
            (process.PID, start_time, current_time)
        )

        # Bu sürede gelen yeni processleri kuyruğa ekle
        while (
            next_index < len(processes)
            and processes[next_index].Arrival_Time <= current_time
        ):
            ready_queue.append(processes[next_index])
            next_index += 1

        # Process tamamlanmadı mı kontrol ediliyor, bitmediyse kuyruğun sonuna gidiyor
        if process.remaining_time > 0:
            ready_queue.append(process)

        else:
            process.completion_time = current_time  # bitiş zamanı kaydediliyor
            process.calculate_metrics()   # turnaround time, waiting time hesaplanılıyor

    return processes, gantt_chart

