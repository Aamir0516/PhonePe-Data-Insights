# PhonePe Pulse Data Insights Project

This project is a comprehensive data engineering and analytics solution built using the PhonePe Pulse dataset. It involves extracting real-time data from JSON files, storing it in a MySQL database, performing data transformation using Python and SQL, and visualizing insights using Streamlit.

## 🔍 Key Features

* 🔄 **Data Extraction & Processing**: Python scripts parse raw JSON data from the PhonePe Pulse repository across transaction, user, and insurance metrics.
* 🗃️ **MySQL Integration**: Cleaned data is loaded into structured MySQL tables for scalable querying.
* 📈 **Streamlit Dashboard**: Interactive web app to explore national, state, and district-level insights.
* 🔧 **Modular Script Design**: Organized into 9 components for each data category and directory structure.
* 📚 **End-to-End Workflow**: Includes extraction, transformation, loading (ETL), and visualization steps.

## 📂 Tech Stack

* **Languages**: Python, SQL
* **Database**: MySQL
* **Visualization**: Plotly/Matplotlib, Streamlit
* **Data Source**: [PhonePe Pulse](https://github.com/PhonePe/pulse)

## 🚀 Use Case

Ideal for analyzing digital payment trends, insurance adoption, and user behavior across India using real transaction data.

## ⚙️ Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/phonepe-pulse-insights.git
   cd phonepe-pulse-insights
   ```

2. **Install Required Libraries**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure MySQL Database**:

   * Create a database named `phonepe_data` in MySQL.
   * Update the database credentials in the Python script (`phonepe.py`).

4. **Run the Streamlit App**:

   ```bash
   streamlit run phonepe.py
   ```

## 📝 Author

**Aamir Sohail**

Email: [aamirofficial2022@gmail.com](mailto:aamirofficial2022@gmail.com)

