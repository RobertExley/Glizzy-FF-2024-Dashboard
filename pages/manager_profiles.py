import streamlit as st
from renderer.manager_profile import ManagerProfile

st.set_page_config(
    page_title="Manager Profiles",
    page_icon="👤",
    layout="wide",
)

def render_title_card(title, emoji, manager_name, record):
    html_content = f'''
        <div class="title-card">
            <div class="title-header">
                <span class="title-emoji">{emoji}</span>
                <span class="title-text">{title}</span>
            </div>
            <div class="manager-info">
                <span class="manager-name">{manager_name}</span>
                <span class="manager-record">({record})</span>
            </div>
        </div>
    '''
    st.markdown(html_content, unsafe_allow_html=True)

def format_profile_content(content, manager_name):
    sections = content.split('\n\n')
    title_section = sections[0].split('\n')[0]  # Get the title line
    
    formatted_content = f'''
    <div class="profile-content">
        <div class="profile-section-title">{manager_name}'s Season Analysis</div>
        <div class="profile-header">
            {title_section}
        </div>
    '''
    
    # Process each paragraph with statistical highlighting
    for section in sections[1:]:
        if section.strip():
            highlighted_text = section
            import re
            number_pattern = r'(\d+\.?\d*)'
            highlighted_text = re.sub(number_pattern, r'<span class="stat-highlight">\1</span>', highlighted_text)
            
            formatted_content += f'<div class="profile-paragraph">{highlighted_text}</div>'
    
    formatted_content += '</div>'
    return formatted_content

# Initialize session state check
if not st.session_state.get('data_loaded', False):
    st.warning("Please visit the Home page first to load the data.")
    st.stop()

# Retrieve session state data
calculator = st.session_state.calculator
usernames = st.session_state.usernames

st.title('Manager Profiles')

# Title Cards Section
st.markdown("### League Titles")
col1, col2 = st.columns(2)

with col1:
    render_title_card(
        "League Fraud",
        "💩",
        "gautamm",
        "10-4"
    )

with col2:
    render_title_card(
        "League Robbed",
        "😭",
        "hooghost",
        "8-6"
    )

# Apply CSS styling
st.markdown('''
<style>
.title-card {
    background-color: rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
    border: 1px solid rgba(255, 255, 255, 0.1);
    text-align: center;
}

.title-header {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 10px;
}

.title-emoji {
    font-size: 24px;
    margin-right: 10px;
}

.title-text {
    font-size: 20px;
    font-weight: bold;
    color: white;
}

.manager-info {
    margin-bottom: 15px;
}

.manager-name {
    font-size: 18px;
    color: #64B5F6;
}

.manager-record {
    margin-left: 10px;
    color: rgba(255, 255, 255, 0.7);
}

.profile-content {
    font-size: 18px;
    line-height: 2;
    padding: 40px;
    background-color: rgba(0, 0, 0, 0.15);
    margin: 30px 0;
    border-left: 4px solid #64B5F6;
}

.profile-section-title {
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 30px;
    color: #64B5F6;
    border-bottom: 2px solid rgba(100, 181, 246, 0.3);
    padding-bottom: 15px;
}

.profile-header {
    display: flex;
    align-items: center;
    margin-bottom: 30px;
    padding: 15px;
    background: linear-gradient(90deg, rgba(100,181,246,0.1) 0%, rgba(0,0,0,0) 100%);
}

.profile-paragraph {
    margin-bottom: 30px;
    color: rgba(255, 255, 255, 0.9);
    font-size: 20px;
    padding-left: 20px;
    position: relative;
}

.profile-paragraph::before {
    content: '';
    position: absolute;
    left: 0;
    width: 4px;
    height: 100%;
    background: linear-gradient(180deg, rgba(100,181,246,0.3) 0%, rgba(100,181,246,0) 100%);
    border-radius: 2px;
}

.stat-highlight {
    color: #64B5F6;
    font-weight: bold;
}

/* Timeline Chart Styling */
.js-plotly-plot .plotly .modebar {
    display: none !important;
}

.js-plotly-plot {
    margin-bottom: 2rem;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 8px;
    padding: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.js-plotly-plot:hover {
    border-color: rgba(255, 255, 255, 0.2);
}
</style>
''', unsafe_allow_html=True)

# Detailed Analysis Section
st.markdown("### Detailed Manager Analysis")
selected_manager = st.selectbox(
    "Select a manager to view their detailed profile",
    ["gautamm", "hooghost"],
    key="detailed_analysis"
)

try:
    with open(f"profiles/{selected_manager}.txt", "r") as file:
        profile_content = file.read()
    
    # Add visual separator
    st.markdown("""
        <div style="height: 2px; background: linear-gradient(90deg, rgba(100,181,246,0.2) 0%, rgba(100,181,246,0.8) 50%, rgba(100,181,246,0.2) 100%); margin: 30px 0;"></div>
    """, unsafe_allow_html=True)
    
    # Initialize and render profile with timeline
    profile = ManagerProfile(calculator)
    profile.render_profile(selected_manager)
    
    # Display formatted text content
    st.markdown(format_profile_content(profile_content, selected_manager), unsafe_allow_html=True)
    
except FileNotFoundError:
    st.error(f"Profile data for {selected_manager} not found.")