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
# Reading data from puls_data.csv
output_dir = '/Users/haraldbeker/PythonProjects/blutdruck/' # Define output directory
csv_path = 'puls_data.csv'
plot_html_path = 'combined_plotly.html'
plot_png_path = 'combined_plotly.png'
plot_pdf_path = os.path.join(output_dir, 'blutdruck_plotly.pdf')

def read_csv_file(file_path):
    """
    Reads a CSV file from the specified file path and returns its contents as a pandas DataFrame.

    Parameters:
        file_path (str): The path to the CSV file to be read.

    Returns:
        pandas.DataFrame or None: The DataFrame containing the CSV data if successful, 
        or None if the file is not found, empty, or an error occurs.

    Exceptions:
        Handles FileNotFoundError if the file does not exist.
        Handles pandas.errors.EmptyDataError if the file is empty.
        Handles any other exceptions that may occur during file reading.

    Prints:
        Success or error messages indicating the result of the file reading operation.
    """
    """Read CSV file and return DataFrame."""
    try:
        df = pd.read_csv(file_path)
        print(f"CSV file '{file_path}' read successfully.")
        return df
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"File '{file_path}' is empty.")
        return None
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return None
# --- Plotly Visualization (replaces matplotlib section) ---




def clean_df(df):
# convert columns to stringS otherwise datetime conversion will fail
    df['Datum'] = df['Datum'].astype(str)
    df['Uhrzeit'] = df['Uhrzeit'].astype(str)
    #combine date and time columns to a single datetime column recognized by pandas and matplotlib
    df['Datum_Uhrzeit'] = pd.to_datetime("2025 " + df['Datum'] + ' ' + df['Uhrzeit'], format='%Y %d.%m %H:%M')
    return df


def plot_data(df):
    """
    Generates and saves interactive Plotly visualizations for blood pressure and pulse data.
    This function creates a combined figure with two subplots:
    1. A time series plot showing the progression of systolic, diastolic, and pulse values over time,
       including mean lines and shaded bands for normal ranges.
    2. Overlaid histograms for each metric (systolic, diastolic, pulse) with mean indicators and
       colored bands for normal value ranges.
    The resulting figure is saved as both an HTML file and a PNG image in the specified output directory.
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the following columns:
            - 'Datum_Uhrzeit': datetime values for measurement times
            - 'Systolisch': systolic blood pressure values
            - 'Diastolisch': diastolic blood pressure values
            - 'Pulse': pulse values
    Side Effects
    ------------
    - Saves 'combined_plotly.html' and 'combined_plotly.png' to the global `output_dir`.
    - Prints the maximum histogram frequency and the path to the saved PNG file.
    Notes
    -----
    - Requires Plotly, NumPy, pandas, and os modules.
    - The global variable `output_dir` must be defined before calling this function.
    - The function modifies `output_dir` at the end.
    """
    global output_dir
    mean_systolisch = df['Systolisch'].mean()
    mean_diastolisch = df['Diastolisch'].mean()
    mean_pulse = df['Pulse'].mean()
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

    x0 = df['Datum_Uhrzeit'].min() - timedelta(days=2)
    x1 = df['Datum_Uhrzeit'].max() + timedelta(days=2)
# loop through the metrics systolic, diastolic and pulse  and their properties
    for metric,color,marker,mean,band in [('Systolisch',"blue",'square',mean_systolisch,(120,140)), 
                        ('Diastolisch','green','circle',mean_diastolisch,(80,90)), 
                        ('Pulse','red','diamond',mean_pulse,(60,80))]:
    # --- Time Series Plot (Row 1) ---
        fig.add_trace(
            go.Scatter(
                x=df['Datum_Uhrzeit'], y=df[metric],
                mode='lines+markers', name=metric, line=dict(width=2), marker=dict(size=8, symbol=marker, color=color),
            ),
            row=1, col=1
        )
    # --- Histogram Plot (Row 2) ---
        fig.add_trace(
            go.Histogram(
                x=df[metric], name=metric, marker_color=color, opacity=0.4, xbins=dict(start=bins[0], end=bins[-1], size=5)
            ),
            row=2, col=1
        )
    # Add a horizontal dashed line for the average metric in the time series plot
        fig.add_shape(
            type="line",
            x0=x0, x1=x1,
            y0=mean, y1=mean,
            line=dict(color=color, width=2, dash="dash"),
            row=1, col=1
        )
        fig.add_annotation(  # Add annotation for the average metric in the time series plot
            x=x1,
            y=mean,
            text=f"⌀ {metric[0:4]}: {mean:.1f}",
            showarrow=False,
            font=dict(color=color, size=12, family="Arial"),
            xanchor="left",
            yanchor="middle",
            bgcolor="white",
            bordercolor=color,
            borderwidth=1,
            row=1, col=1 )
                
        # Add a vertical dashed line for the average metric in the histogram plot
        fig.add_shape(
            type="line",
            x0=mean, x1=mean,
            y0=0, y1=max_hist_freq,
            xref='x2', yref='paper',
            line=dict(color=color, width=3, dash='dash'),  # Increased width, dashed for visibility
            layer="below",
            row=2, col=1)
        
        fig.add_annotation( # Add annotation for the average metric in the histogram plot
            x=mean, y=max_hist_freq + 5,  # Slightly above the plot
            xref='x2', yref='paper',
            text=f"⌀ {metric[0:4]}: {mean:.1f}",
            showarrow=False,
            font=dict(color=color, size=12),
            yanchor='bottom',
            row=2, col=1,
            bgcolor="white",  # Add background for better contrast
            bordercolor=color,
            borderwidth=1

        )
        # bands for normal ranges in the time series plot
        fig.add_shape(type="rect", x0=df['Datum_Uhrzeit'].min(), x1=df['Datum_Uhrzeit'].max(),
                y0=band[0], y1=band[1], fillcolor=color, opacity=0.2, line_width=0, row=1, col=1)
        # Add colored bands for histogram x-axis (row 2), in the layer below the histogram
        fig.add_shape(
            type="rect",
            xref='x2', yref='paper',
            x0=band[0], x1=band[1], y0=0, y1=max_hist_freq,
            fillcolor=color, opacity=0.3, line_width=0,
            layer="below",
            row=2, col=1
        )

    fig.update_yaxes(title_text="mmHg / Puls", row=1, col=1)
    fig.update_xaxes(title_text="Datum", row=1, col=1, tickformat="%d.%m", tickangle=20)


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


    fig.update_yaxes(title_text="Häufigkeit", row=2, col=1)
    fig.update_xaxes(title_text="mmHg / Puls", row=2, col=1)

    # Layout and legend
    fig.update_layout(
        title_text="Blutdruckanalyse",
        height=800,
        showlegend=True,
        legend=dict(
            orientation="v",  # Vertical orientation
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=1
        )
    )

    fig.update_layout(width=14 * 96, height=10 * 96)  # 1 inch = 96 px for Plotly


    # Save as HTML and PNG
    plot_html_path = os.path.join(output_dir, 'combined_plotly.html')
    fig.write_html(plot_html_path)
    plot_png_path = os.path.join(output_dir, 'combined_plotly.png')
    fig.write_image(plot_png_path, scale=2)

    print(f"Plotly PNG plot saved to: {plot_png_path}")
    output_dir = '/Users/haraldbeker/PythonProjects/blutdruck/' # Define output directory


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

def  print_table(df):
    styled_table_df = table_df.style \
    .map(highlight_systolisch, subset=['Syst.']) \
    .map(highlight_diastolisch, subset=['Diast.']) \
    .hide(axis='index') \
    .set_table_styles([{'selector': 'th', 'props': [('text-align', 'left')]}, # Right align header
                       {'selector': 'td', 'props': [('text-align', 'right')]}]) # Right align content
    html_file_path = os.path.join(output_dir, 'blutdruck_table.html')
    pdf_file_path = os.path.join(output_dir, 'blutdruck_table_landscape_4col.pdf')
    styled_table_df.to_html(html_file_path, escape=False) # escape=False if using html tags in styles

# Define CSS for landscape, multi-column layout, and smaller font
    css_style = CSS(string='''
    @page {
        size: A4 landscape; /* Set page size and orientation */
        margin: 0.5cm;       /* Optional: Adjust margins */
    }
    body {                 /* Target the main body of the HTML */
        column-count: 4;   /* Arrange content into 4 columns */
        column-gap: 15px;  /* Optional: Adjust space between columns */
    }
    /* Set font size for table elements */
    table, th, td {
        font-size: 9pt;    /* Adjust this value as needed (e.g., 8pt, 10px) */
        break-inside: avoid; /* Try to prevent rows breaking across columns */
        padding: 2px 4px; /* Add some padding */
        border: 1px solid #000; /* Add light borders */
        text-align: right; /* Ensure text is left-aligned */
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
        browser.open(f'file://{os.path.abspath(plot_html_path)}')
        # You might want to open the Markdown file in a text editor or previewer
        # webbrowser might not render it well. Example using default app:
        # if os.path.exists(abs_markdown_path):
        #     os.startfile(abs_markdown_path) # Windows
            # or subprocess.call(['open', abs_markdown_path]) # macOS
            # or subprocess.call(['xdg-open', abs_markdown_path]) # Linux

    except Exception as e:
        print(f"Could not open one or more files: {e}")
        # Fallback or alternative browser logic if needed

# Prepare datetime column
df = read_csv_file(csv_path)
table_df = df.copy()  # Use a deep copy of the DataFrame for the table outputs
table_df['Datum'] = df['Datum'].astype(str)
table_df = table_df.rename(columns={'Systolisch': 'Syst.'})
table_df = table_df.rename(columns={'Diastolisch': 'Diast.'})
df = clean_df(df)
# Plot data
plot_data(df)
# Print table
print_table(df)
# Show all rows and columns in the console
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(table_df)