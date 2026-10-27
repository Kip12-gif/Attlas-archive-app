import folium
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Atlas & Archive | Vintage Field Notebook & GIS Atlas",
    page_icon="📓",
    layout="wide",
)

# ==============================================================================
# 📜 VINTAGE PARCHMENT NOTEBOOK & KEYLESS GIS THEME (CSS)
# ==============================================================================
custom_css = """
<style>
/* Authentic Aged Parchment Texture with Subtle Grid */
.stApp {
    background-color: #F4EEDC;
    background-image: radial-gradient(#E3D6B8 0.75px, transparent 0.75px), 
                      radial-gradient(#E3D6B8 0.75px, #F4EEDC 0.75px);
    background-size: 30px 30px;
    background-position: 0 0, 15px 15px;
}

/* Antique Sepia & Leather Typography */
html, body, [class*="css"], .stMarkdown, p, span, label, h1, h2, h3, h4, h5, h6 {
    color: #2D231B !important;
    font-family: 'Georgia', serif;
}

/* Notebook Header styling with antique underline */
h1, h2, h3 {
    font-family: 'Georgia', serif;
    font-weight: 700;
    border-bottom: 2px solid #C4B495;
    padding-bottom: 8px;
    color: #4A3525 !important;
}

/* Paper Journal Cards */
div[data-testid="stBlock"] {
    background-color: #FCF9F2 !important;
    border-radius: 4px;
    border: 1px solid #C4B495;
    box-shadow: 3px 5px 15px rgba(45, 35, 27, 0.08);
    padding: 1.2rem;
}

/* Deep Leather Brown Accent Buttons */
div.stButton > button {
    background-color: #5C3A21 !important;
    color: #F4EEDC !important;
    border-radius: 4px !important;
    border: 1px solid #3B2414 !important;
    font-family: 'Georgia', serif;
    font-weight: 600;
}
div.stButton > button:hover {
    background-color: #432A17 !important;
}

/* Custom Metrics */
[data-testid="stMetricValue"] {
    color: #5C3A21 !important;
    font-weight: 700 !important;
}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
}
.stTabs [data-baseweb="tab"] {
    background-color: #E8DECA !important;
    border-radius: 4px 4px 0px 0px;
    border: 1px solid #C4B495;
    padding: 10px 16px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==============================================================================
# 📍 INITIALIZE GLOBAL DEMO DATA IN SESSION STATE
# ==============================================================================
if "bucket_list" not in st.session_state:
  st.session_state.bucket_list = [
      {
          "id": 1,
          "title": "Watch the Northern Lights",
          "location": "Tromsø, Norway",
          "lat": 69.6492,
          "lon": 18.9553,
          "category": "Nature & Wildlife",
          "status": "Planned",
          "notes": (
              "Rent a cabin in Arctic Norway, setup tripod, and capture the"
              " aurora borealis peak season."
          ),
      },
      {
          "id": 2,
          "title": "Hike the Inca Trail to Machu Picchu",
          "location": "Cusco, Peru",
          "lat": -13.1631,
          "lon": -72.5450,
          "category": "Adventure",
          "status": "Achieved",
          "notes": (
              "Completed the 4-day trek. Altitude sickness was tough near Dead"
              " Woman's Pass, but the sunrise at Sun Gate was life-changing."
          ),
      },
      {
          "id": 3,
          "title": "Learn Traditional Pottery & Tea Ceremony",
          "location": "Kyoto, Japan",
          "lat": 35.0116,
          "lon": 135.7681,
          "category": "Culture & Art",
          "status": "In Progress",
          "notes": (
              "Studying wabi-sabi principles and practicing wheel throwing in"
              " the Higashiyama district."
          ),
      },
      {
          "id": 4,
          "title": "Surf the Uluwatu Breaks",
          "location": "Bali, Indonesia",
          "lat": -8.8149,
          "lon": 115.0884,
          "category": "Skill & Sport",
          "status": "In Progress",
          "notes": (
              "Catching left-hand reef breaks during dry season. Working on"
              " duck-diving consistency."
          ),
      },
      {
          "id": 5,
          "title": "Summit Mount Kilimanjaro",
          "location": "Tanzania",
          "lat": -3.0674,
          "lon": 37.3556,
          "category": "Adventure",
          "status": "Planned",
          "notes": (
              "Machame Route (Whiskey Route). Training cardio and endurance"
              " for the final midnight push to Uhuru Peak."
          ),
      },
      {
          "id": 6,
          "title": "Stargazing at Atacama Desert",
          "location": "San Pedro de Atacama, Chile",
          "lat": -22.9087,
          "lon": -68.1997,
          "category": "Nature & Wildlife",
          "status": "Planned",
          "notes": (
              "One of the driest, clearest skies on Earth. Book a night"
              " astronomical tour with professional telescopes."
          ),
      },
  ]

# ==============================================================================
# 📜 APP HEADER & METRICS
# ==============================================================================
st.title("📓 Atlas & Archive")
st.markdown(
    "*A spatial bucket list and personal field notebook for global explorers.*"
)

# Calculate metrics
df = pd.DataFrame(st.session_state.bucket_list)
total_goals = len(df)
achieved = len(df[df["status"] == "Achieved"])
in_progress = len(df[df["status"] == "In Progress"])
planned = len(df[df["status"] == "Planned"])

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Total Milestones", value=total_goals)
col2.metric(
    label="Archived (Achieved)",
    value=achieved,
    delta=f"{int(achieved/total_goals*100)}% Complete"
    if total_goals > 0
    else "0%",
)
col3.metric(label="In Progress", value=in_progress)
col4.metric(label="Planned Expeditions", value=planned)

st.divider()

# ==============================================================================
# 📑 TABS: ATLAS (GIS MAP) vs. FIELD NOTES (NOTEBOOK) vs. ADD NEW DREAM
# ==============================================================================
tab_map, tab_notes, tab_add, tab_analytics = st.tabs([
    "🗺️ The Global Atlas (GIS)",
    "📖 Field Journal",
    "✨ New Expedition Entry",
    "📊 Expedition Analytics",
])

with tab_map:
  st.markdown("### Cartographic Field Atlas")
  st.caption(
      "Switch between OpenStreetMap and Google Satellite layers using the map"
      " control in the top-right corner."
  )

  # Initialize map with OpenStreetMap as default
  m = folium.Map(
      location=[20.0, 0.0],
      zoom_start=2,
      tiles="OpenStreetMap",
      name="OpenStreetMap",
  )

  # Add keyless Google Satellite layer option
  folium.TileLayer(
      tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
      attr="Google Satellite",
      name="Google Satellite",
      max_zoom=20,
  ).add_to(m)

  color_map = {
      "Achieved": "darkgreen",
      "In Progress": "orange",
      "Planned": "cadetblue",
  }

  for item in st.session_state.bucket_list:
    marker_color = color_map.get(item["status"], "gray")
    popup_html = f"""
        <div style="font-family: Georgia, serif; width: 220px; color: #2D231B;">
            <h4 style="margin:0; color:#5C3A21; border-bottom: 1px solid #C4B495; padding-bottom:4px;">{item['title']}</h4>
            <p style="margin:6px 0 4px 0; font-size:12px;"><b>📍 Location:</b> {item['location']}</p>
            <p style="margin:4px 0; font-size:12px;"><b>🏷️ Category:</b> {item['category']}</p>
            <p style="margin:4px 0; font-size:12px;"><b>📌 Status:</b> {item['status']}</p>
            <hr style="margin:4px 0; border-top: 1px solid #C4B495;">
            <p style="font-size:11px; font-style: italic; color:#555; margin-top:4px;">{item['notes']}</p>
        </div>
        """
    folium.Marker(
        location=[item["lat"], item["lon"]],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=item["title"],
        icon=folium.Icon(color=marker_color, icon="book", prefix="fa"),
    ).add_to(m)

  # Add layer control to switch between OSM and Google Satellite
  folium.LayerControl().add_to(m)

  # Render map in Streamlit
  st_data = st_folium(m, width=1200, height=520)

with tab_notes:
  st.markdown("### 📖 The Field Notebook")
  st.caption("Review your life goals organized like pages in a leather journal.")

  # Filter widgets
  filter_col1, filter_col2 = st.columns(2)
  with filter_col1:
    status_filter = st.selectbox(
        "Filter by Status", ["All", "Achieved", "In Progress", "Planned"]
    )
  with filter_col2:
    category_filter = st.selectbox(
        "Filter by Category",
        ["All"] + list(df["category"].unique()) if not df.empty else ["All"],
    )

  # Apply filters
  filtered_df = df.copy()
  if status_filter != "All":
    filtered_df = filtered_df[filtered_df["status"] == status_filter]
  if category_filter != "All":
    filtered_df = filtered_df[filtered_df["category"] == category_filter]

  # Display as Notebook Entries
  for _, row in filtered_df.iterrows():
    status_emoji = (
        "📜"
        if row["status"] == "Achieved"
        else "⏳"
        if row["status"] == "In Progress"
        else "🧭"
    )
    with st.container():
      col_a, col_b = st.columns([4, 1])
      with col_a:
        st.markdown(
            f"#### {status_emoji} {row['title']} — *{row['location']}*"
        )
        st.markdown(
            f"**Category:** `{row['category']}` &nbsp;|&nbsp; **Status:**"
            f" `{row['status']}`"
        )
        st.info(row["notes"])
      with col_b:
        if st.button("Delete Entry", key=f"del_{row['id']}"):
          st.session_state.bucket_list = [
              x for x in st.session_state.bucket_list if x["id"] != row["id"]
          ]
          st.rerun()
      st.divider()

with tab_add:
  st.markdown("### ✨ Record a New Entry in Your Atlas")
  st.markdown(
      "Pin a new world destination, milestone, or ambition with its"
      " coordinates."
  )

  with st.form("new_bucket_form"):
    new_title = st.text_input(
        "Goal / Milestone Title",
        placeholder="e.g., Sail across the Mediterranean",
    )
    new_location = st.text_input(
        "Location Name", placeholder="e.g., Palma de Mallorca, Spain"
    )

    c1, c2 = st.columns(2)
    with c1:
      new_lat = st.number_input("Latitude", value=39.5696, format="%.4f")
    with c2:
      new_lon = st.number_input("Longitude", value=2.6502, format="%.4f")

    c3, c4 = st.columns(2)
    with c3:
      new_category = st.selectbox(
          "Category",
          [
              "Adventure",
              "Nature & Wildlife",
              "Culture & Art",
              "Skill & Sport",
              "Career & Impact",
          ],
      )
    with c4:
      new_status = st.selectbox("Status", ["Planned", "In Progress", "Achieved"])

    new_notes = st.text_area(
        "Field Notes & Reflections",
        placeholder="What is the motivation? What is the preparation plan?",
    )

    submitted = st.form_submit_button("Seal Entry in Atlas")
    if submitted:
      if new_title and new_location:
        new_id = (
            max([x["id"] for x in st.session_state.bucket_list]) + 1
            if st.session_state.bucket_list
            else 1
        )
        st.session_state.bucket_list.append({
            "id": new_id,
            "title": new_title,
            "location": new_location,
            "lat": new_lat,
            "lon": new_lon,
            "category": new_category,
            "status": new_status,
            "notes": new_notes,
        })
        st.success(f"Successfully recorded '{new_title}' in your field atlas!")
        st.rerun()
      else:
        st.error("Please provide at least a title and location name.")

with tab_analytics:
  st.markdown("### 📊 Expedition & Goal Analytics")
  col_chart1, col_chart2 = st.columns(2)

  with col_chart1:
    fig_status = px.pie(
        df,
        names="status",
        title="Milestones by Status",
        hole=0.4,
        color_discrete_sequence=["#5C3A21", "#8C6239", "#C4B495"],
    )
    fig_status.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Georgia, serif", color="#2D231B"),
    )
    st.plotly_chart(fig_status, use_container_width=True)

  with col_chart2:
    cat_counts = (
        df["category"].value_counts().reset_index()
        if not df.empty
        else pd.DataFrame(columns=["Category", "Count"])
    )
    if not cat_counts.empty:
      cat_counts.columns = ["Category", "Count"]
    fig_cat = px.bar(
        cat_counts,
        x="Category",
        y="Count",
        title="Milestones by Category",
        color="Category",
        color_discrete_sequence=["#5C3A21", "#704214", "#8C6239", "#C4B495"],
    )
    fig_cat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Georgia, serif", color="#2D231B"),
    )
    st.plotly_chart(fig_cat, use_container_width=True)
