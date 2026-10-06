def run_fcfs(process_list):
    """
    FCFS CPU Scheduling simülasyonunu çalıştırır.
    Girdi olarak Process nesnelerinden oluşan bir liste alır.
    """
    # 1. Prosesleri varış zamanlarına göre sırala (Eğer eşitse geliş sırasına göre kalırlar)
    sorted_processes = sorted(process_list, key=lambda p: p.Arrival_Time)
    
    current_time = 0  # Simülasyon zaman sayacı
    gantt_chart = []  # Görsel şema oluşturmak için zaman logları
    
    for process in sorted_processes:
        # Eğer CPU boşta kalmışsa (Mevcut zaman, prosesin varış zamanından küçükse)
        if current_time < process.Arrival_Time:
            # CPU'nun boş kaldığı aralığı kaydet
            gantt_chart.append(("IDLE", current_time, process.Arrival_Time))
            current_time = process.Arrival_Time # Zamanı prosesin geldiği ana ilerlet
            
        # Proses CPU'yu ilk kez alıyor (FCFS'te tepki zamanı CPU'ya girdiği andır)
        process.response_time = current_time - process.Arrival_Time
        
        # Prosesin başlama ve bitiş anını Gantt şeması için kaydet
        start_time = current_time
        current_time += process.Burst_Time
        process.completion_time = current_time
        
        gantt_chart.append((process.PID, start_time, current_time))
        
        # Metrik hesaplama fonksiyonunu çağırıyoruz (TAT ve WT hesaplar)
        process.calculate_metrics()
        
    return sorted_processes, gantt_chart
