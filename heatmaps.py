####### 
# Side-by-side heatmaps for Sitka, Alaska, Santa Barbara, California and Yuma, Arizona using a shared temperature scale.
######

import plotly.offline as pyo
import plotly.graph_objs as go
from plotly import tools
import pandas as pd

Sitka = pd.read_csv('../PlotlyDashboards/2010SitkaAK.csv')
SantaBarbara = pd.read_csv('../PlotlyDashboards/2010SantaBarbaraCA.csv')
Yuma = pd.read_csv('../PlotlyDashboards/2010YumaAZ.csv')

trace_Sitka = go.Heatmap(
    x = Sitka['DAY'],
    y = Sitka['LST_TIME'],
    z = Sitka['T_HR_AVG'],
    colorscale = 'Jet',
    zmin = 5, zmax = 40 # add max/min color values to make each plot consistent
)
trace_SantaBarbara = go.Heatmap(
    x = SantaBarbara['DAY'],
    y = SantaBarbara['LST_TIME'],
    z = SantaBarbara['T_HR_AVG'],
    colorscale = 'Jet',
    zmin = 5, zmax = 40
)
trace_Yuma = go.Heatmap(
    x = Yuma['DAY'],
    y = Yuma['LST_TIME'],
    z = Yuma['T_HR_AVG'],
    colorscale = 'Jet',
    zmin = 5, zmax = 40
)

fig = tools.make_subplots(rows = 1, cols = 3,
    subplot_titles=('Sitka, AK','Santa Barbara, CA', 'Yuma, AZ'),
    shared_yaxes = True,  # this makes the hours appear only on the left
)
fig.append_trace(trace_Sitka, 1, 1)
fig.append_trace(trace_SantaBarbara, 1, 2)
fig.append_trace(trace_Yuma, 1, 3)

fig['layout'].update(      # access the layout directly!
    title = 'Hourly Temperatures, June 1-7, 2010'
)
pyo.plot(fig, filename = 'HeatmapUS.html')