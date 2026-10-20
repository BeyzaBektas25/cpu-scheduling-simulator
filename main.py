
from src.models.process import Process
from src.models.sjf import run_sjf


def main():
    # Örnek prosesler oluştur
    processes = [
        Process(1, 0, 7),
        Process(2, 2, 4),
        Process(3, 4, 1)
    ]

    # SJF algoritmasını çalıştır
    completed_processes, gantt_chart = run_sjf(processes)

    # Proses sonuçlarını yazdır
    print("SJF Algorithm Results")
    print("---------------------")

    for process in completed_processes:
        print(
            f"PID: {process.PID} | "
            f"AT: {process.Arrival_Time} | "
            f"BT: {process.Burst_Time} | "
            f"CT: {process.completion_time} | "
            f"TAT: {process.turnaround_time} | "
            f"WT: {process.waiting_time} | "
            f"RT: {process.response_time}"
        )

    # Gantt şemasını yazdır
    print("\nGantt Chart")
    print("-----------")

    for item in gantt_chart:
        print(item)


if __name__ == "__main__":
    main()
