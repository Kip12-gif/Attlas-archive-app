<div align="center">

# 🗺️ Atlas & Archive
### *A Global Spatial Bucket List & Personal Field Notebook*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Folium](https://img.shields.io/badge/GIS-Folium%2FLeaflet-green?style=for-the-badge&logo=leaflet&logoColor=white)](https://python-visualization.github.io/folium/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

*Explore the world through your ambitions. Pin milestones, track adventures, and journal your life goals on an interactive global canvas.*

[✨ View Live Demo](#-getting-started) • [🚀 Quick Start](#-local-installation)

</div>

---

## 📖 About The Project

**Atlas & Archive** bridges the gap between personal productivity and spatial exploration. Instead of a traditional, static checklist, this application treats your life goals like an explorer's field notebook—attaching coordinates, map pins, and journal reflections to every milestone. 

Whether you are planning to track your next global adventure, document skills you want to master, or visualize your personal growth across continents, Atlas & Archive provides a sleek, minimalist Moleskine-inspired UI designed for dreamers worldwide.

---

## ✨ Key Features

* **🗺️ The Global Atlas (GIS Map View):** Interactive world map powered by `Folium` and `Leaflet`, featuring dynamic status markers (Achieved, In Progress, Planned) with custom pop-up field notes.
* **📖 The Field Notebook:** A searchable, filterable journal interface allowing you to organize goals by category and completion status.
* **✨ Dynamic Dream Pinning:** An intuitive submission form that lets users add custom life goals anywhere on Earth by inputting coordinates, categories, and personal reflections.
* **📊 Progress Analytics:** Built-in `Plotly` data visualizations tracking goal distribution, completion rates, and category breakdowns.
* **🎨 Moleskine Design Aesthetic:** Crafted with custom CSS, warm cream paper tones (`#FDFBF7`), and typography optimized for high readability.

---

## 🛠️ Tech Stack

* **Frontend & Framework:** Streamlit (Python)
* **GIS & Spatial Mapping:** Folium, Leaflet.js, Streamlit-Folium
* **Data Handling & Analytics:** Pandas, Plotly
* **Styling:** Custom CSS / HTML Glassmorphism & Paper Textures

---

## 📁 Repository Structure

```text
atlas-and-archive/
├── .streamlit/
│   └── config.toml      # Theme & configuration settings
├── app.py               # Main application logic & UI
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation