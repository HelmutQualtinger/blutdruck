# %%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec
import numpy as np
import os

# Reading data from puls_data.csv
df = pd.read_csv('/Users/haraldbeker/PythonProjects/blutdruck/puls_data.csv')

# Creating DataFrame
# %%
# print(df.dtypes)
df['Datum'] = df['Datum'].astype(str)
df['Uhrzeit'] = df['Uhrzeit'].astype(str)
table_df = df.copy()
# Datum und Uhrzeit kombinieren und in datetime umwandeln
df['Datum_Uhrzeit'] = pd.to_datetime("2025 " + df['Datum'] + ' ' + df['Uhrzeit'], format='%Y %d.%m %H:%M')

# Set up the figure with subplots
plt.style.use('seaborn-v0_8-whitegrid')
fig = plt.figure(figsize=(12, 8))
gs = GridSpec(2, 1, height_ratios=[2, 1], hspace=0.3)

# Time series plot (top subplot)
ax1 = fig.add_subplot(gs[0])
ax1.plot(df['Datum_Uhrzeit'], df['Systolisch'], 'o-', color='blue', linewidth=2, label='Systolisch')
ax1.plot(df['Datum_Uhrzeit'], df['Diastolisch'], 's--', color='green', linewidth=2, label='Diastolisch')
ax1.plot(df['Datum_Uhrzeit'], df['Pulse'], '^:', color='red', linewidth=1, label='Puls')

# Reference lines
# Reference lines
for y_val in [80, 90, 120, 140]:
    ax1.axhline(y=y_val, color='black', linestyle='-', linewidth=1)

# Add light green bands for normal ranges
ax1.axhspan(80, 90, facecolor='lightgreen', alpha=0.3)
ax1.axhspan(120, 140, facecolor='lightgreen', alpha=0.3)
# Set y-ticks every 5 units
y_min, y_max = ax1.get_ylim()
ax1.set_yticks(np.arange(np.floor(y_min / 5) * 5, np.ceil(y_max / 5) * 5 + 1, 5))
# Format the date axis
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
ax1.xaxis.set_major_locator(mdates.DayLocator())
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

# Labels and title for time series
ax1.set_title('Blutdruck und Pulse im Zeitverlauf', fontsize=14)
ax1.set_xlabel('Datum')
ax1.set_ylabel('mmHg')
ax1.legend()
ax1.grid(True)

# Histogram plot (bottom subplot)
ax2 = fig.add_subplot(gs[1])

# Calculate means
mean_systolisch = df['Systolisch'].mean()
mean_diastolisch = df['Diastolisch'].mean()
mean_pulse = df['Pulse'].mean()

# Create histograms
bins = np.arange(min(df['Pulse'].min(), df['Diastolisch'].min(), df['Systolisch'].min()) - 5,
                 df['Systolisch'].max() + 5, 2)

ax2.hist(df['Systolisch'], bins=bins, alpha=0.5, color='blue', label='Systolisch')
ax2.hist(df['Diastolisch'], bins=bins, alpha=0.5, color='green', label='Diastolisch')
ax2.hist(df['Pulse'], bins=bins, alpha=0.3, color='red', label='Puls')

# Add vertical lines for means
ax2.axvline(mean_systolisch, color='blue', linestyle='-', linewidth=2)
ax2.axvline(mean_diastolisch, color='cyan', linestyle='-', linewidth=2)
ax2.axvline(mean_pulse, color='red', linestyle='-', linewidth=2)

# Add text for means
ax2.text(mean_systolisch + 1, ax2.get_ylim()[1] * 0.95, f'⌀ Systolisch: {mean_systolisch:.1f}', 
         color='blue', fontweight='bold')
ax2.text(mean_diastolisch + 1, ax2.get_ylim()[1] * 0.85, f'⌀ Diastolisch: {mean_diastolisch:.1f}', 
         color='green', fontweight='bold')
ax2.text(mean_pulse + 1, ax2.get_ylim()[1] * 0.75, f'⌀ Puls: {mean_pulse:.1f}', 
         color='red', fontweight='bold')

# Reference lines for normal ranges
for value in [80, 90, 120, 140]:
    ax2.axvline(value, color='green', linestyle=':', linewidth=2)

# Labels and title for histogram
ax2.set_title('Histogramme von Systolisch, Diastolisch, & Puls', fontsize=14)
ax2.set_xlabel('mmHg')
ax2.set_ylabel('Häufigkeit')
ax2.legend()
ax2.grid(True)

# Overall title
fig.suptitle('Blutdruckanalyse', fontsize=16, y=0.98)

# Update figure size to 12x8 inches

home_dir = os.path.expanduser("~")

plt.savefig(os.path.join(home_dir, 'PythonProjects/blutdruck/combined_plot.pdf'), bbox_inches='tight')
plt.savefig('/Users/haraldbeker/PythonProjects/blutdruck/combined_plot.png', dpi=300, bbox_inches='tight')
plt.show()

# Table styling (using the same code you had)
def highlight_systolisch(val):
    color = 'black; font-weight: bold' if val >= 140 else ''
    return f'color: {color}'

def highlight_diastolisch(val):
    color = 'black; font-weight: bold' if val >= 90 else ''
    return f'color: {color}'

styled_table_df = table_df.style.map(highlight_systolisch, subset=['Systolisch'])
styled_table_df = styled_table_df.map(highlight_diastolisch, subset=['Diastolisch'])
styled_table_df = styled_table_df.hide(axis='index')
styled_table_df.to_html('/Users/haraldbeker/PythonProjects/blutdruck/blutdruck_table.html')

from weasyprint import HTML
import webbrowser
import os
# HTML-Datei in PDF umwandeln
html = HTML('/Users/haraldbeker/PythonProjects/blutdruck/blutdruck_table.html')
html.write_pdf('/Users/haraldbeker/PythonProjects/blutdruck/blutdruck_table.pdf')

# Open files
webbrowser.get("safari").open('file:///Users/haraldbeker/PythonProjects/blutdruck/blutdruck_table.html')
webbrowser.get('safari').open('file:///Users/haraldbeker/PythonProjects/blutdruck/combined_plot.pdf')  # Open PNG instead of HTML
# %%


