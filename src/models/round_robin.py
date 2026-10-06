from collections import deque

def round_robin(processes, quantum):
    if quantum <= 0:
        raise ValueError("Quantum pozitif olmalıdır.")

    ready_queue = deque()   ##processler kuyruğa alınır.
    current_time = 0
    next_index = 0   ##ready queue'ya eklenmemiş ilk processin listedeki yerini gösteriyor.

    for process in processes:
        if process.arrival_time <= current_time:
            ready_queue.append(process)

    while ready_queue:
        process = ready_queue.popleft()

        run_time = min(quantum, process.remaining_time)

        process.remaining_time -= run_time
        current_time += run_time

        for new_process in processes:
            if new_process.arrival_time <= current_time and new_process not in ready_queue:
                ready_queue.append(new_process)

        if process.remaining_time > 0:
            ready_queue.append(process)
        
