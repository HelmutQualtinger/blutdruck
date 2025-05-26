import numpy as np
import plotly.graph_objects as go

def z_function(x, y, b_param):
    r_squared = x**2 + y**2
    return np.sin(r_squared) * np.exp(-r_squared * b_param)

# Definiere den Bereich für x und y
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)

# 3. Erstelle die Slider-Schritte und die Anfangsdaten
b_slider_values = np.linspace(0.01, 1, 50) # Erhöhe die Anzahl der Schritte für b

# Initialisiere die Figure
fig = go.Figure()

# Füge die erste Surface-Spur für den Startwert von b hinzu
initial_b = b_slider_values[0]
Z_initial = z_function(X, Y, initial_b)
fig.add_trace(go.Surface(
    z=Z_initial,
    x=X,
    y=Y,
    surfacecolor=Z_initial, # Farbe basierend auf Z-Werten
    colorscale='Viridis',   # Wähle eine Farbskala
    showscale=True,        # Zeige die Farbskala-Legende
    name=f'b = {initial_b:.2f}' # Name für die Legende (optional hier)
))

# Erstelle die Slider-Schritte
steps = []
for i, b in enumerate(b_slider_values):
    Z = z_function(X, Y, b)
    step = dict(
        method='update',
        args=[{'z': [Z], 'surfacecolor': [Z]}],
        label=f'{b:.2f}'
    )
    steps.append(step)

# Definiere die Slider
sliders = [dict(
    active=0,
    pad={"t": 50},
    steps=steps,
    currentvalue={"prefix": "b: "}
)]

fig.update_layout(
    sliders=sliders
)

fig.show()