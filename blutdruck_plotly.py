# %%
import pandas as pd
import plotly.graph_objs as go
import plotly.subplots as sp
import numpy as np
import os
from weasyprint import HTML, CSS
import webbrowser
from plotly.subplots import make_subplots
from datetime import timedelta
import plotly.graph_objs as go
# Reading data from puls_data.csv

csv_path = '/Users/haraldbeker/PythonProjects/blutdruck/puls_data.csv'
plot_html_path = '/Users/haraldbeker/PythonProjects/blutdruck/combined_plotly.html'
plot_png_path = '/Users/haraldbeker/PythonProjects/blutdruck/combined_plotly.png'
output_dir = '/Users/haraldbeker/PythonProjects/blutdruck/' # Define output directory
plot_pdf_path = os.path.join(output_dir, 'blutdruck_plotly.pdf')

# --- Plotly Visualization (replaces matplotlib section) ---

# Prepare datetime column
df = pd.read_csv(csv_path)
# Add mean lines
mean_systolisch = df['Systolisch'].mean()
mean_diastolisch = df['Diastolisch'].mean()
mean_pulse = df['Pulse'].mean()

# Creating DataFrame
# convert columns to stringS otherwise datetime conversion will fail
df['Datum'] = df['Datum'].astype(str)
df['Uhrzeit'] = df['Uhrzeit'].astype(str)
table_df = df.copy() # Use this DataFrame for the table outputs
#combine date and time columns to a single datetime column recognized by pandas and matplotlib
df['Datum_Uhrzeit'] = pd.to_datetime("2025 " + df['Datum'] + ' ' + df['Uhrzeit'], format='%Y %d.%m %H:%M')

# Create subplots: 2 rows, 1 column
fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=False,
    vertical_spacing=0.15,
    subplot_titles=("Blutdruck und Puls im Zeitverlauf", "Histogramme von Systolisch, Diastolisch, & Puls"),
    x_title="",
    y_title="",
    specs=[[{"secondary_y": False}], [{"secondary_y": False}]],
    print_grid=False,
    row_titles=None,
    column_titles=None,
    # Add visible frames (boxes) around each subplot
    # We'll use 'subplot_titles' for titles, and add layout shapes for boxes below
)
# --- Time Series Plot (Row 1) ---
fig.add_trace(
    go.Scatter(
        x=df['Datum_Uhrzeit'], y=df['Systolisch'],
        mode='lines+markers', name='Systolisch', line=dict(color='blue'), marker=dict(symbol='circle', size=8)
    ),
    row=1, col=1
)
# Add a blue horizontal dashed line for the average systolic pressure
# Calculate 7 days before and after the min/max datetime for the average line

x0 = df['Datum_Uhrzeit'].min() - timedelta(days=2)
x1 = df['Datum_Uhrzeit'].max() + timedelta(days=2)

fig.add_shape(
    type="line",
    x0=x0, x1=x1,
    y0=mean_systolisch, y1=mean_systolisch,
    line=dict(color="blue", width=2, dash="dash"),
    row=1, col=1
)
fig.add_annotation(
    x=x1,
    y=mean_systolisch,
    text=f"⌀ Syst{mean_systolisch:.1f}",
    showarrow=False,
    font=dict(color="blue", size=12),
    xanchor="left",
    yanchor="middle",
    bgcolor="white",
    bordercolor="blue",
    borderwidth=1,
    row=1, col=1
)
fig.add_trace(
    go.Scatter(
        x=df['Datum_Uhrzeit'], y=df['Diastolisch'],
        mode='lines+markers', name='Diastolisch', line=dict(color='green', dash='dash'), marker=dict(symbol='square', size=8)
    ),
    row=1, col=1
)

fig.add_shape(
    type="line",
    x0=x0, x1=x1,
    y0=mean_diastolisch, y1=mean_diastolisch,
    line=dict(color="green", width=2, dash="dash"),
    row=1, col=1
)


fig.add_annotation(
    x=x1,
    y=mean_diastolisch,
    text=f"⌀ Diast: {mean_diastolisch:.1f}",
    showarrow=False,
    font=dict(color="green", size=12),
    xanchor="left",
    yanchor="middle",
    bgcolor="white",
    bordercolor="green",
    borderwidth=1,
    row=1, col=1
)
fig.add_trace(
    go.Scatter(
        x=df['Datum_Uhrzeit'], y=df['Pulse'],
        mode='lines+markers', name='Puls', line=dict(color='red', dash='dot'), marker=dict(symbol='triangle-up', size=8)
    ),
    row=1, col=1
)

fig.add_shape(
    type="line",
    x0=x0, x1=x1,
    y0=mean_pulse, y1=mean_pulse,
    line=dict(color="red", width=2, dash="dash"),
    row=1, col=1
)

fig.add_annotation(
    x=x1,
    y=mean_pulse,
    text=f"⌀ Puls: {mean_pulse:.1f}",
    showarrow=False,
    font=dict(color="red", size=12),
    xanchor="left",
    yanchor="middle",
    bgcolor="white",
    bordercolor="red",
    borderwidth=1,
    row=1, col=1
)
# Reference lines and bands
for y_val in [80, 90, 120, 140]:
    fig.add_shape(type="line", x0=df['Datum_Uhrzeit'].min(), x1=df['Datum_Uhrzeit'].max(),
                  y0=y_val, y1=y_val, line=dict(color="lightgrey", width=1), row=1, col=1)

# Add colored bands for normal ranges
fig.add_shape(type="rect", x0=df['Datum_Uhrzeit'].min(), x1=df['Datum_Uhrzeit'].max(),
              y0=80, y1=90, fillcolor="lightgreen", opacity=0.3, line_width=0, row=1, col=1)
fig.add_shape(type="rect", x0=df['Datum_Uhrzeit'].min(), x1=df['Datum_Uhrzeit'].max(),
              y0=120, y1=140, fillcolor="lightblue", opacity=0.3, line_width=0, row=1, col=1)

fig.update_yaxes(title_text="mmHg / Puls", row=1, col=1)
fig.update_xaxes(title_text="Datum", row=1, col=1, tickformat="%d.%m", tickangle=45)

# --- Histogram Plot (Row 2) ---
# Compute bins
min_val = df[['Systolisch', 'Diastolisch', 'Pulse']].min().min()
max_val = df[['Systolisch', 'Diastolisch', 'Pulse']].max().max()
bins = np.arange(min_val , max_val , 5)

# Compute histogram counts for each variable
hist_syst, _ = np.histogram(df['Systolisch'], bins=bins)
hist_diast, _ = np.histogram(df['Diastolisch'], bins=bins)
hist_pulse, _ = np.histogram(df['Pulse'], bins=bins)
max_hist_freq = max(hist_syst.max(), hist_diast.max(), hist_pulse.max())
print(f"Maximum histogram frequency: {max_hist_freq}")

fig.add_trace(
    go.Histogram(
        x=df['Systolisch'], name='Systolisch', marker_color='blue', opacity=0.4, xbins=dict(start=bins[0], end=bins[-1], size=5)
    ),
    row=2, col=1
)
fig.add_trace(
    go.Histogram(
        x=df['Diastolisch'], name='Diastolisch', marker_color='green', opacity=0.4, xbins=dict(start=bins[0], end=bins[-1], size=5)
    ),
    row=2, col=1
)
fig.add_trace(
    go.Histogram(
        x=df['Pulse'], name='Puls', marker_color='red', opacity=0.4, xbins=dict(start=bins[0], end=bins[-1], size=5)
    ),
    row=2, col=1
)

# Show grid for histograms (row 2)
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey', row=2, col=1,dtick=5)
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey', row=2, col=1)

fig.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor='lightgrey',
    row=1, col=1,
    dtick="604800000"  # 7 days in milliseconds for Plotly datetime axes
)
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey', row=1, col=1, dtick=5)



for val, color, label in [
    (mean_systolisch, 'blue', f'⌀ Syst: {mean_systolisch:.1f}'),
    (mean_diastolisch, 'green', f'⌀ Dias: {mean_diastolisch:.1f}'),
    (mean_pulse, 'red', f'⌀ Puls: {mean_pulse:.1f}')
]:
    fig.add_shape(
        type="line",
        x0=val, x1=val,
        y0=0, y1=max_hist_freq,
        xref='x2', yref='paper',
        line=dict(color=color, width=3, dash='dash'),  # Increased width, dashed for visibility
        row=2, col=1
    )
    fig.add_annotation(
        x=val, y=max_hist_freq + 5,  # Slightly above the plot
        xref='x2', yref='paper',
        text=label,
        showarrow=False,
        font=dict(color=color, size=12),
        yanchor='bottom',
        row=2, col=1,
        bgcolor="white",  # Add background for better contrast
        bordercolor=color,
        borderwidth=1
    )
    
    # Add colored bands for histogram x-axis (row 2), in the layer below the histogram
fig.add_shape(
        type="rect",
        xref='x2', yref='paper',
        x0=80, x1=90, y0=0, y1=max_hist_freq,
        fillcolor="lightgreen", opacity=0.3, line_width=0,
        layer="below",
        row=2, col=1
    )
fig.add_shape(
        type="rect",
        xref='x2', yref='paper',
        x0=120, x1=140, y0=0, y1=max_hist_freq,
        fillcolor="lightblue", opacity=0.3, line_width=0,
        layer="below",
        row=2, col=1
    )

fig.update_yaxes(title_text="Häufigkeit", row=2, col=1)
fig.update_xaxes(title_text="mmHg / Puls", row=2, col=1)

# Layout and legend
fig.update_layout(
    title_text="Blutdruckanalyse",
    height=900,
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

fig.write_html(plot_html_path)
webbrowser.open(f'file://{os.path.abspath(plot_html_path)}')


# Save as HTML and PNG
plot_html_path = os.path.join(output_dir, 'combined_plotly.html')
plot_png_path = os.path.join(output_dir, 'combined_plotly.png')
fig.write_html(plot_html_path)
fig.write_image(plot_png_path, scale=2)
print(f"Plotly HTML plot saved to: {plot_html_path}")
print(f"Plotly PNG plot saved to: {plot_png_path}")
output_dir = '/Users/haraldbeker/PythonProjects/blutdruck/' # Define output directory

# Ensure output directory exists (optional, good practice)
# os.makedirs(output_dir, exist_ok=True)

df = pd.read_csv(csv_path)



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
html_file_path = os.path.join(output_dir, 'blutdruck_table.html')
pdf_file_path = os.path.join(output_dir, 'blutdruck_table_landscape_3col.pdf')
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
