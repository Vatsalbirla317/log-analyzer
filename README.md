# 📊 Log Analyzer Dashboard

A smart log monitoring and anomaly detection tool built with **Streamlit**, **SQLite**, and **Machine Learning**.

This project parses `.log` or `.json` files, detects error spikes, and visualizes them on a real-time dashboard — perfect for understanding system health.

---

## 🔧 Features

- 📤 Upload `.log` or `.json` files
- 🔎 Parse & filter logs by **Service** and **Level**
- 🧠 Detect anomalies using **Isolation Forest**
- 🗃️ Store logs in a local **SQLite** database
- 📈 Visualize error spikes (bar chart)
- 🔁 Auto-refresh for real-time monitoring
- ☁️ **Live Streamlit Cloud deployment**

---

## 🚀 Tech Stack

| Layer            | Tools Used                         |
|------------------|-------------------------------------|
| Programming      | Python, Pandas                     |
| Machine Learning | Scikit-learn (Isolation Forest)    |
| Dashboard        | Streamlit                          |
| Backend Storage  | SQLite                             |
| Deployment       | Streamlit Cloud                    |

---

## 📍 Live Demo

🔗 [Log Analyzer App (Hosted on Streamlit)](https://log-analyzer-dwye9xy4pwgfhlqrzgsxvh.streamlit.app/)

---

## 🖼️ Architecture

![Architecture](./assets/architecture.png)

1. **User uploads** `.log`/`.json` files via Streamlit UI  
2. File is parsed using custom `parser.py`  
3. Anomalies are detected using `IsolationForest` in `anomaly.py`  
4. Filtered logs shown + error spikes visualized  
5. Logs optionally stored in SQLite via `storage.py`  
6. App auto-refreshes every 10 sec for real-time updates  

---

## 📄 How to Run Locally

```bash
git clone https://github.com/Vatsalbirla317/log-analyzer.git
cd log-analyzer
pip install -r requirements.txt
streamlit run dashboard.py
