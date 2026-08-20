import plotly.express as px
import numpy as np
import pandas as pd


df = pd.read_csv('jobs_plotly.csv')
df = df.sort_values(by='Start')



fig = px.timeline(df, x_start="Start", 
                  x_end="Finish", y="Experience", color="Type",
                  template='plotly_white',)
fig.show()

fig.write_html('cv.html')

import plotly.express as px
fig2 = px.scatter_geo(df, locations="iso_alpha", 
                     #color="Type",
                     hover_name="country", #size="pop",
                     projection="natural earth", 
                     scope='world', 
                     text='Experience', animation_frame='Start',
                     )
fig2.update_traces(textposition='top center')
fig2.show()

fig2.update_geos(
    lonaxis_range=[-20, 65],
    lataxis_range=[35, 71],
    #projection_type="mercator",  # optional projection choice
)

fig2.write_html('cv_map.html')

###
from pathlib import Path
import base64


def html_to_data_uri(filename):
    html_bytes = Path(filename).read_bytes()

    encoded = base64.b64encode(html_bytes).decode("ascii")

    return f"data:text/html;base64,{encoded}"


# Your existing standalone Plotly HTML files
timeline_uri = html_to_data_uri("cv.html")
map_uri = html_to_data_uri("cv_map.html")


combined_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">

<title>Interactive visualization</title>

<style>

body {{
    font-family: Arial, sans-serif;
    max-width: 1200px;
    margin: 30px auto;
    padding: 0 20px;
}}

.tabs {{
    display: flex;
    gap: 6px;
    margin-bottom: 15px;
}}

.tab {{
    border: 1px solid #ccc;
    background: white;
    padding: 8px 18px;
    cursor: pointer;
    border-radius: 4px;
    font-size: 14px;
}}

.tab:hover {{
    background: #f2f2f2;
}}

.tab.active {{
    background: #555;
    color: white;
    border-color: #555;
}}

.view {{
    display: none;
    width: 100%;
}}

.view.active {{
    display: block;
}}

iframe {{
    width: 100%;
    height: 750px;
    border: none;
}}

</style>
</head>


<body>


<div class="tabs">

    <button
        class="tab active"
        data-target="timeline">
        Timeline
    </button>

    <button
        class="tab"
        data-target="map">
        Map
    </button>

</div>


<div
    id="timeline"
    class="view active">

    <iframe
        src="{timeline_uri}"
        title="Timeline">
    </iframe>

</div>


<div
    id="map"
    class="view">

    <iframe
        src="{map_uri}"
        title="Map">
    </iframe>

</div>


<script>

const buttons = document.querySelectorAll(".tab");
const views = document.querySelectorAll(".view");


buttons.forEach(button => {{

    button.addEventListener("click", () => {{

        const target = button.dataset.target;


        // Hide all views
        views.forEach(view => {{
            view.classList.remove("active");
        }});


        // Remove active state from buttons
        buttons.forEach(btn => {{
            btn.classList.remove("active");
        }});


        // Show selected view
        document
            .getElementById(target)
            .classList.add("active");


        button.classList.add("active");

    }});

}});

</script>


</body>
</html>
"""


Path("combined.html").write_text(
    combined_html,
    encoding="utf-8"
)


print("Created combined.html")