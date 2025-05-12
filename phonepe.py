import streamlit as st
from streamlit_option_menu import option_menu
import pymysql
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import json
import requests


# Set Streamlit layout
st.set_page_config(layout="wide")
st.title("📱 PHONE PE DATA TRANSACTION INSIGHTS")

# Sidebar menu
with st.sidebar:
    st.write("👨‍💻 Writer: Aamir Sohail")
    selected = option_menu(
        menu_title="Main Menu",
        options=["HOME", "Business Case Study"],
        icons=["house", "bar-chart-line"],
        menu_icon="cast",
        default_index=0,
    )

# Display based on menu selection
if selected == "HOME":
    st.subheader("Welcome to the PhonePe Dashboard!")
    st.subheader("Domain: :green[Finance/Payment Systems]")
    st.subheader(":green[TECHNOLOGY USED]")
    st.markdown("Github Cloning, Python, Pandas, MySql, Plotly/Matplotlib and Streamlit")
    st.subheader("Overview")
    st.write(" The PhonePe Pulse Data Exploration and Visualization project aims to gather valuable information from PhonePe's GitHub repository, process the data, and present it using an interactive dashboard that's visually appealing. ")


# DataBase Connection
connection = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="Abby@123",
    database="phonepe_data"
)
cursor = connection.cursor()

# Function to execute SQL and return DataFrame
def run_query(query):
    cursor.execute(query)
    connection.commit()
    return pd.DataFrame(cursor.fetchall(), columns=[col[0] for col in cursor.description])

# Function to get map data for a given year and quarter
def map_data(years, quarter):
    query = f"""
    SELECT states AS state, SUM(transaction_amount) AS Total_Transaction_Value
    FROM map_transaction
    WHERE years = {years} AND quarter = {quarter}
    GROUP BY states;
    """
    return run_query(query)
    
# Function to prepare data for choropleth map 
def map_state(df):
    df['state'] = df['state'].str.title()  
    return df

# Business Case Study
if selected == "Business Case Study":
    selected_case = st.selectbox(
        "Select a Business Case", 
        [
            "1. Decoding Transaction Dynamics on PhonePe", 
            "2. Device Dominance and User Engagement Analysis", 
            "3. Transaction Analysis for Market Expansion", 
            "4. User Engagement and Growth Strategy",
            "5. Insurance Engagement Analysis"
            
        ]
    )

    if selected_case == "1. Decoding Transaction Dynamics on PhonePe":
        st.subheader(" Business Case 1: Decoding Transaction Dynamics")

        sub_question = st.selectbox(
            "Select a Sub-Question",
            [
                "1. Overall transaction volume by states and type",
                "2. Transaction trends across states over time",
                "3. Top growing payment categories by states and year",
                "4. Top 10 State-wise Total Transaction Amount",
                "5. Total Transaction Amount Analysis"
            ]
        )


        
        # Sub-Question 1
        if sub_question == "1. Overall transaction volume by states and type":
            query = """
            SELECT States, 
                   SUM(Transaction_count) AS Total_Count, 
                   SUM(Transaction_amount) AS Total_Amount
            FROM aggregated_transaction
            GROUP BY States
            """
            result_df = run_query(query)

            
            st.markdown("### Transaction Volume and Value by State")

            # Total Transaction Amount bar chart
            fig_amount = px.bar(
                    result_df,
                    x="States",
                    y="Total_Amount",
                    text="Total_Amount",
                    title="Total Transaction Amount by State",
                    labels={"States": "State", "Total_Amount": "Transaction Amount"},
                    color="Total_Amount",
                    color_continuous_scale="Blues",
                    height=700, 
                    width=900   
                )
                
            st.plotly_chart(fig_amount, use_container_width=True)

            # Total Transaction Count bar chart
            fig_count = px.bar(
                    result_df,
                    x="States",
                    y="Total_Count",
                    text="Total_Count",
                    title="Total Transaction Count by State",
                    labels={"States": "State", "Total_Count": "Transaction Count"},
                    color="Total_Count",
                    color_continuous_scale="Greens",
                    height=700, 
                    width=900 
                    )
                
            st.plotly_chart(fig_count, use_container_width=True)



        # Sub-Question 2
        elif sub_question == "2. Transaction trends across states over time":
            query = """
            SELECT 
                years,
                quarter,
                SUM(Transaction_count) AS Total_Transaction_Count, 
                SUM(Transaction_amount) AS Total_Transaction_Amount
            FROM aggregated_transaction
            GROUP BY years, quarter
            ORDER BY years, quarter;
            """
            result_df = run_query(query)

           
                
            #dropdown for year selection
            years_options = result_df["years"].unique()
            selected_year = st.selectbox("Select a Year", years_options)

            #filter data based on selected year
            filtered_df= result_df[result_df["years"] == selected_year]

                
            # Line chart for Transaction Amount and Count across Quarters
            filtered_df['Year_Quarter'] = filtered_df['years'].astype(str) + " Q" + filtered_df['quarter'].astype(str)

            col1, col2 = st.columns(2)
            with col1:
                    st.plotly_chart(
                        px.line(filtered_df, 
                                x="Year_Quarter", 
                                y="Total_Transaction_Amount", 
                                markers=True, 
                                title="Transaction Amount Trend Across Quarters")
                    )
            with col2:
                    st.plotly_chart(
                        px.line(filtered_df, 
                                x="Year_Quarter", 
                                y="Total_Transaction_Count", 
                                markers=True, 
                                title="Transaction Count Trend Across Quarters")
                                 )
                    
            #Bar chart using matplotlib
            st.subheader(f" Transactions for years {selected_year}")
            plt.figure(figsize=(10,6))
            plt.bar(filtered_df["quarter"].astype(str), filtered_df["Total_Transaction_Amount"], color= "skyblue")
            plt.xlabel("Quarter")
            plt.ylabel("Total Transaction Amount")
            plt.title(f"Transaction Amount Distribution for {selected_year}")
            plt.xticks(rotation=0)
            st.pyplot(plt)
                                
                
                  

        # Sub-Question 3: Top Growing Payment Categories by States and Year
        elif sub_question == "3. Top growing payment categories by states and year":
            query = """
            SELECT States, 
                Transaction_type, 
                Years AS Year,
                SUM(Transaction_count) AS Total_Count, 
                SUM(Transaction_amount) AS Total_Amount
            FROM aggregated_transaction
            GROUP BY States, Transaction_type, Year
            ORDER BY States, Year, Total_Amount DESC;
            """
            
            # Run the query and get the result
            result_df = run_query(query)

            
            # Ensure the correct data types
            result_df['Transaction_type'] = result_df['Transaction_type'].astype(str)
            result_df['Total_Amount'] = result_df['Total_Amount'].astype(float)
            result_df['Year'] = result_df['Year'].astype(int)

            # Display the full result DataFrame
            st.markdown("### Top Growing Payment Categories by States and Year")
                
            # Selectbox for the user to choose a state
            selected_state = st.selectbox("Select a State", options=result_df['States'].unique())
                
            # Selectbox for the user to choose a year
            selected_year = st.selectbox("Select a Year", options=result_df['Year'].unique())

            # Filter the data based on the selected state and year
            filtered_df = result_df[(result_df['States'] == selected_state) & (result_df['Year'] == selected_year)]

            # Display the filtered data
            st.markdown(f"#### Payment Categories in {selected_state} for {selected_year}")
            st.dataframe(filtered_df)

            # Create a pie chart for transaction amount distribution by payment type for the selected state and year
                
            pie_fig = px.pie(filtered_df, 
                                    names="Transaction_type", 
                                    values="Total_Amount",
                                    title=f"Transaction Amount Distribution by Payment Type in {selected_state} ({selected_year})",
                                    hole=0.4)  
            st.plotly_chart(pie_fig, use_container_width=True)
                


        # Sub-Question 4
        elif sub_question == "4. Top 10 State-wise Total Transaction Amount":
            query = """
            SELECT States, 
                   SUM(Transaction_amount) AS Total_Transaction_Amount
            FROM aggregated_transaction
            GROUP BY States
            ORDER BY Total_Transaction_Amount DESC
            LIMIT 10;
            """
            result_df = run_query(query)

            
            st.markdown("### Top 10 State-wise Total Transaction Amount")
                
            fig = px.bar(
                    result_df, 
                    x="States", 
                    y="Total_Transaction_Amount",
                    text="Total_Transaction_Amount", 
                    title="Total Transaction Amount By State",
                    labels={
                        "States": "State", 
                        "Total_Transaction_Amount": "Transaction Amount"
                    }
                )
                
                
            st.plotly_chart(fig)
                
            
        # Sub-Question 5
        if sub_question == "5. Total Transaction Amount Analysis":
            query = """
            SELECT DISTINCT years, quarter
            FROM aggregated_transaction
            ORDER BY years, quarter;
            """
            df = run_query(query)

            st.markdown("### Total Transaction Amount Analysis")
            col1, col2 = st.columns(2)
            with col1:
                y = st.select_slider("Years", list(df["years"].unique()))
            with col2:
                q = st.select_slider("Quarter", list(df["quarter"].unique()))

            # Get map and transaction data
            m = map_data(int(y), int(q))
            df_map = map_state(m)

            # Choropleth Map
            fig = px.choropleth(
                df_map,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey="properties.ST_NM",
                locations="state",
                color="Total_Transaction_Value",
                hover_name="state",
                hover_data={"Total_Transaction_Value": ":,.0f"},
                color_continuous_scale="Rainbow"
            )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)

            # Bar Chart
            st.markdown("### State-wise Total Transaction Value")
            bar_fig = px.bar(
                df_map.sort_values(by="Total_Transaction_Value", ascending=False),
                x="state",
                y="Total_Transaction_Value",
                color="Total_Transaction_Value",
                color_continuous_scale="Rainbow",
                labels={"Total_Transaction_Value": "Transaction Value"},
                title=f"Total Transaction Value by State - Q{q}, {y}"
            )
            bar_fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(bar_fig)


           
           

    if selected_case == "2. Device Dominance and User Engagement Analysis":
        st.subheader(" Business Case 2: Device Dominance and User Engagement Analysis")

        sub_question = st.selectbox(
        "Select a Sub-Question",
        [
            "1. Top 10 Districts with Most Users",
            "2. Registered Users vs App Opens Trend",
            "3. Yearly Growth of Registered Users",
            "4. Device Type Usage Distribution",
            "5. User Engagement Rate by State",
            "6. Device Preference by State"
            
        ]
        )
        # Sub-Question 1
        if sub_question == "1. Top 10 Districts with Most Users":
            query = """
            SELECT Districts, SUM(RegisteredUsers) AS total_users
            FROM map_user
            GROUP BY Districts
            ORDER BY total_users DESC
            LIMIT 10;
            """
            df = run_query(query)

            st.markdown("### Top 10 Districts by Registered Users")

            fig = px.bar(
                df,
                x="Districts",
                y="total_users",
                text="total_users",
                title="Top 10 Districts with Most Registered Users",
                labels={"Districts": "District", "total_users": "Registered Users"},
                color="Districts",
                height=600,
                width=800
            )

            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        # Sub-Question 2
        if sub_question == "2. Registered Users vs App Opens Trend":
            
            query = """
                    SELECT Years, 
                        SUM(RegisteredUsers) AS total_registered_users, 
                        SUM(AppOpens) AS total_app_opens
                    FROM map_user
                    GROUP BY Years
                    ORDER BY Years;
                    """

            # Run the query and store the result in a DataFrame
            result_df = run_query(query)

            # Ensure the result is not empty
            if result_df.empty:
                st.error("No data found.")
            else:
                # Plotting the trend of registered users and app opens over time
                fig = px.line(result_df, 
                            x='Years', 
                            y=['total_registered_users', 'total_app_opens'],
                            title='Registered Users vs App Opens Trend',
                            labels={'Years': 'Year', 'total_registered_users': 'Registered Users', 
                             'total_app_opens': 'App Opens', 'variable': 'Metric'}
                            )
                
                st.plotly_chart(fig, use_container_width=True)


        # Sub-Question 3
        elif sub_question == "3. Yearly Growth of Registered Users":
            query = """
            SELECT years, SUM(RegisteredUsers) AS total_users
            FROM map_user
            GROUP BY years
            ORDER BY years;
            """
            df = run_query(query)
            st.markdown("### Yearly Growth of Registered Users")
            fig = px.line(df,
                        x="years",
                        y="total_users",
                        markers=True,
                        title="Yearly Growth of Registered Users",
                        labels={"years": "Year", "total_users": "Registered Users"},
                        height=500,
                        width=900 
                    )

            fig.update_traces(line=dict(width=3), marker=dict(size=8))

            st.plotly_chart(fig, use_container_width=True)
       
        
        # Sub-Question 4
        elif sub_question == "4. Device Type Usage Distribution":
            query = """
            SELECT brands, SUM(transaction_count) AS total_users
            FROM aggregated_user
            GROUP BY brands
            ORDER BY total_users DESC
            LIMIT 10;
            """
            df = run_query(query)
            st.markdown("### Device Type Usage Distribution")
            fig = px.pie(df, names="brands", values="total_users", title="Device Brand Usage Share")
            st.plotly_chart(fig)

        # Sub-Question 5
        elif sub_question == "5. User Engagement Rate by State":
            query = """
                    SELECT States, 
                        SUM(RegisteredUsers) AS total_registered_users, 
                        SUM(AppOpens) AS total_app_opens, 
                        (SUM(AppOpens) / SUM(RegisteredUsers)) AS engagement_rate
                    FROM aggregated_user  -- Change to top_user or map_user as needed
                    GROUP BY States
                    ORDER BY engagement_rate DESC;
                    """

            # Run the query and store the result in a DataFrame
            result_df = run_query(query)

            fig = px.bar(result_df, 
                        x='States', 
                        y='engagement_rate',
                        title='User Engagement Rate by State',
                        color= 'States',
                        labels={'States': 'State', 'engagement_rate': 'Engagement Rate'},
                        height=600,
                        width=800
                        )
            
            st.plotly_chart(fig, use_container_width=True)

        # Sub-Question 6
        elif sub_question == "6. Device Preference by State":
            
            # SQL query to get device preference by region/state
            query = """
                    SELECT States, 
                        Brands, 
                        SUM(RegisteredUsers) AS num_users
                    FROM aggregated_user
                    GROUP BY States, Brands
                    ORDER BY States, num_users DESC;
                    """

            # Run the query and store the result in a DataFrame
            result_df = run_query(query)

            # Ensure the result is not empty
            if result_df.empty:
                st.error("No data found.")
            else:
                # Plotting the device preference by state using a stacked bar chart
                fig = px.bar(result_df, 
                            x='States', 
                            y='num_users',
                            color='Brands', 
                            title='Device Preference by Region/State',
                            labels={'States': 'State', 'num_users': 'Number of Registered Users'},
                            barmode='stack',
                            height=700,
                            width=900
                            )

                st.plotly_chart(fig, use_container_width=True)



    # Business Case 3: Transaction Analysis for Market Expansion
    if selected_case == "3. Transaction Analysis for Market Expansion":
        st.subheader(" Business Case 3: Transaction Analysis for Market Expansion")

        sub_question = st.selectbox(
        "Select a Sub-Question",
        [
            "1. Top 10 States by Total Transaction Amount",
            "2. State-wise Transaction Growth Over Time",
            "3. Transaction Type Usage by State",
            "4. Top Districts by Transaction Volume",
            "5. Top Transaction Types by Amount"
        ]
    )

        # Sub-Question 1
        #Which states show the highest total transaction amount?
        
        if sub_question == "1. Top 10 States by Total Transaction Amount":
            query = """
            SELECT States, SUM(Transaction_amount) AS Total_Amount
            FROM aggregated_transaction
            GROUP BY States
            ORDER BY Total_Amount DESC
            LIMIT 10;
            """
            df = run_query(query)
            st.markdown("### Top 10 States by Total Transaction Amount")
            fig = px.bar(
                        df,
                        x="States",
                        y="Total_Amount",
                        text="Total_Amount",
                        color="States",
                        title="Top 10 States by Total Transaction Amount",
                        labels={"States": "State", "Total_Amount": "Transaction Amount"},
                        height=600,
                        width=800,
                        color_discrete_sequence=px.colors.qualitative.Safe  # Beginner-friendly named palette
                        )
            fig.update_traces(textposition='outside')
            fig.update_layout(xaxis_tickangle=-45)

            st.plotly_chart(fig, use_container_width=True)

        # Sub-Question 2
        #Which states have shown the most growth over time?
        
        elif sub_question == "2. State-wise Transaction Growth Over Time":
            query = """
            SELECT Years, States, SUM(Transaction_amount) AS Total_Amount
            FROM aggregated_transaction
            GROUP BY Years, States
            ORDER BY Years, Total_Amount DESC;
            """
            df = run_query(query)
            st.markdown("### State-wise Transaction Growth Over Time")
            fig = px.line(
                        df,
                        x="Years",
                        y="Total_Amount",
                        color="States",
                        markers=True,
                        title="Yearly Transaction Growth by State",
                        labels={"Years": "Year", "Total_Amount": "Transaction Amount", "States": "State"},
                        color_discrete_sequence=px.colors.qualitative.Set2
                        )
            fig.update_layout(height=700, width=900)
            st.plotly_chart(fig, use_container_width=True)

        # Sub-Question 3
        #Which transaction types are most used in growing states?
        
        elif sub_question == "3. Transaction Type Usage by State":
            query = """
            SELECT States, Transaction_type, SUM(Transaction_amount) AS Total_Amount
            FROM aggregated_transaction
            GROUP BY States, Transaction_type
            ORDER BY States, Total_Amount DESC;
            """
            df = run_query(query)
            
             # Stacked Bar Chart
            st.markdown("#### Transaction Amount by Type and State")
            fig_stacked = px.bar(
                df,
                x="States",
                y="Total_Amount",
                color="Transaction_type",
                barmode="stack",
                title="Transaction Amount by Type and State",
                labels={"States": "State", "Total_Amount": "Transaction Amount", "Transaction_type": "Type"},
                height=800
            )
            st.plotly_chart(fig_stacked, use_container_width=True)

        # Sub-Question 4
        #What is the transaction volume at the district level?
        
        elif sub_question == "4. Top Districts by Transaction Volume":
            st.markdown("### Top Districts by Transaction Volume")

            # Dropdown to select top N
            top_n = st.selectbox("Select number of top districts", [5, 10, 15], index=1)

            query = f"""
            SELECT Districts, SUM(Transaction_amount) AS Total_Amount
            FROM map_transaction
            GROUP BY Districts
            ORDER BY Total_Amount DESC
            LIMIT {top_n};
            """
            df = run_query(query)
            
            fig = px.bar(
                df,
                x="Districts",
                y="Total_Amount",
                text="Total_Amount",
                title=f"Top {top_n} Districts by Transaction Volume",
                labels={"Districts": "District", "Total_Amount": "Transaction Volume"},
                color_discrete_sequence=px.colors.qualitative.Plotly,
                height=600
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(xaxis_tickangle=-45)

            st.plotly_chart(fig, use_container_width=True)


        # Sub-Question 5
        elif sub_question == "5. Top Transaction Types by Amount":
            query = """
            SELECT Transaction_type, SUM(Transaction_amount) AS Total_Amount
            FROM aggregated_transaction
            GROUP BY Transaction_type
            ORDER BY Total_Amount DESC;
            """
            df = run_query(query)

            st.markdown("### Top Transaction Types by Total Transaction Amount")

            fig = px.bar(
                df,
                x="Total_Amount",
                y="Transaction_type",
                orientation='h',
                text="Total_Amount",
                color_discrete_sequence=["indianred"],
                labels={"Transaction_type": "Transaction Type", "Total_Amount": "Transaction Amount"},
                title="Top Transaction Types by Amount"
            )

            fig.update_traces(textposition="outside")
            fig.update_layout(height=500)

            st.plotly_chart(fig, use_container_width=True)

        
     # Business Case 4: User Engagement and Growth Strategy
    if selected_case == "4. User Engagement and Growth Strategy":
        st.subheader(" Business Case 4: User Engagement and Growth Strategy") 

        sub_question = st.selectbox(
            "Select a Sub-Question",
            [
                "1. Total Registered Users by State",
                "2. User Growth Over Time",
                "3. App Open Frequency by State",
                "4. Top Districts by User Count"                
            ]
            )
        # Sub-Question 1
        if sub_question == "1. Total Registered Users by State":
            query = """
            SELECT States, SUM(RegisteredUsers) AS Total_Users
            FROM aggregated_user
            GROUP BY States
            ORDER BY Total_Users DESC;
            """
            df = run_query(query)
            st.markdown("### Total Registered Users by State")
            
            #Creating the bar chart
            fig = px.bar(df, x='States', y='Total_Users',
                        title="Total Registered Users by State",
                        labels={'Total_Users': 'Registered Users'},
                        color='Total_Users',
                        color_continuous_scale='Blues')

            fig.update_layout(xaxis_tickangle=-45)

            st.plotly_chart(fig)

        # Sub-Question 2
        elif sub_question == "2. User Growth Over Time":
            query = """
            SELECT Years, Quarter, SUM(RegisteredUsers) AS New_Users
            FROM top_user
            GROUP BY Years, Quarter
            ORDER BY Years, Quarter;
            """
            df = run_query(query)

            # Create Year_Quarter label
            df["Year_Quarter"] = df["Years"].astype(str) + " Q" + df["Quarter"].astype(str)

            # Calculate cumulative users over time
            df["Total_Users"] = df["New_Users"].cumsum()

            st.markdown("### User Growth Over Time")

            # Plot using Plotly for labeled axes
            import plotly.express as px
            fig = px.line(
                df,
                x="Year_Quarter",
                y="Total_Users",
                title="Cumulative User Growth Over Time",
                labels={"Year_Quarter": "Quarter", "Total_Users": "Total Registered Users"},
                height=500,
                width=800
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)


        # Sub-Question 3
        elif sub_question == "3. App Open Frequency by State":
            query = """
            SELECT States, SUM(AppOpens) AS Total_App_Opens
            FROM map_user
            GROUP BY States
            ORDER BY Total_App_Opens DESC;
            """
            df = run_query(query)
            st.markdown("### App Open Frequency by State")
            
            fig = px.bar(
                df, 
                x='States', 
                y='Total_App_Opens',
                title="App Open Frequency by State",
                labels={'Total_App_Opens': 'Total App Opens'},
                color='Total_App_Opens',
                color_continuous_scale='Blues'  
            )
            st.plotly_chart(fig)


        # Sub-Question 4
        elif sub_question == "4. Top Districts by User Count":
            query = """
            SELECT Districts, SUM(RegisteredUsers) AS Total_Users
            FROM map_user
            GROUP BY Districts
            ORDER BY Total_Users DESC
            LIMIT 10;
            """
            df = run_query(query)
            st.markdown("### Top 10 Districts by Registered Users")
            fig = px.bar(
                df,
                x='Districts',
                y='Total_Users',
                title='Top 10 Districts by Registered Users',
                labels={'Total_Users': 'Registered Users'},
                color='Total_Users',
                color_continuous_scale='Teal',
                height=500,
                width=800
                )
            st.plotly_chart(fig)

        
    # Business Case 5: Insurance Engagement Analysis    
    if selected_case == "5. Insurance Engagement Analysis":
        st.subheader(" Business Case 5: Insurance Engagement Analysis")
        
        sub_question = st.selectbox(
        "Select a Sub-Question",
        [
            "1. Total Insurance Transaction Value by State",
            "2. Insurance Growth Over Time by Year and Quarter",
            "3. Top 10 States with Highest Insurance Transactions",
            "4. Insurance Transactions at District Level",
            
        ]
    )
        # Sub-Question 1
        if sub_question == "1. Total Insurance Transaction Value by State":
            query = """
            SELECT States, SUM(Transaction_amount) AS Total_Insurance_Value
            FROM aggregated_insurance
            GROUP BY States
            ORDER BY Total_Insurance_Value DESC;
            """
            # Run your query and get the result as a DataFrame
            df = run_query(query)
            
            st.markdown("### Total Insurance Transaction Value by State")
            
            # Plotting with Matplotlib
            fig, ax = plt.subplots(figsize=(10, 6))  
            ax.bar(df['States'], df['Total_Insurance_Value'], color='skyblue')

            # Add labels and title
            ax.set_xlabel('States', fontsize=12)
            ax.set_ylabel('Total Insurance Transaction Value', fontsize=12)
            ax.set_title('Total Insurance Transaction Value by State', fontsize=14)
            
            # Rotate x-axis labels for better readability 
            plt.xticks(rotation=45, ha='right')

            
            st.pyplot(fig)

        # Sub-Question 2
        elif sub_question == "2. Insurance Growth Over Time by Year and Quarter":
            query = """
            SELECT Years, Quarter, SUM(Transaction_amount) AS Total_Insurance_Value
            FROM aggregated_insurance
            GROUP BY Years, Quarter
            ORDER BY Years, Quarter;
            """
            df = run_query(query)
            df["Year_Quarter"] = df["Years"].astype(str) + " Q" + df["Quarter"].astype(str)
            st.markdown("### Insurance Growth Over Time")
            st.line_chart(df.set_index("Year_Quarter"))

        # Sub-Question 3: Top 10 States with Highest Insurance Transactions
        elif sub_question == "3. Top 10 States with Highest Insurance Transactions":
            query = """
            SELECT States, SUM(Transaction_count) AS Total_Insurance_Count
            FROM top_insurance
            GROUP BY States
            ORDER BY Total_Insurance_Count DESC
            LIMIT 10;
            """
            df = run_query(query)
            
            # Display title
            st.markdown("### Top 10 States with Highest Insurance Transactions")
            
            # the bar chart using Matplotlib
            fig, ax = plt.subplots(figsize=(10, 6))  
            ax.bar(df['States'], df['Total_Insurance_Count'], color='orange')
            
            # Adding labels and title
            ax.set_xlabel('States', fontsize=12)
            ax.set_ylabel('Total Insurance Transactions', fontsize=12)
            ax.set_title('Top 10 States with Highest Insurance Transactions', fontsize=14)
            
            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45, ha='right')
            
            # Display the plot in Streamlit
            st.pyplot(fig)

        # Sub-Question 4
        elif sub_question == "4. Insurance Transactions at District Level":
            query = """
            SELECT Districts, SUM(Transaction_count) AS Insurance_Count
            FROM map_insurance
            GROUP BY Districts
            ORDER BY Insurance_Count DESC
            LIMIT 10;
            """
            df = run_query(query)
            # Display the title for the chart
            st.markdown("### Top 10 Districts by Insurance Transactions")
            
            # Create a bar chart using Plotly
            fig = px.bar(df, x='Districts', y='Insurance_Count', 
                        title="Top 10 Districts by Insurance Transactions", 
                        labels={'Districts': 'District', 'Insurance_Count': 'Insurance Transactions'},
                        color='Insurance_Count', 
                        color_continuous_scale='Blues') 
            
            
            # Show the plot in Streamlit
            st.plotly_chart(fig)

        

     