Based on Romanian The National Institute for Earth Physics NIEP data stations
www.infp.ro
The web system monitor, alert and forecast is meant for study and research only.
Only for demonstration usage. Coded by Adrian Lavric 

Live 
https://radon.qgiengine.com/

![Screenshot_20250601-185208-361](https://github.com/user-attachments/assets/9642efd1-a734-4a60-8fa7-2e1e9fe6f314)

![Screenshot_20250601-185501](https://github.com/user-attachments/assets/c85809b7-ec24-4e4d-add8-0fd687663a47)


🔧 What This Python Script Does:

1. Fetches real data from a remote API (geobs.infp.ro) for:

Radon levels from known stations (e.g., DLMdd, LOPRdd, etc.).

CO₂ levels, applying offset for certain stations.


2. Fetch data for:
Atmospheric chemical potential ACP

3. Adds alert levels depending on thresholds (like red, green, orange).
- standalone on selected stations
- all station
- combined, eg  Radon + Co2

4. Outputs JSON (sensors.json) to be read by the interactive HTML map.

📁 Download the generated JSON for preview/use: Click to download sensors.json


🤖 What the AI Script Do (Model Integration):

The AI component is intended to:

Train a simple prediction model using past sensor data (you’ll feed it with historical radon, CO₂, or ACP/PRC	Pattern Recurrence Cycle, SPM	Synodic Pattern Match, RPG	Resonant Planetary Geometry values).

Predict the next mean values or anomalies based on current readings and patterns.

Automatically flag counties with expected high risk (color-coded).

Eventually support seismic signal classification or anomaly prediction if trained EHZ data.


