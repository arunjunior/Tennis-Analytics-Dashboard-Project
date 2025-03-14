import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import base64

# MySQL connection
MYSQL_USER = "root"
MYSQL_PASSWORD = "password"
MYSQL_HOST = "localhost"
MYSQL_DB = "tennis_analytics_db"
engine = create_engine(f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}")

# Fetch data function
@st.cache_data
def fetch_data(query):
    return pd.read_sql(query, engine)

# Load data
competitors_query = """
    SELECT c.competitor_id, c.name, c.country, cr.rank, cr.movement, cr.points, cr.competitions_played
    FROM Competitors c
    JOIN Competitor_Rankings cr ON c.competitor_id = cr.competitor_id
"""
competitions_query = """
    SELECT c.competition_id, c.competition_name, c.type, c.gender, cat.category_name
    FROM Competitions c
    LEFT JOIN Categories cat ON c.category_id = cat.category_id
"""
venues_query = """
    SELECT v.venue_name, v.city_name, v.country_name, v.country_code, v.timezone
    FROM Venues v
"""
df_competitors = fetch_data(competitors_query)
df_competitions = fetch_data(competitions_query)
df_venues = fetch_data(venues_query)

# Function for CSV download
def get_csv_download_link(df, filename="data.csv"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV</a>'
    return href

# Streamlit app
st.title("Tennis Analytics Dashboard")

# Custom Sidebar Styling with CSS
st.sidebar.markdown("""
    <style>
    /* Sidebar background and padding */
    [data-testid="stSidebar"] {
        background-color: #000000;
        padding: 20px;
        border-right: 2px solid #ddd;
    }
    /* Styled title */
    .sidebar-title {
        font-size: 24px;
        font-weight: bold;
        color: #FFFFFF;
        margin-bottom: 20px;
        text-align: center;
    }
    /* Radio button container */
    .stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    /* Radio button labels */
    .stRadio label {
        font-size: 16px;
        color: #34495e;
        padding: 10px;
        border-radius: 5px;
        background-color: #000000;
        transition: all 0.3s ease;
    }
    /* Hover effect */
    .stRadio label:hover {
        background-color: #666666;
        color: #1abc9c;
    }
    /* Selected radio button */
    .stRadio [role="radiogroup"] [aria-checked="true"] {
        background-color: #1abc9c;
        color: white;
    }
    /* Footer styling */
    .sidebar-footer {
        font-size: 14px;
        color: #7f8c8d;
        text-align: center;
        margin-top: 30px;
        border-top: 1px solid #ddd;
        padding-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.markdown('<div class="sidebar-title">Navigation</div>', unsafe_allow_html=True)
page = st.sidebar.radio("", [  # Empty label, styled via CSS
    "Homepage Dashboard",
    "Search and Filter Competitors",
    "Competitor Details Viewer",
    "Country-Wise Analysis",
    "Leaderboards",
    "Competitions Analysis",
    "Venues Map"
], key="nav")

# Homepage Dashboard
if page == "Homepage Dashboard":
    st.header("Homepage Dashboard")
    total_competitors = len(df_competitors['competitor_id'].unique())
    num_countries = len(df_competitors['country'].unique())
    max_points = df_competitors['points'].max()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Competitors", total_competitors)
    col2.metric("Countries Represented", num_countries)
    col3.metric("Highest Points", max_points)
    top_10 = df_competitors.nlargest(10, 'points')[['name', 'points']]
    fig = px.bar(top_10, x='name', y='points', title="Top 10 Competitors by Points")
    st.plotly_chart(fig)

# Search and Filter Competitors
elif page == "Search and Filter Competitors":
    st.header("Search and Filter Competitors")
    search_term = st.text_input("Search by Competitor Name", "")
    filtered_df = df_competitors[df_competitors['name'].str.contains(search_term, case=False, na=False)] if search_term else df_competitors
    rank_min, rank_max = st.slider("Rank Range", 1, int(df_competitors['rank'].max()), (1, 50))
    countries = st.multiselect("Country", options=df_competitors['country'].unique(), default=[])
    points_threshold = st.number_input("Points Threshold", min_value=0, value=0)
    if countries:
        filtered_df = filtered_df[filtered_df['country'].isin(countries)]
    filtered_df = filtered_df[
        (filtered_df['rank'].between(rank_min, rank_max)) &
        (filtered_df['points'] >= points_threshold)
    ]
    st.dataframe(filtered_df[['name', 'rank', 'points', 'country']])
    st.markdown(get_csv_download_link(filtered_df, "filtered_competitors.csv"), unsafe_allow_html=True)

# Competitor Details Viewer
elif page == "Competitor Details Viewer":
    st.header("Competitor Details Viewer")
    competitor_names = df_competitors['name'].unique()
    selected_competitor = st.selectbox("Select Competitor", competitor_names)
    details = df_competitors[df_competitors['name'] == selected_competitor].iloc[0]
    st.write(f"**Name**: {details['name']}")
    st.write(f"**Rank**: {details['rank']}")
    st.write(f"**Movement**: {details['movement']}")
    st.write(f"**Points**: {details['points']}")
    st.write(f"**Competitions Played**: {details['competitions_played']}")
    st.write(f"**Country**: {details['country']}")

# Country-Wise Analysis
elif page == "Country-Wise Analysis":
    st.header("Country-Wise Analysis")
    country_stats = df_competitors.groupby('country').agg(
        competitor_count=('competitor_id', 'nunique'),
        avg_points=('points', 'mean')
    ).reset_index().sort_values('competitor_count', ascending=False)
    st.dataframe(country_stats)
    fig_pie = px.pie(country_stats.head(10), values='competitor_count', names='country',
                     title="Top 10 Countries by Number of Competitors")
    st.plotly_chart(fig_pie)
    fig_bar = px.bar(country_stats.head(10), x='country', y='avg_points',
                     title="Average Points by Top 10 Countries")
    st.plotly_chart(fig_bar)

# Leaderboards
elif page == "Leaderboards":
    st.header("Leaderboards")
    st.subheader("Top-Ranked Competitors")
    top_ranked = df_competitors[df_competitors['rank'] <= 10][['name', 'rank', 'points', 'country']].sort_values('rank')
    st.dataframe(top_ranked)
    st.subheader("Competitors with Highest Points")
    top_points = df_competitors.nlargest(10, 'points')[['name', 'rank', 'points', 'country']]
    st.dataframe(top_points)
    fig = px.bar(top_points, x='name', y='points', title="Top 10 by Points", text=top_points['rank'])
    st.plotly_chart(fig)

# Competitions Analysis
elif page == "Competitions Analysis":
    st.header("Competitions Analysis")
    types = st.multiselect("Competition Type", options=df_competitions['type'].unique(), default=[])
    genders = st.multiselect("Gender", options=df_competitions['gender'].unique(), default=[])
    categories = st.multiselect("Category", options=df_competitions['category_name'].unique(), default=[])
    filtered_competitions = df_competitions
    if types:
        filtered_competitions = filtered_competitions[filtered_competitions['type'].isin(types)]
    if genders:
        filtered_competitions = filtered_competitions[filtered_competitions['gender'].isin(genders)]
    if categories:
        filtered_competitions = filtered_competitions[filtered_competitions['category_name'].isin(categories)]
    st.dataframe(filtered_competitions[['competition_name', 'type', 'gender', 'category_name']])
    type_counts = filtered_competitions['type'].value_counts().reset_index()
    type_counts.columns = ['type', 'count']
    fig = px.bar(type_counts, x='type', y='count', title="Competitions by Type")
    st.plotly_chart(fig)

# Venues Map
elif page == "Venues Map":
    st.header("Venues Map")
    venue_counts = df_venues.groupby('country_name').size().reset_index(name='venue_count')
    fig = px.choropleth(venue_counts, locations='country_name', locationmode='country names',
                        color='venue_count', title="Tennis Venues by Country",
                        color_continuous_scale=px.colors.sequential.Plasma)
    st.plotly_chart(fig)
    st.dataframe(df_venues[['venue_name', 'city_name', 'country_name']])

# Styled Footer
st.sidebar.markdown('<div class="sidebar-footer">Built with Streamlit by ArunKumar</div>', unsafe_allow_html=True)
