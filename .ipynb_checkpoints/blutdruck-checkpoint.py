# %%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec
import numpy as np
import os
from weasyprint import HTML, CSS # Make sure weasyprint is imported if not already
import webbrowser
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'

# Reading data from puls_data.csv
csv_path = '/Users/haraldbeker/PythonProjects/blutdruck/puls_data.csv'
output_dir = '/Users/haraldbeker/PythonProjects/blutdruck/' # Define output directory

# Ensure output directory exists (optional, good practice)
# os.makedirs(output_dir, exist_ok=True)

df = pd.read_csv(csv_path)

# Creating DataFrame
# %%
# convert columns to stringS otherwise datetime conversion will fail
df['Datum'] = df['Datum'].astype(str)
df['Uhrzeit'] = df['Uhrzeit'].astype(str)
table_df = df.copy() # Use this DataFrame for the table outputs
#combine date and time columns to a single datetime column recognized by pandas and matplotlib
df['Datum_Uhrzeit'] = pd.to_datetime("2025 " + df['Datum'] + ' ' + df['Uhrzeit'], format='%Y %d.%m %H:%M')

# Set up the figure with subplots
# plt.style.use('seaborn-v0_8-whitegrid')
fig = plt.figure(figsize=(12, 8))
gs = GridSpec (2, 1, height_ratios=[1, 1], hspace=0.5)

# Time series plot (top subplot)
ax1 = fig.add_subplot(gs[0])
ax1.plot(df['Datum_Uhrzeit'], df['Systolisch'], 'o-', color='blue', linewidth=2, label='Systolisch')
ax1.plot(df['Datum_Uhrzeit'], df['Diastolisch'], 's--', color='green', linewidth=2, label='Diastolisch')
ax1.plot(df['Datum_Uhrzeit'], df['Pulse'], '^:', color='red', linewidth=1, label='Puls')

# Add markers for each data point
ax1.plot(df['Datum_Uhrzeit'], df['Systolisch'], 'o', color='blue', markersize=5)
ax1.plot(df['Datum_Uhrzeit'], df['Diastolisch'], 's', color='green', markersize=5)

# Reference lines
for y_val in [80, 90, 120, 140]:
    ax1.axhline(y=y_val, color='black', linestyle='-', linewidth=1)

# Add light green bands for normal ranges
ax1.axhspan(80, 90, facecolor='lightgreen', alpha=0.3) # Diastolic normal/high normal boundary
ax1.axhspan(120, 140, facecolor='yellow', alpha=0.3) # Systolic normal/high normal boundary

# Set y-ticks every 5 units
y_min, y_max = ax1.get_ylim()
# Ensure y_min and y_max cover the data range reasonably
y_min = min(y_min, df[['Systolisch', 'Diastolisch', 'Pulse']].min().min() - 5)
y_max = max(y_max, df[['Systolisch', 'Diastolisch', 'Pulse']].max().max() + 5)
ax1.set_yticks(np.arange(np.floor(y_min / 5) * 5, np.ceil(y_max / 5) * 5 + 1, 5))
ax1.set_ylim(y_min, y_max) # Apply the adjusted limits

# Format the date axis
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
# Set the locator to show ticks every 7 days (or adjust as needed)
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=7))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha="right") # Improve label rotation alignment

# Labels and title for time series
ax1.set_title('Blutdruck und Pulse im Zeitverlauf', fontsize=14)
ax1.set_xlabel('Datum')
ax1.set_ylabel('mmHg / Puls') # Adjust label if needed
ax1.grid(True)
ax1.legend(loc='center left', frameon=False, fontsize=10)

# Histogram plot (bottom subplot)
ax2 = fig.add_subplot(gs[1])

# Calculate means
mean_systolisch = df['Systolisch'].mean()
mean_diastolisch = df['Diastolisch'].mean()
mean_pulse = df['Pulse'].mean()

# Create histograms
# Adjust bins to be more appropriate for the data ranges
min_val = df[['Systolisch', 'Diastolisch', 'Pulse']].min().min()
max_val = df[['Systolisch', 'Diastolisch', 'Pulse']].max().max()
bins = np.arange(min_val - 5, max_val + 10, 2) # Use step of 5, ensure range covers max+5

ax2.hist(df['Systolisch'], bins=bins, alpha=0.4, color='blue', label='Systolisch', edgecolor='black')
ax2.hist(df['Diastolisch'], bins=bins, alpha=0.4, color='green', label='Diastolisch', edgecolor='black')
ax2.hist(df['Pulse'], bins=bins, alpha=0.4, color='red', label='Puls', edgecolor='black')

# Add vertical lines for means
ax2.axvline(mean_systolisch, color='blue', linestyle='-', linewidth=2, label=f'⌀ Syst: {mean_systolisch:.1f}')
ax2.axvline(mean_diastolisch, color='green', linestyle='-', linewidth=2, label=f'⌀ Dias: {mean_diastolisch:.1f}')
ax2.axvline(mean_pulse, color='red', linestyle='-', linewidth=2, label=f'⌀ Puls: {mean_pulse:.1f}')

# Remove text annotations for means as they are now in the legend
# ax2.text(mean_systolisch + 1, ax2.get_ylim()[1] * 0.9, f'⌀ Systolisch: {mean_systolisch:.1f}', color='blue', fontweight='bold')
# ax2.text(mean_diastolisch + 1, ax2.get_ylim()[1] * 0.8, f'⌀ Diastolisch: {mean_diastolisch:.1f}', color='green', fontweight='bold')
# ax2.text(mean_pulse + 1, ax2.get_ylim()[1] * 0.7, f'⌀ Puls: {mean_pulse:.1f}', color='red', fontweight='bold')

# Reference lines for normal ranges
for value in [80, 90, 120, 140]:
    ax2.axvline(value, color='grey', linestyle=':', linewidth=1.5)

# Labels and title for histogram
ax2.set_title('Histogramme von Systolisch, Diastolisch, & Puls', fontsize=14)
ax2.set_xlabel('mmHg / Puls')
ax2.set_ylabel('Häufigkeit')
ax2.legend()
ax2.grid(True)

# Overall title
fig.suptitle('Blutdruckanalyse', fontsize=16, y=0.98)

# Adjust layout to prevent overlap
plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust rect to make space for suptitle

# Save the plot
plot_png_path = os.path.join(output_dir, 'combined_plot.png')
plot_pdf_path = os.path.join(output_dir, 'combined_plot.pdf')
plt.savefig(plot_png_path, dpi=300, bbox_inches='tight')
plt.savefig(plot_pdf_path, bbox_inches='tight')
plt.show()
plt.close(fig) # Close the figure after saving and showing

# --- HTML/PDF Table Generation ---
html_file_path = os.path.join(output_dir, 'blutdruck_table.html')
pdf_file_path = os.path.join(output_dir, 'blutdruck_table_landscape_3col.pdf')

# Table styling
def highlight_systolisch(val):
    # Highlight if >= 140 (Stage 2 Hypertension) or < 90 (Hypotension)
    color = ''
    weight = 'normal'
    if val >= 140:
        color = 'red'
        weight = 'bold'
    elif val < 90:
         color = 'blue'
    return f'color: {color}; font-weight: {weight};'

def highlight_diastolisch(val):
    # Highlight if >= 90 (Stage 2 Hypertension) or < 60 (Hypotension)
    color = ''
    weight = 'normal'
    if val >= 90:
        color = 'red'
        weight = 'bold'
    elif val < 60:
        color = 'blue'
    return f'color: {color}; font-weight: {weight};'

styled_table_df = table_df.style \
    .map(highlight_systolisch, subset=['Systolisch']) \
    .map(highlight_diastolisch, subset=['Diastolisch']) \
    .hide(axis='index') \
    .set_table_styles([{'selector': 'th', 'props': [('text-align', 'left')]},
                       {'selector': 'td', 'props': [('text-align', 'left')]}]) # Left align content

styled_table_df.to_html(html_file_path, escape=False) # escape=False if using html tags in styles

# Define CSS for landscape, multi-column layout, and smaller font
css_style = CSS(string='''
    @page {
        size: A4 landscape; /* Set page size and orientation */
        margin: 1cm;       /* Optional: Adjust margins */
    }
    body {                 /* Target the main body of the HTML */
        column-count: 3;   /* Arrange content into 3 columns */
        column-gap: 15px;  /* Optional: Adjust space between columns */
    }
    /* Set font size for table elements */
    table, th, td {
        font-size: 8pt;    /* Adjust this value as needed (e.g., 8pt, 10px) */
        break-inside: avoid; /* Try to prevent rows breaking across columns */
        padding: 2px 4px; /* Add some padding */
        border: 1px solid #ccc; /* Add light borders */
        text-align: left; /* Ensure text is left-aligned */
    }
    th {
        background-color: #f2f2f2; /* Light grey background for headers */
        font-weight: bold;
    }
    table {
        border-collapse: collapse; /* Collapse borders */
        width: 100%; /* Make table use full column width */
    }
''')

# Convert HTML to PDF with the specified CSS
try:
    html = HTML(html_file_path)
    html.write_pdf(pdf_file_path, stylesheets=[css_style]) # Apply the CSS
    print(f"HTML table saved to: {html_file_path}")
    print(f"PDF table saved to: {pdf_file_path}")
except Exception as e:
    print(f"Error converting HTML to PDF: {e}")


# --- Generate Markdown Table ---
markdown_file_path = os.path.join(output_dir, 'blutdruck_protocol.md')

try:
    # Use the 'pipe' format which is common for Markdown tables
    # index=False removes the DataFrame index column
    markdown_string = table_df.to_markdown(index=False, tablefmt="pipe")

    # Write the markdown string to a file
    with open(markdown_file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_string)
    print(f"Markdown protocol table saved to: {markdown_file_path}")
except Exception as e:
    print(f"Error saving Markdown file: {e}")

# --- Open generated files ---
try:
    # Use absolute paths for webbrowser
    abs_html_path = os.path.abspath(html_file_path)
    abs_pdf_path = os.path.abspath(pdf_file_path)
    abs_plot_pdf_path = os.path.abspath(plot_pdf_path)
    abs_markdown_path = os.path.abspath(markdown_file_path) # Added markdown path

    # Open files (adjust browser if needed)
    browser = webbrowser.get("safari") # Or use webbrowser.open() for default browser
    browser.open(f'file://{abs_html_path}')
    browser.open(f'file://{abs_pdf_path}')
    browser.open(f'file://{abs_plot_pdf_path}')
    # You might want to open the Markdown file in a text editor or previewer
    # webbrowser might not render it well. Example using default app:
    # if os.path.exists(abs_markdown_path):
    #     os.startfile(abs_markdown_path) # Windows
        # or subprocess.call(['open', abs_markdown_path]) # macOS
        # or subprocess.call(['xdg-open', abs_markdown_path]) # Linux

except Exception as e:
    print(f"Could not open one or more files: {e}")
    # Fallback or alternative browser logic if needed
