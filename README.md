# 🏏 Cricbuzz LiveStats  
### Real-Time Cricket Insights & SQL-Based Analytics

🚀 A full-stack cricket analytics dashboard built using **Python, SQL, and Streamlit**, integrating real-time data from the Cricbuzz API.

---

## 📌 Overview
Cricbuzz LiveStats transforms live cricket data into structured insights. It allows users to track live matches, analyze player performance, and run advanced SQL queries on stored data.

---

## ✨ Features
- ⚡ Real-time match updates via API  
- 📊 Player performance analytics  
- 🧮 25+ SQL queries (Beginner → Advanced)  
- 🛠️ CRUD operations for database  
- 🌐 Interactive multi-page Streamlit dashboard  

---

## 🏗️ Tech Stack
- **Python** – Backend logic  
- **SQL** – Database & analytics  
- **Streamlit** – Frontend UI  
- **REST API** – Cricbuzz data  
- **Pandas** – Data processing  

---

## 📂 Project Structure

cricbuzz_livestats/
│── app.py # Main Streamlit app
│── requirements.txt # Dependencies
│── README.md # Project documentation
│
├── pages/ # Streamlit pages
│ ├── live_matches.py
│ ├── player_stats.py
│ ├── sql_analytics.py
│ ├── crud_operations.py
│
├── utils/ # Helper modules
│ ├── db_connection.py
│ ├── api_fetch.py
│ ├── data_processing.py
│
├── database/ # SQL scripts
│ ├── schema.sql
│ ├── sample_data.sql
│
└── assets/ # Static files (images/icons)



---

## ⚙️ Installation & Setup

```bash
# Clone the repository
git clone https://github.com/your-username/cricbuzz-livestats.git

# Navigate to project folder
cd cricbuzz-livestats

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
