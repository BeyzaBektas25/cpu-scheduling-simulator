import random
import psutil
import pandas as pd
import plotly.express as px
import streamlit as st

from src.models.process import Process
from src.models.fcfs import run_fcfs
from src.models.sjf import run_sjf
from src.models.srtf import run_srtf
from src.models.priority import run_priority
from src.models.round_robin import round_robin

st.set_page_config(page_title="OS CPU Scheduling Simulator", page_icon="⚙️", layout="wide")

st.title("⚙️ İşletim Sistemleri — CPU Zamanlama (Scheduling) Simülatörü")
st.markdown(
    "Bu simülatör; **sentetik süreçler**, **rastgele OS yükü** veya **şu an bilgisayarınızda çalışan gerçek Windows/Linux süreçleri** üzerinde 5 farklı CPU zamanlama algoritmasını analiz eder."
)

# --- SOL MENÜ: SİMÜLASYON AYARLARI ---
st.sidebar.header("🎛️ Simülasyon Parametreleri")

data_source = st.sidebar.radio(
    "1. Veri Kaynağı Seçin:",
    ["Manuel Süreç Listesi", "Canlı Bilgisayar Süreçleri (Gerçek OS)", "Rastgele OS Yükü Üret"],
)

algo_options = [
    "FCFS (First Come First Served)",
    "SJF (Non-Preemptive)",
    "SRTF (Preemptive SJF)",
    "Priority Scheduling",
    "Round Robin",
]

selected_algo = st.sidebar.selectbox("2. Zamanlama Algoritması:", algo_options)
quantum = st.sidebar.slider("Round Robin Time Quantum (ms):", min_value=1, max_value=10, value=2)
context_switch = st.sidebar.number_input("Context Switch Maliyeti (ms):", min_value=0.0, max_value=5.0, value=0.0, step=0.5)

# --- VERİ KAYNAĞI OLUŞTURMA ---
processes_data = []

if data_source == "Manuel Süreç Listesi":
    st.subheader("📋 Süreç Tablosu (Düzenlenebilir)")
    default_df = pd.DataFrame([
        {"PID": 1, "Arrival_Time": 0, "Burst_Time": 7, "Priority": 2, "Process_Name": "System_Init"},
        {"PID": 2, "Arrival_Time": 2, "Burst_Time": 4, "Priority": 1, "Process_Name": "Chrome.exe"},
        {"PID": 3, "Arrival_Time": 4, "Burst_Time": 1, "Priority": 3, "Process_Name": "VSCode.exe"},
        {"PID": 4, "Arrival_Time": 5, "Burst_Time": 4, "Priority": 2, "Process_Name": "Spotify.exe"},
    ])
    edited_df = st.data_editor(default_df, num_rows="dynamic", use_container_width=True)
    for _, row in edited_df.iterrows():
        if pd.notna(row["PID"]) and pd.notna(row["Arrival_Time"]) and pd.notna(row["Burst_Time"]):
            processes_data.append({
                "PID": int(row["PID"]),
                "AT": int(row["Arrival_Time"]),
                "BT": max(1, int(row["Burst_Time"])),
                "PR": int(row["Priority"]) if pd.notna(row["Priority"]) else 0,
                "Name": str(row.get("Process_Name", f"P{int(row['PID'])}"))
            })

elif data_source == "Canlı Bilgisayar Süreçleri (Gerçek OS)":
    st.subheader("🖥️ Bilgisayarınızda Şu An Çalışan Gerçek Süreçler (psutil)")
    proc_count = st.slider("Çekilecek Canlı Süreç Sayısı:", 3, 12, 6)
    if st.button("🔄 Bilgisayardan Anlık Süreçleri Çek") or "live_procs" not in st.session_state:
        live_list = []
        for idx, p in enumerate(psutil.process_iter(['pid', 'name', 'cpu_times'])):
            try:
                info = p.info
                cpu_t = info['cpu_times']
                burst = max(1, min(15, int((cpu_t.user + cpu_t.system) % 12) + 1)) if cpu_t else random.randint(2, 8)
                live_list.append({
                    "PID": info['pid'],
                    "Arrival_Time": idx * 2,
                    "Burst_Time": burst,
                    "Priority": random.randint(1, 5),
                    "Process_Name": info['name']
                })
                if len(live_list) >= proc_count:
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        st.session_state["live_procs"] = live_list

    live_df = pd.DataFrame(st.session_state["live_procs"])
    st.dataframe(live_df, use_container_width=True)
    for _, row in live_df.iterrows():
        processes_data.append({
            "PID": int(row["PID"]), "AT": int(row["Arrival_Time"]),
            "BT": int(row["Burst_Time"]), "PR": int(row["Priority"]), "Name": row["Process_Name"]
        })

else:
    st.subheader("🎲 Rastgele İşletim Sistemi Süreç Yükü")
    n_procs = st.slider("Süreç Adedi:", 3, 15, 5)
    rand_df = pd.DataFrame([
        {"PID": i + 1, "Arrival_Time": i * 2, "Burst_Time": random.randint(2, 10), "Priority": random.randint(1, 5), "Process_Name": f"Task_{i+1}"}
        for i in range(n_procs)
    ])
    st.dataframe(rand_df, use_container_width=True)
    for _, row in rand_df.iterrows():
        processes_data.append({
            "PID": int(row["PID"]), "AT": int(row["Arrival_Time"]),
            "BT": int(row["Burst_Time"]), "PR": int(row["Priority"]), "Name": row["Process_Name"]
        })

# --- SİMÜLASYONU ÇALIŞTIRMA FONKSİYONU ---
def execute_algorithm(algo_name, proc_dicts):
    procs = [Process(p["PID"], p["AT"], p["BT"], p["PR"]) for p in proc_dicts]
    if algo_name.startswith("FCFS"):
        return run_fcfs(procs)
    elif algo_name.startswith("SJF"):
        return run_sjf(procs)
    elif algo_name.startswith("SRTF"):
        return run_srtf(procs)
    elif algo_name.startswith("Priority"):
        return run_priority(procs)
    elif algo_name.startswith("Round Robin"):
        return round_robin(procs, quantum)
    return run_fcfs(procs)

if st.button("▶️ Simülasyonu Başlat", type="primary") and processes_data:
    completed, gantt = execute_algorithm(selected_algo, processes_data)

    # Context Switch ve CPU Verimliliği Hesabı
    total_burst = sum(p.Burst_Time for p in completed)
    active_blocks = [g for g in gantt if (g[0] if isinstance(g, tuple) else g.get("PID")) != "IDLE"]
    cs_count = max(0, len(active_blocks) - 1)
    total_cs_time = cs_count * context_switch
    max_ct = max(p.completion_time for p in completed) + total_cs_time
    cpu_utilization = (total_burst / max_ct * 100) if max_ct > 0 else 100

    avg_tat = sum(p.turnaround_time for p in completed) / len(completed)
    avg_wt = sum(p.waiting_time for p in completed) / len(completed)
    avg_rt = sum(p.response_time for p in completed) / len(completed)

    # Üst Metrik Kartları
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ortalama Bekleme (Avg WT)", f"{avg_wt:.2f} ms")
    c2.metric("Ortalama Dönüş (Avg TAT)", f"{avg_tat:.2f} ms")
    c3.metric("Ortalama Yanıt (Avg RT)", f"{avg_rt:.2f} ms")
    c4.metric("CPU Kullanım Oranı", f"%{cpu_utilization:.1f}", f"{cs_count} Context Switch")

    # Sonuç Tablosu
    st.subheader("📊 Süreç Zamanlama Metrikleri")
    res_df = pd.DataFrame([
        {
            "PID": p.PID,
            "Arrival Time (AT)": p.Arrival_Time,
            "Burst Time (BT)": p.Burst_Time,
            "Priority": p.Priority,
            "Completion Time (CT)": p.completion_time,
            "Turnaround Time (TAT)": p.turnaround_time,
            "Waiting Time (WT)": p.waiting_time,
            "Response Time (RT)": p.response_time,
        }
        for p in completed
    ])
    st.dataframe(res_df, use_container_width=True)

    # Renkli Gantt Şeması
    st.subheader("📈 Görsel Gantt Şeması (CPU Zaman Çizelgesi)")
    gantt_rows = []
    for item in gantt:
        if isinstance(item, dict):
            pid = item.get("PID") or item.get("pid")
            start = item.get("start")
            end = item.get("end")
        else:
            pid, start, end = item[0], item[1], item[2]
        label = "CPU Boşta (IDLE)" if pid == "IDLE" else f"PID {pid}"
        gantt_rows.append({"Süreç": label, "Başlangıç": start, "Bitiş": end, "Süre": end - start})

    gantt_df = pd.DataFrame(gantt_rows)
    fig = px.bar(
        gantt_df,
        x="Süre",
        y="Süreç",
        base="Başlangıç",
        color="Süreç",
        orientation="h",
        text="Süre",
        title=f"{selected_algo} — CPU Çalışma Zaman Çizelgesi",
    )
    fig.update_layout(xaxis_title="Zaman (ms)", yaxis_title="Süreç (PID)", height=380)
    st.plotly_chart(fig, use_container_width=True)

    # Tüm Algoritmaları Kıyaslama Tablosu
    st.subheader("🏆 5 Algoritmanın Performans Karşılaştırması")
    comp_rows = []
    for opt in algo_options:
        try:
            c_procs, c_gantt = execute_algorithm(opt, processes_data)
            c_active = [g for g in c_gantt if (g[0] if isinstance(g, tuple) else g.get("PID")) != "IDLE"]
            comp_rows.append({
                "Algoritma": opt,
                "Ort. Bekleme Süresi (WT)": round(sum(p.waiting_time for p in c_procs) / len(c_procs), 2),
                "Ort. Dönüş Süresi (TAT)": round(sum(p.turnaround_time for p in c_procs) / len(c_procs), 2),
                "Ort. Yanıt Süresi (RT)": round(sum(p.response_time for p in c_procs) / len(c_procs), 2),
                "Bağlam Değiştirme (CS)": max(0, len(c_active) - 1),
            })
        except Exception:
            pass
    if comp_rows:
        st.dataframe(pd.DataFrame(comp_rows), use_container_width=True)

