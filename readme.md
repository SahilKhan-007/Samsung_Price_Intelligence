# Samsung Price Intelligence — Data Analysis

## 📌 Project Overview

This project presents an end-to-end data analysis of Samsung smartphones using a custom GSMArena web scraping pipeline and exploratory data analysis (EDA) in Python.

The objective is to analyze:

- 📈 Evolution of Samsung smartphone hardware over time  
- 🔍 Trends in specifications like RAM, Battery, Display, Storage  
- 📊 Comparison across Galaxy series (S, A, M, Z, F)  
- 🧠 Product positioning and market strategy insights  

The project includes the full data workflow:
web scraping → data cleaning → feature engineering → EDA → visualization → insights.

---

## 🏢 About Samsung

:contentReference[oaicite:0]{index=0} is a global leader in smartphone manufacturing.

Galaxy lineup:

- **Galaxy S** → Flagship devices  
- **Galaxy A / M / F** → Mid-range & budget segment  
- **Galaxy Z** → Foldable premium devices  

This analysis explores how these product lines evolved over time.

---

## 📂 Dataset Information

### Data Source
- GSMArena web scraping pipeline  
- File: `samsung_features.csv`

### Features

- Model Name  
- Release Year  
- RAM (GB)  
- Storage (GB)  
- Battery Capacity (mAh)  
- Display Size (inches)  
- Performance Score (engineered feature)  
- Series (S, A, M, Z, F)  
- Device Age  

---

## 🧠 Project Workflow

### 1. Data Collection
- Scraped smartphone data using BeautifulSoup  
- Stored structured output in CSV format  

### 2. Data Cleaning
- Handled missing values  
- Fixed inconsistent formats  
- Converted data types  

### 3. Exploratory Data Analysis (EDA)
- Used Pandas, NumPy, Matplotlib, Seaborn  
- Generated statistical summaries and visual insights  

---

## 📈 Key Analysis

### RAM Trends
- Continuous increase in average RAM over years  
- Flagship devices lead memory upgrades  

### Battery Trends
- Stabilized around ~5000 mAh in recent years  
- Hardware limitations affect further growth  

### Display Trends
- Screen sizes steadily increasing  
- Shift toward media consumption devices  

---

## 📊 Series Comparison

### Galaxy Series Insights

- **S Series** → Premium innovation  
- **A / M / F Series** → Mass-market devices  
- **Z Series** → Foldable experimental devices  

---

## 🔗 Correlation Analysis

Key relationships:

- RAM strongly impacts performance  
- Storage moderately affects performance  
- Battery shows weak correlation with performance  
- Older devices tend to have lower performance scores  

---

## 📅 Release Trends

- Increasing number of mid-range launches  
- Strong expansion of Galaxy A and M series  
- Foldable devices emerging in recent years  
- Flagships remain limited and premium  

---

## 📌 Key Insights

- RAM and performance have a strong positive relationship  
- Battery capacity has plateaued around 5000 mAh  
- Samsung focuses heavily on mid-range markets  
- Foldables represent premium innovation strategy  

---

## 🚀 Future Improvements

- Add price dataset for price-performance analysis  
- Build ML model for price prediction  
- Compare with other smartphone brands  
- Perform forecasting on hardware evolution trends  

---

## 🛠️ Tools Used

- Python  
- BeautifulSoup  
- Pandas  
- NumPy  
- Matplotlib  
- Seaborn  
- Jupyter Notebook  

---

## ⚠️ Disclaimer

This project is created strictly for **educational and learning purposes only**.

All data used in this project has been collected from publicly available information on :contentReference[oaicite:0]{index=0} through web scraping techniques.

- No personal, private, or sensitive data has been collected  
- The data is used only for academic and non-commercial analysis  
- This project does not claim ownership of any third-party content  
- All trademarks, brand names, and product information belong to their respective owners  

This project demonstrates skills in web scraping, data cleaning, exploratory data analysis (EDA), and data visualization.

If any content owner has concerns, the relevant data can be modified or removed upon request.

---

## 👨‍💻 Author

**Sahil Khan**  
Data Analyst | Python | SQL | Power BI | Machine Learning  