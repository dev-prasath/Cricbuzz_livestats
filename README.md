# 🏏 Cricbuzz LiveStats – Real-Time Cricket Insights & SQL-Based Analytics

A powerful cricket analytics dashboard built using **Python, Streamlit, SQL, and Cricbuzz API** that provides real-time cricket updates, player statistics, advanced SQL analytics, and interactive CRUD operations.

This project combines **Sports Analytics**, **Database Management**, and **Web Development** into a single interactive platform.

---

# 📌 Project Overview

Cricbuzz LiveStats is a real-time cricket analytics application that fetches live match data using Cricbuzz API and stores structured cricket data in a SQL database for advanced analysis.

The platform enables users to:

- 📡 Track live cricket matches
- 📊 Analyze player performance
- 🧮 Execute advanced SQL analytical queries
- 🛠 Perform CRUD operations on records
- 📈 Visualize cricket insights interactively

---

# 🚀 Features

## 📡 Live Match Dashboard
- Real-time live cricket scores
- Match status updates
- Team and player statistics
- Venue and innings details
- Live batting & bowling scorecards

---

## 📊 Player Analytics
- Top run scorers
- Highest wicket takers
- Batting average analysis
- Strike rate comparison
- Bowling economy statistics
- Performance trend tracking

---

## 🧮 SQL Analytics Module
Includes **25+ SQL analytical queries** categorized into:

### 🟢 Beginner Level
- Basic SELECT queries
- GROUP BY operations
- ORDER BY sorting
- Filtering records

### 🟡 Intermediate Level
- JOIN operations
- Aggregate functions
- Subqueries
- Performance analysis

### 🔴 Advanced Level
- Window Functions
- Common Table Expressions (CTEs)
- Time-Series Analysis
- Ranking Systems
- Match Prediction Analytics

---

## 🛠 CRUD Operations
Interactive form-based database operations:

- ➕ Add new records
- ✏️ Update player statistics
- ❌ Delete records
- 📖 Read & manage data

---

## 🌐 Interactive Streamlit UI
- Multi-page dashboard
- Responsive UI design
- Interactive charts & tables
- Dynamic navigation system

---

# 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend Logic |
| Streamlit | Web Application |
| SQL | Database & Analytics |
| REST API | Fetch Live Data |
| Pandas | Data Processing |
| Requests | API Handling |
| SQLite / PostgreSQL / MySQL | Database Storage |
| Plotly | Data Visualization |

---

# 📂 Project Structure

```bash
cricbuzz_livestats/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
│
├── pages/
│   ├── home.py
│   ├── live_matches.py
│   ├── top_players.py
│   ├── sql_queries.py
│   └── crud_operations.py
│
├── utils/
│   ├── api.py
│   ├── db_connection.py
│   ├── helpers.py
│   └── queries.py
│
├── database/
│   ├── schema.sql
│   ├── sample_data.sql
│   └── setup_db.py
│
├── assets/
│   ├── images/
│   └── icons/
│
└── notebooks/
    └── analysis.ipynb
```

---

# ⚙️ Installation Guide

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/cricbuzz-livestats.git
cd cricbuzz-livestats
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### ▶ Activate Virtual Environment

### Windows
```bash
venv\Scripts\activate
```

### Mac/Linux
```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 📦 Requirements

Create a `requirements.txt` file with:

```txt
streamlit
pandas
requests
sqlalchemy
plotly
python-dotenv
sqlite3
psycopg2
mysql-connector-python
```

---

# 🔑 API Configuration

Create a `.env` file in the root directory:

```env
CRICBUZZ_API_KEY=your_api_key_here
```

---

# 🗄 Database Configuration

## SQLite Setup

```bash
python database/setup_db.py
```

---

## PostgreSQL/MySQL Setup

Update database credentials inside:

```python
utils/db_connection.py
```

Example:

```python
DB_HOST = "localhost"
DB_NAME = "cricket_db"
DB_USER = "root"
DB_PASSWORD = "password"
```

---

# ▶️ Running the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

---

# 📊 Dashboard Pages

## 🏠 Home Page
- Project introduction
- Features overview
- Navigation menu
- Documentation access

---

## 🏏 Live Match Page
Displays:
- Ongoing matches
- Live scorecards
- Batting & bowling details
- Match venue and status

---

## 👤 Top Players Page
Displays:
- Most runs
- Highest scores
- Most wickets
- Best strike rates
- Top bowling performances

---

## 🧮 SQL Analytics Page
Includes:
- 25+ analytical SQL queries
- Cricket performance insights
- Player trend analysis
- Match statistics

---

## 🛠 CRUD Operations Page
Allows:
- Adding new players
- Editing player records
- Removing entries
- Managing match data

---

# 📈 SQL Analytics Included

## Beginner Queries
- Find players by country
- Top ODI scorers
- Venue capacity analysis
- Team win statistics

---

## Intermediate Queries
- Home vs away performance
- Batting partnerships
- Bowling analysis by venue
- Player consistency metrics

---

## Advanced Queries
- Toss impact analysis
- Player ranking systems
- Match prediction analytics
- Career progression tracking
- Quarterly performance trends

---

# 🎯 Business Use Cases

## 📺 Sports Broadcasting
- Live match analytics
- Commentary insights
- Historical performance data

---

## 🎮 Fantasy Cricket Platforms
- Player form tracking
- Team selection analytics
- Match predictions

---

## 📈 Cricket Analytics Companies
- Performance evaluation
- Statistical modeling
- Team strategy analysis

---

## 🎓 Educational Institutions
- SQL learning with real-world datasets
- API integration practice
- Database management concepts

---

# 🛡 Best Practices Followed

- ✅ PEP 8 Coding Standards
- ✅ Modular Project Structure
- ✅ Proper Error Handling
- ✅ Secure API Key Management
- ✅ Optimized SQL Queries
- ✅ Scalable Database Design
- ✅ Clean UI/UX Design

---

# 🔥 Future Enhancements

- AI-based match prediction
- Player recommendation engine
- Advanced data visualizations
- Authentication system
- Cloud deployment
- Mobile responsive design

---

# 📚 Learning Outcomes

By building this project, you will learn:

- REST API Integration
- SQL Query Optimization
- Streamlit Dashboard Development
- Database Connectivity
- Data Visualization
- CRUD Operations
- Sports Data Analytics
- Real-Time Data Processing

---

# 🤝 Contributing

Contributions are welcome!

## Steps to Contribute

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Added new feature"
```

4. Push changes

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# ⭐ Support

If you found this project useful:

- ⭐ Star this repository
- 🍴 Fork the project
- 🧠 Share with others

---

