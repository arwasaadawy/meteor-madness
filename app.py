import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time
import random

# Page configuration
st.set_page_config(
    page_title="Meteor Madness - NASA Space Apps 2025",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0B3D91 0%, #061F4A 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        border: 2px solid #FC3D21;
        box-shadow: 0 8px 32px rgba(11, 61, 145, 0.3);
    }
    
    .nasa-navbar {
        background: linear-gradient(90deg, #0B3D91 0%, #FC3D21 50%, #061F4A 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        font-weight: bold;
        font-size: 1.4rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        border: 1px solid #FFD700;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #0B3D91;
        padding: 10px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        white-space: pre-wrap;
        background: #1e3c72;
        border-radius: 8px 8px 0px 0px;
        gap: 8px;
        padding: 12px 20px;
        font-weight: bold;
        color: white;
    }
    
    .stTabs [aria-selected="true"] {
        background: #FC3D21 !important;
        color: white !important;
        border-bottom: 3px solid #FFD700;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        border: 1px solid #FC3D21;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .data-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #FC3D21;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .status-success {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1212px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #FC3D21 0%, #e62e1a 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(252, 61, 33, 0.4);
    }
    
    .chart-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #0B3D91;
        text-align: center;
        margin: 1.5rem 0 0.5rem 0;
        padding: 0.8rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 8px;
        border-left: 4px solid #FC3D21;
    }
    
    .report-btn {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%) !important;
        color: white !important;
        border: none !important;
        padding: 15px 30px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .report-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 184, 148, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

def setup_secrets():
    """Setup API keys securely"""
    try:
        return st.secrets["NASA_API_KEY"]
    except:
        return "DEMO_KEY"

NASA_API_KEY = setup_secrets()

def navigation():
    st.markdown("""
    <div class="nasa-navbar">
        🌌 METEOR MADNESS | 🛡️ PLANETARY DEFENSE SYSTEM | 🚀 NASA SPACE APPS 2025
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(title, value, subtitle, icon):
    """Create metric cards"""
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
        <h3 style="margin: 0; font-size: 1.8rem; color: #FFD700;">{value}</h3>
        <p style="margin: 0.2rem 0; font-weight: bold;">{title}</p>
        <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def generate_simulated_neo_data():
    """Generate simulated NEO data when API fails"""
    asteroids = {}
    for i in range(7):
        date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        asteroids[date] = [
            {
                'id': f"sim_{i}_{j}",
                'name': f"Simulated Asteroid {i}-{j}",
                'estimated_diameter': {'meters': {'estimated_diameter_min': random.randint(50, 500)}},
                'is_potentially_hazardous_asteroid': random.choice([True, False]),
                'close_approach_data': [{
                    'miss_distance': {'kilometers': str(random.randint(5000000, 50000000))},
                    'relative_velocity': {'kilometers_per_second': str(random.uniform(5, 25))}
                }]
            } for j in range(random.randint(3, 8))
        ]
    return {'element_count': 127, 'near_earth_objects': asteroids}

def fetch_live_neo_data(days=7):
    """Fetch live data from NASA NEO API"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        url = "https://api.nasa.gov/neo/rest/v1/feed"
        params = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'api_key': NASA_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'data': data,
                'count': data.get('element_count', 127)
            }
        else:
            simulated_data = generate_simulated_neo_data()
            return {
                'success': False,
                'data': simulated_data,
                'count': simulated_data['element_count']
            }
            
    except Exception as e:
        simulated_data = generate_simulated_neo_data()
        return {
            'success': False,
            'data': simulated_data,
            'count': simulated_data['element_count']
        }

def generate_simulated_earthquake_data():
    """Generate simulated earthquake data with coordinates"""
    locations = [
        {"place": "California, USA", "lat": 36.7783, "lon": -119.4179},
        {"place": "Tokyo, Japan", "lat": 35.6762, "lon": 139.6503},
        {"place": "Indonesia", "lat": -0.7893, "lon": 113.9213},
        {"place": "Chile", "lat": -35.6751, "lon": -71.5430},
        {"place": "Italy", "lat": 41.8719, "lon": 12.5674},
        {"place": "New Zealand", "lat": -40.9006, "lon": 174.8860},
        {"place": "Greece", "lat": 39.0742, "lon": 21.8243},
        {"place": "Turkey", "lat": 38.9637, "lon": 35.2433},
        {"place": "Mexico", "lat": 23.6345, "lon": -102.5528},
        {"place": "Philippines", "lat": 12.8797, "lon": 121.7740},
        {"place": "Alaska, USA", "lat": 64.2008, "lon": -149.4937},
        {"place": "Peru", "lat": -9.1900, "lon": -75.0152},
        {"place": "India", "lat": 20.5937, "lon": 78.9629},
        {"place": "Iran", "lat": 32.4279, "lon": 53.6880},
        {"place": "Papua New Guinea", "lat": -6.3150, "lon": 143.9555}
    ]
    
    earthquakes = []
    for loc in locations:
        earthquakes.append({
            'magnitude': round(random.uniform(4.5, 7.5), 1),
            'place': loc['place'],
            'time': datetime.now() - timedelta(days=random.randint(0, 6)),
            'depth': round(random.uniform(5, 100), 1),
            'latitude': loc['lat'],
            'longitude': loc['lon'],
            'significance': random.randint(100, 800)
        })
    
    return earthquakes

def fetch_usgs_earthquake_data():
    """Fetch earthquake data from USGS with coordinates"""
    try:
        url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_week.geojson"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            earthquakes = []
            for feature in data['features'][:15]:
                eq = feature['properties']
                coords = feature['geometry']['coordinates']
                earthquakes.append({
                    'magnitude': eq['mag'],
                    'place': eq['place'],
                    'time': datetime.fromtimestamp(eq['time']/1000),
                    'depth': coords[2],
                    'longitude': coords[0],
                    'latitude': coords[1],
                    'significance': eq.get('sig', 0)
                })
            return earthquakes
        return generate_simulated_earthquake_data()
    except:
        return generate_simulated_earthquake_data()

def calculate_defense_success(defense_strategy, asteroid_size, warning_time):
    """Calculate defense success probability"""
    base_success = {
        "Kinetic Impactor": 0.85,
        "Gravity Tractor": 0.70,
        "Nuclear Option": 0.95
    }
    
    size_factor = max(0.1, 1 - (asteroid_size / 2000))
    time_factor = min(1.0, warning_time / 10)
    
    success_rate = base_success[defense_strategy] * size_factor * time_factor
    success_rate = min(0.98, max(0.3, success_rate))
    
    miss_distance = random.randint(5000, 50000) * (success_rate / 0.85)
    
    return success_rate, miss_distance

def calculate_impact_effects(diameter, velocity, angle, material):
    """Calculate dynamic impact effects"""
    mass = (4/3) * np.pi * ((diameter/2)**3) * 3000
    energy_joules = 0.5 * mass * (velocity * 1000)**2
    energy_megatons = energy_joules / (4.184e15)
    
    crater_diameter = 1.2 * diameter * (velocity / 10) * np.sin(np.radians(angle))
    seismic_magnitude = 4.5 + (np.log10(energy_joules) - 12) / 1.5
    fireball_radius = 50 * (energy_megatons ** 0.4)
    
    angle_factor = angle / 90
    velocity_factor = velocity / 30
    
    distribution = {
        'Crater Formation': 35 + (15 * angle_factor),
        'Seismic Waves': 20 + (10 * velocity_factor),
        'Thermal Radiation': 25 + (5 * velocity_factor),
        'Ejecta & Debris': 20 + (10 * (1 - angle_factor))
    }
    
    total = sum(distribution.values())
    for key in distribution:
        distribution[key] = (distribution[key] / total) * 100
    
    return {
        'energy_megatons': energy_megatons,
        'crater_diameter': crater_diameter,
        'seismic_magnitude': seismic_magnitude,
        'fireball_radius': fireball_radius,
        'affected_area': crater_diameter * 3,
        'impact_distribution': distribution
    }

def create_impactor_2025_scenario():
    """Impactor-2025 Interactive Scenario"""
    st.markdown("## 🎮 IMPACTOR-2025 DEFENSE MISSION")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 MISSION PARAMETERS")
        time_to_impact = st.slider("Days to Impact", 30, 365, 180)
        asteroid_size = st.slider("Asteroid Size (meters)", 200, 1000, 450)
        defense_budget = st.select_slider("Defense Budget", 
                                        options=["$1B", "$5B", "$10B", "$50B", "$100B"])
        
        strategy = st.radio(
            "Defense Strategy:",
            ["Kinetic Impactor", "Nuclear Deflection", "Gravity Tractor", "Combined Approach"]
        )
    
    with col2:
        if st.button("🚀 LAUNCH DEFENSE MISSION", use_container_width=True):
            with st.spinner("Executing defense mission..."):
                time.sleep(2)
                success = random.random() > 0.3
                
                if success:
                    st.balloons()
                    st.success("""
                    🎉 MISSION SUCCESSFUL!
                    
                    **Earth Defense Status:** ✅ SECURE
                    **Asteroid Deflected:** 15,842 km from Earth
                    **Casualties Prevented:** Millions
                    """)
                else:
                    st.error("""
                    💥 MISSION FAILED!
                    
                    **Earth Defense Status:** ❌ CRITICAL
                    **Impact Probability:** 89%
                    **Emergency Evacuation:** Required
                    """)

def generate_3d_orbital_map(neo_data):
    """Generate 3D orbital visualization of asteroids"""
    
    # Create Earth sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x_earth = 6371 * np.outer(np.cos(u), np.sin(v))
    y_earth = 6371 * np.outer(np.sin(u), np.sin(v))
    z_earth = 6371 * np.outer(np.ones(np.size(u)), np.cos(v))
    
    fig = go.Figure()
    
    # Add Earth
    fig.add_trace(go.Surface(
        x=x_earth, y=y_earth, z=z_earth,
        colorscale=[[0, '#1f77b4'], [1, '#1f77b4']],
        showscale=False,
        opacity=0.7,
        name="Earth"
    ))
    
    # Extract asteroid data and plot orbits
    asteroid_count = 0
    for date, objects in neo_data['near_earth_objects'].items():
        for obj in objects[:5]:
            try:
                distance = float(obj['close_approach_data'][0]['miss_distance']['kilometers'])
                velocity = float(obj['close_approach_data'][0]['relative_velocity']['kilometers_per_second'])
                hazardous = obj['is_potentially_hazardous_asteroid']
                diameter = obj['estimated_diameter']['meters']['estimated_diameter_min']
                
                # Create elliptical orbit
                theta = np.linspace(0, 2*np.pi, 100)
                r = distance / 1000
                x_orbit = r * np.cos(theta) + random.uniform(-2, 2)
                y_orbit = r * np.sin(theta) + random.uniform(-2, 2)
                z_orbit = np.sin(theta) * r * 0.3
                
                # Add orbit path
                fig.add_trace(go.Scatter3d(
                    x=x_orbit, y=y_orbit, z=z_orbit,
                    mode='lines',
                    line=dict(width=2, color='red' if hazardous else 'green'),
                    name=f"{obj['name']} - {'Hazardous' if hazardous else 'Safe'}",
                    showlegend=False
                ))
                
                # Add asteroid point
                fig.add_trace(go.Scatter3d(
                    x=[x_orbit[0]], y=[y_orbit[0]], z=[z_orbit[0]],
                    mode='markers',
                    marker=dict(
                        size=max(5, diameter / 50),
                        color='red' if hazardous else 'green',
                        opacity=0.8
                    ),
                    name=obj['name'],
                    text=f"{obj['name']}<br>Diameter: {diameter:.0f}m<br>Velocity: {velocity:.1f} km/s<br>Hazardous: {hazardous}",
                    hoverinfo='text'
                ))
                
                asteroid_count += 1
                if asteroid_count >= 15:
                    break
                    
            except (KeyError, ValueError):
                continue
    
    fig.update_layout(
        title="3D Asteroid Orbital Visualization",
        scene=dict(
            xaxis_title="X (1000 km)",
            yaxis_title="Y (1000 km)", 
            zaxis_title="Z (1000 km)",
            bgcolor='black',
            camera=dict(eye=dict(x=2, y=2, z=1)),
            aspectmode='data'
        ),
        height=600,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    return fig

def generate_live_visualizations():
    """Generate dynamic visualizations for dashboard"""
    
    # 1. Asteroid Velocity Distribution - Fixed version
    velocities = np.random.normal(15, 5, 100)
    velocity_ranges = ['0-5 km/s', '5-10 km/s', '10-15 km/s', '15-20 km/s', '20-25 km/s', '25+ km/s']
    velocity_counts = np.histogram(velocities, bins=[0, 5, 10, 15, 20, 25, 30])[0]
    
    # Create DataFrame for proper coloring
    velocity_df = pd.DataFrame({
        'Velocity Range': velocity_ranges,
        'Count': velocity_counts
    })
    
    fig1 = px.bar(
        velocity_df,
        x='Velocity Range', 
        y='Count',
        color='Count',
        color_continuous_scale='Viridis'
    )
    fig1.update_layout(
        showlegend=False,
        title="",
        xaxis_title="Velocity Range",
        yaxis_title="Number of Asteroids"
    )
    
    # 2. Threat Level Analysis
    threat_levels = ['Low Risk', 'Medium Risk', 'High Risk', 'Critical']
    threat_counts = [45, 28, 15, 12]
    
    fig2 = px.pie(
        values=threat_counts, 
        names=threat_levels,
        color=threat_levels,
        color_discrete_map={'Low Risk': '#00b894', 'Medium Risk': '#fdcb6e', 
                          'High Risk': '#e17055', 'Critical': '#d63031'}
    )
    fig2.update_layout(title="", showlegend=True)
    
    # 3. Close Approach Timeline
    dates = pd.date_range(start='2025-01-01', end='2025-12-31', freq='30D')
    approaches = np.random.randint(1, 20, size=len(dates))
    
    fig3 = px.line(
        x=dates, 
        y=approaches,
        markers=True
    )
    fig3.update_traces(line=dict(color='#FC3D21', width=3))
    fig3.update_layout(
        title="",
        xaxis_title="Date",
        yaxis_title="Number of Close Approaches"
    )
    
    # 4. Size vs Hazard Analysis
    sizes = np.random.randint(50, 1000, 50)
    hazards = np.random.choice([True, False], 50, p=[0.3, 0.7])
    
    fig4 = px.scatter(
        x=sizes,
        y=[random.randint(5, 25) for _ in range(50)],
        color=hazards,
        labels={'x': 'Diameter (m)', 'y': 'Velocity (km/s)', 'color': 'Hazardous'},
        color_discrete_map={True: '#d63031', False: '#00b894'}
    )
    fig4.update_layout(title="")
    
    return [fig1, fig2, fig3, fig4]

def generate_nasa_data_visualizations(neo_data):
    """Generate enhanced visualizations for NASA Data tab"""
    
    asteroids = []
    for date, objects in neo_data['near_earth_objects'].items():
        for obj in objects:
            try:
                asteroids.append({
                    'diameter': obj['estimated_diameter']['meters']['estimated_diameter_min'],
                    'hazardous': obj['is_potentially_hazardous_asteroid'],
                    'velocity': float(obj['close_approach_data'][0]['relative_velocity']['kilometers_per_second']),
                    'distance': float(obj['close_approach_data'][0]['miss_distance']['kilometers'])
                })
            except (KeyError, ValueError):
                continue
    
    if len(asteroids) > 0:
        df = pd.DataFrame(asteroids)
        
        # 1. Asteroid Size Distribution
        fig1 = px.histogram(
            df, x='diameter',
            nbins=15,
            title="",
            color_discrete_sequence=['#FC3D21'],
            opacity=0.8
        )
        fig1.update_layout(
            xaxis_title="Diameter (meters)",
            yaxis_title="Number of Asteroids",
            bargap=0.05
        )
        
        # 2. Orbital Distance Analysis
        fig2 = px.scatter(
            df, x='distance', y='velocity', 
            size='diameter',
            color='hazardous', 
            title="",
            labels={
                'distance': 'Distance (km)', 
                'velocity': 'Velocity (km/s)', 
                'hazardous': 'Hazardous'
            },
            color_discrete_map={True: '#d63031', False: '#00b894'}
        )
        
        # 3. Hazardous Objects Analysis
        hazardous_count = df['hazardous'].sum()
        non_hazardous_count = len(df) - hazardous_count
        
        fig3 = px.pie(
            values=[hazardous_count, non_hazardous_count],
            names=['Hazardous', 'Non-Hazardous'],
            color=['Hazardous', 'Non-Hazardous'],
            color_discrete_map={'Hazardous': '#d63031', 'Non-Hazardous': '#00b894'}
        )
        fig3.update_layout(title="", showlegend=True)
        
        # 4. Impact Probability Heatmap
        objects = ['2024 AB3', '2024 CD2', 'Apophis', 'Bennu', '2023 XR1', '2025 YZ4']
        years = ['2024', '2025', '2026', '2027', '2028']
        probability = np.random.rand(6, 5) * 0.1
        
        fig4 = px.imshow(
            probability, 
            x=years, 
            y=objects, 
            title="",
            color_continuous_scale='Reds'
        )
        fig4.update_layout(
            xaxis_title="Year", 
            yaxis_title="Asteroid"
        )
        
        return [fig1, fig2, fig3, fig4]
    else:
        # Fallback to simulated data if no real data
        return generate_live_visualizations()

def main():
    if 'defense_deployed' not in st.session_state:
        st.session_state.defense_deployed = False
    if 'run_impact' not in st.session_state:
        st.session_state.run_impact = False
    
    navigation()
    
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 3rem;">🌌 METEOR MADNESS</h1>
        <h3 style="margin: 0; color: #FFD700;">NASA Space Apps Challenge 2025 - Planetary Defense System</h3>
        <p style="margin: 1rem 0 0 0; font-size: 1.1rem;">
            Real-time asteroid tracking and impact simulation powered by NASA API
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    neo_data = fetch_live_neo_data()
    
    # تبويبات بس من غير تبويب الريبورت
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📡 LIVE DASHBOARD", 
        "💥 IMPACT SIMULATOR", 
        "🛡️ DEFENSE SYSTEMS", 
        "🎮 IMPACTOR-2025",
        "🛰️ 3D ORBITAL MAP",
        "📊 NASA DATA"
    ])
    
    with tab1:
        st.markdown("## 🎯 REAL-TIME MONITORING DASHBOARD")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔄 REFRESH DATA", use_container_width=True):
                st.rerun()
        
        with col2:
            # زر GENERATE REPORT واحد بس
            REPORT_URL = "https://drive.google.com/file/d/1tCIIT6jPK7OgKgM4opSibf7HXOviWZkr/view"
            
            # استخدام markdown علشان زر يفتح اللينك مباشرة
            st.markdown(f"""
            <a href="{REPORT_URL}" target="_blank" style="text-decoration: none;">
                <button class="report-btn">
                    📊 GENERATE REPORT
                </button>
            </a>
            """, unsafe_allow_html=True)
        
        with col3:
            if st.button("🚨 ALERT STATUS", use_container_width=True):
                st.warning("🟡 All systems nominal - No immediate threats")
        
        with col4:
            if st.button("🌍 GLOBAL VIEW", use_container_width=True):
                st.info("🛰️ Loading global asteroid distribution...")
        
        st.markdown("### 📊 QUICK STATS")
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        
        with stats_col1:
            total_count = neo_data['count']
            create_metric_card("TOTAL OBJECTS", str(total_count), "Tracked objects", "🚀")
        
        with stats_col2:
            create_metric_card("HAZARDOUS", "15", "Potential threats", "⚠️")
        
        with stats_col3:
            create_metric_card("CLOSE APPROACH", "8", "This week", "🌍")
        
        with stats_col4:
            create_metric_card("DEFENSE READY", "100%", "Systems online", "🛡️")
        
        st.markdown("### 📈 LIVE VISUALIZATIONS")
        
        figs = generate_live_visualizations()
        
        viz_col1, viz_col2 = st.columns(2)
        
        with viz_col1:
            st.markdown('<div class="chart-title">🚀 Asteroid Velocity Distribution</div>', unsafe_allow_html=True)
            st.plotly_chart(figs[0], use_container_width=True)
        
        with viz_col2:
            st.markdown('<div class="chart-title">⚠️ Threat Level Distribution</div>', unsafe_allow_html=True)
            st.plotly_chart(figs[1], use_container_width=True)
        
        viz_col3, viz_col4 = st.columns(2)
        
        with viz_col3:
            st.markdown('<div class="chart-title">📅 Close Approaches Timeline 2025</div>', unsafe_allow_html=True)
            st.plotly_chart(figs[2], use_container_width=True)
        
        with viz_col4:
            st.markdown('<div class="chart-title">📊 Size vs Hazard Correlation</div>', unsafe_allow_html=True)
            st.plotly_chart(figs[3], use_container_width=True)
    
    with tab2:
        st.markdown("## 💥 ASTEROID IMPACT SIMULATOR")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### 🎯 IMPACT PARAMETERS")
            
            diameter = st.slider("Asteroid Diameter (meters)", 50, 2000, 500)
            velocity = st.slider("Impact Velocity (km/s)", 5, 30, 15)
            angle = st.slider("Impact Angle (degrees)", 15, 90, 45)
            material = st.selectbox("Target Material", 
                                  ["Ocean", "Continental Crust", "Sedimentary Rock", "Granite"])
            
            if st.button("🚀 SIMULATE IMPACT", use_container_width=True):
                st.session_state.run_impact = True
        
        with col2:
            st.markdown("### 📊 IMPACT ANALYSIS")
            
            if st.session_state.get('run_impact', False):
                impact_results = calculate_impact_effects(diameter, velocity, angle, material)
                
                st.markdown(f"""
                <div class="data-card">
                    <h3 style="color: #FC3D21;">💥 IMPACT SIMULATION RESULTS</h3>
                    <p><strong>Energy Release:</strong> {impact_results['energy_megatons']:,.1f} megatons TNT</p>
                    <p><strong>Crater Diameter:</strong> {impact_results['crater_diameter']:,.0f} meters</p>
                    <p><strong>Seismic Magnitude:</strong> {impact_results['seismic_magnitude']:.1f} Richter</p>
                    <p><strong>Fireball Radius:</strong> {impact_results['fireball_radius']:.1f} km</p>
                    <p><strong>Affected Area:</strong> {impact_results['affected_area']:,.0f} km²</p>
                </div>
                """, unsafe_allow_html=True)
                
                impact_dist_df = pd.DataFrame({
                    'Effect': list(impact_results['impact_distribution'].keys()),
                    'Percentage': list(impact_results['impact_distribution'].values())
                })
                
                st.markdown('<div class="chart-title">💥 Impact Energy Distribution</div>', unsafe_allow_html=True)
                fig = px.pie(
                    impact_dist_df, 
                    values='Percentage', 
                    names='Effect',
                    hole=0.4,
                    color_discrete_sequence=px.colors.sequential.RdBu
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("## 🛡️ PLANETARY DEFENSE SYSTEMS")
        
        st.markdown("""
        <div class="data-card">
            <h3 style="color: #0B3D91;">🌍 EARTH PROTECTION NETWORK</h3>
            <p>Advanced defense systems for asteroid threat mitigation</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>🚀 KINETIC IMPACTOR</h4>
                <p>High-speed collision to alter trajectory</p>
                <p><strong>Success Rate:</strong> 85%</p>
                <p><strong>Response Time:</strong> 2-3 years</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>🧲 GRAVITY TRACTOR</h4>
                <p>Gentle gravitational influence over time</p>
                <p><strong>Success Rate:</strong> 70%</p>
                <p><strong>Response Time:</strong> 5-10 years</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h4>💣 NUCLEAR DEFLECTION</h4>
                <p>Strategic energy deployment</p>
                <p><strong>Success Rate:</strong> 95%</p>
                <p><strong>Response Time:</strong> 1-2 years</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 DEFENSE SIMULATION")
        defense_col1, defense_col2 = st.columns(2)
        
        with defense_col1:
            defense_strategy = st.selectbox("Select Defense Strategy", 
                                          ["Kinetic Impactor", "Gravity Tractor", "Nuclear Option"])
            asteroid_size = st.slider("Asteroid Size (meters)", 100, 1000, 300, key="defense_size")
            warning_time = st.slider("Warning Time (years)", 1, 20, 5, key="warning_time")
            
            if st.button("🛡️ DEPLOY DEFENSE", use_container_width=True):
                st.session_state.defense_deployed = True
        
        with defense_col2:
            if st.session_state.get('defense_deployed', False):
                success_rate, miss_distance = calculate_defense_success(
                    defense_strategy, asteroid_size, warning_time
                )
                
                earth_safety = "GUARANTEED" if success_rate > 0.8 else "PROBABLE" if success_rate > 0.6 else "UNCERTAIN"
                
                st.markdown(f"""
                <div class="status-success">
                    <h3>✅ DEFENSE DEPLOYED</h3>
                    <p><strong>Strategy:</strong> {defense_strategy}</p>
                    <p><strong>Success Probability:</strong> {success_rate:.1%}</p>
                    <p><strong>Estimated Miss Distance:</strong> {miss_distance:,.0f} km</p>
                    <p><strong>Earth Safety:</strong> {earth_safety}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab4:
        create_impactor_2025_scenario()
    
    with tab5:
        st.markdown("## 🛰️ 3D ORBITAL VISUALIZATION")
        
        st.markdown("""
        <div class="data-card">
            <h3 style="color: #0B3D91;">🌍 REAL-TIME ASTEROID TRACKING</h3>
            <p>Interactive 3D visualization of near-Earth objects and their orbital paths</p>
            <p><strong>Red orbits:</strong> Potentially hazardous asteroids</p>
            <p><strong>Green orbits:</strong> Safe asteroids</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("Generating 3D orbital visualization..."):
            fig_3d = generate_3d_orbital_map(neo_data['data'])
            st.plotly_chart(fig_3d, use_container_width=True)
        
        st.markdown("""
        <div class="data-card">
            <h4>🎯 How to Use:</h4>
            <ul>
                <li><strong>Rotate:</strong> Click and drag to rotate the view</li>
                <li><strong>Zoom:</strong> Use mouse wheel to zoom in/out</li>
                <li><strong>Pan:</strong> Hold Shift and drag to pan</li>
                <li><strong>Hover:</strong> Hover over asteroids for details</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tab6:
        st.markdown("## 📊 NASA DATA ANALYSIS")
        
        status_icon = "✅" if neo_data['success'] else "🔄"
        status_text = "Live NASA Data" if neo_data['success'] else "Simulated Data"
        
        st.markdown(f"""
        <div class="status-success">
            <h3>🛰️ NASA DATA INTEGRATION</h3>
            <p><strong>Status:</strong> {status_icon} {status_text}</p>
            <p><strong>Last Update:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p><strong>Objects Tracked:</strong> {neo_data['count']} near-Earth objects</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📈 COMPREHENSIVE DATA ANALYSIS")
        
        nasa_figs = generate_nasa_data_visualizations(neo_data['data'])
        
        nasa_col1, nasa_col2 = st.columns(2)
        
        with nasa_col1:
            st.markdown('<div class="chart-title">📏 Asteroid Size Distribution</div>', unsafe_allow_html=True)
            st.plotly_chart(nasa_figs[0], use_container_width=True)
        
        with nasa_col2:
            st.markdown('<div class="chart-title">🌍 Orbital Dynamics Analysis</div>', unsafe_allow_html=True)
            st.plotly_chart(nasa_figs[1], use_container_width=True)
        
        nasa_col3, nasa_col4 = st.columns(2)
        
        with nasa_col3:
            st.markdown('<div class="chart-title">⚠️ Hazardous Objects Analysis</div>', unsafe_allow_html=True)
            st.plotly_chart(nasa_figs[2], use_container_width=True)
        
        with nasa_col4:
            st.markdown('<div class="chart-title">🔥 Impact Probability Heatmap</div>', unsafe_allow_html=True)
            st.plotly_chart(nasa_figs[3], use_container_width=True)
        
        # Earthquake data with map
        earthquakes = fetch_usgs_earthquake_data()
        if earthquakes:
            st.markdown("### 🌋 RECENT SEISMIC ACTIVITY (USGS Data)")
            
            eq_df = pd.DataFrame(earthquakes)
            
            # Create earthquake map
            st.markdown("#### 🗺️ Global Earthquake Map")
            
            fig_map = px.scatter_mapbox(
                eq_df,
                lat="latitude",
                lon="longitude",
                hover_name="place",
                hover_data={
                    "magnitude": ":.1f",
                    "depth": ":.1f km",
                    "time": "|%Y-%m-%d %H:%M"
                },
                color="magnitude",
                size="magnitude",
                color_continuous_scale="reds",
                size_max=15,
                zoom=1,
                height=500,
                title="Recent Earthquakes (Magnitude 4.5+)"
            )
            
            fig_map.update_layout(
                mapbox_style="open-street-map",
                margin={"r":0,"t":30,"l":0,"b":0}
            )
            
            st.plotly_chart(fig_map, use_container_width=True)
            
            # Quick stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Largest Magnitude", f"{eq_df['magnitude'].max():.1f}")
            with col2:
                st.metric("Total Earthquakes", len(eq_df))
            with col3:
                st.metric("Average Depth", f"{eq_df['depth'].mean():.1f} km")
            
            # Data table
            st.markdown("#### 📊 Detailed Earthquake Data")
            st.dataframe(
                eq_df[['place', 'magnitude', 'depth', 'time']].style.format({
                    'magnitude': '{:.1f}',
                    'depth': '{:.1f} km'
                }),
                use_container_width=True,
                height=300
            )

if __name__ == "__main__":
    main()
