Tennis Analytics Dashboard Project Documentation
Author: ArunKumar K
Project Duration: 15 Days

Overview:
This project entailed the development of an interactive analytics dashboard for tennis competition data, leveraging the SportRadar API. The deliverables encompass a fully populated SQL database, automated API data retrieval scripts, a Streamlit-based visualization application, and detailed documentation. The primary goal was to extract, process, and visualize tennis-related data-including competitor rankings, competition details, and venue information-to provide actionable insights into player performance and event distributions.

















Setup Instructions:
To replicate this project, follow these steps:
1.	Environment Requirements: 
o	Python 3.9 or higher
o	MySQL 8.0 or higher
2.	Library Installation: Install the required Python libraries via the following command: pip install requests sqlalchemy mysql-connector-python pandas streamlit plotly or run requirements.txt
3.	Database Configuration:
o	Create a Myql database named tennis_analytics_db.
o	Use the credentials:
o	Username: root
o	Password: Password
4.	API Access: 
o	Acquire a SportRadar API key. 
5.	Execution Steps: 
o	Populate the database by running: python api_script.py, api_script2.py, api_script3.py.
o	Launch the Streamlit application with: streamlit run tennis_app.py










Project Workflow
	The project was completed over 14 days, with each focusing on specific objectives:

Competition Data Acquisition:
o	Objective: Ingest competition data from the SportRadar API.
o	Actions:
o	Retrieved 5,928 competition records from the /competitions.json endpoint.
o	Designed a relational schema with Competitions, Categories, and Venues tables.
o	Populated the MySQL database using SQLAlchemy.
o	Result: Established a foundational dataset for competitions and venues.

Rankings Data Integration:
o	Objective: Incorporate competitor rankings into the database.
o	Actions: 
o	Extracted 1,000 ranking entries from the /double_competitors_rankings.json endpoint.
o	Extended the schema with Competitors and Competitor_Rankings tables, linked via competitor_id.
o	Result: Enhanced the database with competitor performance data.

Database Optimization
o	Objective: Improve database performance.
o	Actions: 
o	Added indexes (e.g., CREATE INDEX idx_competitor_id ON Competitor_Rankings(competitor_id)).
o	Validated data consistency with row count verifications.
o	Result: Achieved efficient query execution.
Streamlit Application Development:
o	Objective: Build the visualization application.
o	Actions: 
o	Created five pages: Homepage Dashboard, Search and Filter Competitors, Competitor Details Viewer, Country-Wise Analysis, and Leaderboards.
o	Integrated filters and Plotly visualizations (e.g., bar and pie charts).
o	Result: Delivered a functional analytics interface.

Application Refinement:
o	Objective: Enhance the application’s functionality and design.
o	 Actions: 
o	Added "Competitions Analysis" and "Venues Map" pages.
o	Implemented CSV export for filtered data and applied CSS styling.
o	Result: Finalized a polished, user-friendly dashboard.












Database Schema Design
The tennis_analytics_db database comprises five interrelated tables:
Table Definitions
1.	Competitors (~500–1,000 rows): 
o	competitor_id (VARCHAR(50), Primary Key)
o	name (VARCHAR(100))
o	country (VARCHAR(100))
o	country_code (CHAR(3))
o	abbreviation (VARCHAR(10))
2.	Competitor_Rankings (1,000 rows): 
o	rank_id (INT, Primary Key, Auto-increment)
o	rank (INT)
o	movement (INT)
o	points (INT)
o	competitions_played (INT)
o	competitor_id (VARCHAR(50), Foreign Key to Competitors)
3.	Competitions (5,928 rows): 
o	competition_id (VARCHAR(50), Primary Key)
o	competition_name (VARCHAR(100))
o	type (VARCHAR(50))
o	gender (VARCHAR(10))
o	category_id (VARCHAR(50), Foreign Key to Categories)
4.	Categories (~50 rows): 
o	category_id (VARCHAR(50), Primary Key)
o	category_name (VARCHAR(100))
5.	Venues (~100–200 rows): 
o	venue_name (VARCHAR(100), Primary Key)
o	city_name (VARCHAR(100))
o	country_name (VARCHAR(100))
o	country_code (CHAR(3))
o	timezone (VARCHAR(100))
Relationships
o	Competitor_Rankings references Competitors via competitor_id (many-to-one).
o	Competitions references Categories via category_id (many-to-one).


















Challenges and Solutions
The project encountered several technical challenges, addressed as follows:
1.	Gender Filtering Constraint: 
o	Problem: Lack of gender data in Competitor_Rankings prevented gender-based competitor filtering.
o	Solution: Excluded gender filters; future integration of match data could resolve this.
2.	API Key Issues: 
o	Problem: Initial API failures due to misconfiguration and rate limits.
o	Solution: Secured a valid key and cached responses locally.
3.	Large Data Processing: 
o	Problem: Handling 5,928 competition records strained performance.
o	Solution: Employed pandas and SQLAlchemy for efficient data loading.
4.	Geospatial Visualization: 
o	Problem: Absence of venue coordinates hindered precise mapping.
o	Solution: Implemented a country-level choropleth map.










Key Insights
Data analysis revealed the following findings:
1.	Top Competitors: Pavic, Mate (Croatia) and Arevalo-Gonzalez (El Salvador) topped rankings with 7,620 points each across 23 competitions.
2.	Country Trends: ~50 countries represented; Croatia and Russia showed higher average points.
3.	Competition Breakdown: 5,928 events included diverse categories (e.g., ATP, ITF Men).
4.	Venue Hotspots: Predominantly USA and Europe, per the "Venues Map".

















Technical Implementation
API Integration
o	Tools: Python, requests, sqlalchemy, pandas
o	Endpoints: 
o	/competitions.json
o	/complexes.json
o	/double_competitors_rankings.json
o	Script: api_script.py, api_script2.py, api_script3.py automates data retrieval and storage.
Streamlit Application
o	File: tennis_app.py
o	Features: 
o	Seven pages with interactive filters, tables, and Plotly charts.
o	Data export to CSV.
o	Custom CSS styling.
o	Tools: streamlit, pandas, sqlalchemy, plotly.express













Conclusion
This project successfully converted raw SportRadar API data into a structured database and an interactive Streamlit dashboard, delivering insights into tennis rankings, competitions, and venues. The application highlights top performers and geographic trends through intuitive visualizations. Potential future enhancements include real-time data updates and match-level analytics.
Key Takeaways:
o	Relational schema design underscored the value of data interconnectivity.
o	Streamlit facilitated rapid development of data-driven applications.
o	Addressing API and scalability challenges strengthened technical expertise.

