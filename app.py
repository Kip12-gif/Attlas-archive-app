import folium
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Atlas & Archive | Global Bucket List & Field Notes",
    page_icon="🗺️",
    layout="wide",
)

# ==============================================================================
# 🎨 NOTEBOOK & LIGHT GIS THEME (CSS)
# ==============================================================================
custom_css = """
<style>
/* Notebook Cream Background */
.stApp {
    background-color: #FDFBF7;
}

/* Typography - Deep Charcoal/Espresso */
html, body, [class*="css"], .stMarkdown, p, span, label, h1, h2, h3, h4, h5, h6 {
    color: #2C221E !important;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* Notebook Header styling */
h1 {
    font-weight: 700;
    letter-spacing: -0.5px;
    border-bottom: 2px solid #E6DFD5;
    padding-bottom: 10px;
}

/* Card Containers styled like paper notes */
div[data-testid="stBlock"] {
    background-color: #FFFFFF !important;
    border-radius: 10px;
    border: 1px solid #E6DFD5;
    box-shadow: 0 2px 8px rgba(44, 34, 30, 0.04);
    padding: 1rem;
}

/* Custom Metrics */
[data-testid="stMetricValue"] {
    color: #8C5830 !important;
    font-weight: 700 !important;
}

/* Buttons */
div.stButton > button {
    background-color: #8C5830 !important;
    color: #FFFFFF !important;
    border-radius: 6px !important;
    border: none !important;
    font-weight: 600 !important;
}
div.stButton > button:hover {
    background-color: #6E4424 !important;
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
# 🧭 APP HEADER & METRICS
# ==============================================================================
st.title("🗺️ Atlas & Archive")
st.markdown(
    "*A spatial bucket list and personal field notebook for dreamers and"
    " explorers worldwide.*"
)

# Calculate metrics
df = pd.DataFrame(st.session_state.bucket_list)
total_goals = len(df)
achieved = len(df[df["status"] == "Achieved"])
in_progress = len(df[df["status"] == "In Progress"])
planned = len(df[df["status"] == "Planned"])

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Total Life Goals", value=total_goals)
col2.metric(label="Achieved", value=achieved, delta=f"{int(achieved/total_goals*100)}% Complete")
col3.metric(label="In Progress", value=in_progress)
col4.metric(label="Planned", value=planned)

st.divider()

# ==============================================================================
# 📑 TABS: ATLAS (GIS MAP) vs. FIELD NOTES (NOTEBOOK) vs. ADD NEW DREAM
# ==============================================================================
tab_map, tab_notes, tab_add, tab_analytics = st.tabs([
    "🗺️ The Global Atlas (GIS)",
    "📖 Field Notebook",
    "✨ Add New Dream",
    "📊 Progress Analytics",
])

with tab_map:
  st.markdown("### Interactive World Atlas of Dreams")
  st.caption(
      "Explore your pinned milestones across continents. Click map markers for"
      " details."
  )

  # Create Folium Map centered nicely
  m = folium.Map(location=[20.0, 0.0], zoom_start=2, tiles="CartoDB positron")

  # Color mapping for statuses
  color_map = {
      "Achieved": "green",
      "In Progress": "orange",
      "Planned": "blue",
  }

  for item in st.session_state.bucket_list:
    marker_color = color_map.get(item["status"], "gray")
    popup_html = f"""
        <div style="font-family: sans-serif; width: 200px;">
            <h4 style="margin:0; color:#8C5830;">{item['title']}</h4>
            <p style="margin:4px 0; font-size:12px;"><b>📍 Location:</b> {item['location']}</p>
            <p style="margin:4px 0; font-size:12px;"><b>🏷️ Category:</b> {item['category']}</p>
            <p style="margin:4px 0; font-size:12px;"><b>📌 Status:</b> {item['status']}</p>
            <hr style="margin:4px 0;">
            <p style="font-size:11px; color:#555;">{item['notes']}</p>
        </div>
        """
    folium.Marker(
        location=[item["lat"], item["lon"]],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=item["title"],
        icon=folium.Icon(color=marker_color, icon="bookmark", prefix="fa"),
    ).add_to(m)

  # Render map in Streamlit
  st_data = st_folium(m, width=1200, height=500)

with tab_notes:
  st.markdown("### 📖 The Field Notebook")
  st.caption(
      "Browse and filter your bucket list items like pages in a journal."
  )

  # Filter widgets
  filter_col1, filter_col2 = st.columns(2)
  with filter_col1:
    status_filter = st.selectbox(
        "Filter by Status", ["All", "Achieved", "In Progress", "Planned"]
    )
  with filter_col2:
    category_filter = st.selectbox(
        "Filter by Category",
        ["All"] + list(df["category"].unique()),
    )

  # Apply filters
  filtered_df = df.copy()
  if status_filter != "All":
    filtered_df = filtered_df[filtered_df["status"] == status_filter]
  if category_filter != "All":
    filtered_df = filtered_df[filtered_df["category"] == category_filter]

  # Display as Moleskine notebook cards
  for _, row in filtered_df.iterrows():
    status_emoji = (
        "✅"
        if row["status"] == "Achieved"
        else "⏳"
        if row["status"] == "In Progress"
        else "🎯"
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
        if st.button("Delete", key=f"del_{row['id']}"):
          st.session_state.bucket_list = [
              x for x in st.session_state.bucket_list if x["id"] != row["id"]
          ]
          st.rerun()
      st.divider()

with tab_add:
  st.markdown("### ✨ Pin a New Life Goal or Adventure")
  st.markdown(
      "Add a new destination, skill, or milestone with its geographic"
      " coordinates."
  )

  with st.form("new_bucket_form"):
    new_title = st.text_input(
        "Goal Title", placeholder="e.g., Scuba dive the Great Barrier Reef"
    )
    new_location = st.text_input(
        "Location Name", placeholder="e.g., Cairns, Australia"
    )

    c1, c2 = st.columns(2)
    with c1:
      new_lat = st.number_input(
          "Latitude", value=-16.9186, format="%.4f"
      )  # Default Cairns
    with c2:
      new_lon = st.number_input(
          "Longitude", value=145.7781, format="%.4f"
      )

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
        placeholder="Why do you want to do this? What is the plan?",
    )

    submitted = st.form_submit_button("Pin to Atlas")
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
        st.success(
            f"Successfully pinned '{new_title}' to your global atlas!"
        )
        st.rerun()
      else:
        st.error("Please provide at least a title and location name.")

with tab_analytics:
  st.markdown("### 📊 Dream Distribution Analytics")
  col_chart1, col_chart2 = st.columns(2)

  with col_chart1:
    fig_status = px.pie(
        df,
        names="status",
        title="Goals by Completion Status",
        hole=0.4,
        color_discrete_sequence=["#8C5830", "#D9A98F", "#4A3525"],
    )
    fig_status.update_layout(paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_status, use_container_width=True)

  with col_chart2:
    cat_counts = df["category"].value_counts().reset_index()
    cat_counts.columns = ["Category", "Count"]
    fig_cat = px.bar(
        cat_counts,
        x="Category",
        y="Count",
        title="Goals by Category",
        color="Category",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig_cat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_cat, use_container_width=True)