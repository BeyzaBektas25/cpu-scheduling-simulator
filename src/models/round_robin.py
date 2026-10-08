from collections import deque

def round_robin(processes, quantum):
    if quantum <= 0:
        raise ValueError("Quantum pozitif olmalıdır.")

    ready_queue = deque()
    current_time = 0
    next_index = 0
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

        # Kuyruğun başındaki process'i al
        process = ready_queue.popleft()

        # İlk kez CPU alıyorsa response time hesapla
        if process.response_time == -1:
            process.response_time = current_time - process.Arrival_Time

        # Process'in bu turda ne kadar çalışacağını belirle
        run_time = min(quantum, process.remaining_time)

        start_time = current_time
        current_time += run_time
        process.remaining_time -= run_time

        # Gantt chart'a ekle
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

        # Process tamamlanmadıysa kuyunun sonuna gönder
        if process.remaining_time > 0:
            ready_queue.append(process)

        # Process tamamlandıysa
        else:
            process.completion_time = current_time
            process.calculate_metrics()

    return processes, gantt_chart

