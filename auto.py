# generated automatically by gemini ai
# prompted only with the csv file
import pandas as pd
import io
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

# Daten einlesen
data_string = """
    Datum Uhrzeit  Syst.  Diast.  Pulse
0     6.2   11:00    136      85     76
1     6.2   14:00    140      87     71
2     7.2   12:00    144      92     80
3     7.2   15:00    140      94     78
4     8.2   13:30    143      87     82
5     9.2   12:00    148      91     87
6    10.2   14:00    140      88     80
7    11.2   12:30    146      99     79
8    13.2   21:45    138      79     79
9    14.2   11:00    132      88     68
10   14.2   14:55    149      89     75
11   14.2   23:00    134      71     86
12   15.2   10:00    141      90     87
13   15.2   12:20    140      87     84
14   16.2   10:00    136      86     87
15   16.2   17:00    140      93     85
16   17.2   10:00    148      95     83
17   18.2   12:00    134      89     78
18   18.2   21:25    135      85     79
19   19.2   13:30    130      83     75
20   20.2   12:00    144      82     69
21   21.2   13:00    142      97     70
22   22.2   18:30    128      91     83
23   23.2   12:30    141      88     77
24   23.2   18:10    146      90     82
25   24.2   16:30    135      85     79
26   25.2   19:00    135      86     76
27   26.2   00:30    116      67     77
28   26.2   12:00    133      89     68
29   26.2   23:00    139      85     77
30   27.2   10:00    137      88     74
31   27.2   23:10    139      86     69
32   28.2   16:00    134      84     79
33   28.2   18:00    127      84     72
34   28.2   23:00    122      86     79
35    1.3   10:10    131      90     86
36    1.3   22:30    131      83     74
37    2.3   10:00    130      88     81
38    2.3   23:15    140      85     74
39    3.3    9:00    135      85     78
40    3.3   23:48    129      87     77
41    4.3   10:00    137      91     80
42    4.3   17:45    130      85     76
43    4.3   21:10    133      81     83
44    5.3    7:50    137      86     76
45    6.3    9:30    128      82     80
46    6.3   14:40    124      78     76
47    7.3   00:25    143      88     74
48    7.3   08:20    133      84     87
49    7.3   16:00    122      81     85
50    7.3   22:25    126      83     88
51    8.3   10:00    148      92     84
52    8.3   16:30    131      79     72
53    8.3   20:30    133      85     68
54    9.3   11:40    157      97     71
55    9.3   16:30    134      82     73
56    9.3   20:00    131      83     88
57   10.3    7:20    130      92     85
58   10.3   14:10    132      85     75
59   10.3   19:00    134      86     79
60   12.3   11:10    138      89     79
61   12.3   13:00    133      83     77
62   13.3   17:50    136      82     80
63   14.3   17:40    134      82     96
64   15.3   10:15    136      90     81
65   16.3   00:26    146      91     83
66   18.3   23:20    138      88     71
67   19.3   23:20    144      84     69
68   20.3   22:40    140      91     76
69   21.3   23:00    137      88     72
70   22.3   10:00    132      85     80
71   23.3   11:00    145      90     78
72   23.3   12:00    135      91     73
73   24.3   08:18    129      80     73
74   24.3   10:38    122      78     77
75   25.3   00:20    135      85     73
76   25.3   10:20    136      88     83
77   25.3   10:30    124      80     80
78   26.3   16:20    133      85     74
79   26.3   23:00    130      83     75
80   27.3   19:00    131      95     82
81   28.3   10:00    140      92     76
82   28.3   18:00    122      83     78
83   29.3   13:50    147      89     78
84   30.3   00:55    132      91     80
85   30.3   10:40    139      90     80
86   31.3   17:30    138      86     88
87    1.4   17:00    128      82     78
88    1.4   22:00    138      92     78
89    2.4   11:30    130      87     83
90    2.4   11:30    135      92     81
91    2.4   17:25    122      85     86
92    3.4   11:00    134      91     81
93    3.4   13:00    145      94     78
94    4.4   09:33    139      86     82
95    4.4   16:00    144      99     83
96    5.4   15:00    147      96     82
97    6.4   16:00    146      94     80
98    7.4   12:00    145      94     79
99    8.4   13:45    130      85     73
100   8.4   14:30    137      89     68
101   9.4   18:30    139      94     75
102  10.4   00:20    137      82     72
103  10.4   11:00    136      90     80
104  10.4   23:13    128      80     76
105  11.4   17:00    120      75     84
106  11.4   19:00    120      74     78
107  12.4   09:00    130      80     79
108  13.4   10:00    141      88     76
109  13.4   23:20    132      89     69
110  14.4   10:30    132      82     77
111  14.4   18:30    138      88     71
112  16.4   10:25    116      78     87
113  16.4   10:32    125      85     83
114  16.4   15:00    133      85     71
115  17.4   08:00    130      85     81
"""

df = pd.read_csv(io.StringIO(data_string), sep='\s+', index_col=0)

# Korrekte Datums-/Zeit-Spalte erstellen
# Annahme: Das Jahr ist 2024 (oder ein anderes passendes Jahr)
# Wir müssen die Monate korrekt zuordnen (Februar, März, April)
current_year = 2024
datetime_list = []
current_month = 2 # Start im Februar
for index, row in df.iterrows():
    # row['Datum'] is already in the format day.month as a float or string, so split accordingly
    if isinstance(row['Datum'], str):
        day, month = row['Datum'].split('.')
    else:
        # If Datum is a float (e.g., 6.2), convert to string first
        day, month = str(row['Datum']).split('.')
    day = int(day)
    month = int(month)

    # Monat wechseln, wenn der Tag kleiner wird (z.B. von 28.2 auf 1.3)
    if index > 0 and month != current_month:
         if month < current_month : # Jahreswechsel (nicht in diesem Datensatz relevant)
              current_year += 1
         current_month = month


    date_str = f"{day}.{month}.{current_year}"
    time_str = row['Uhrzeit']
    try:
        dt_obj = pd.to_datetime(f"{date_str} {time_str}", format='%d.%m.%Y %H:%M')
        datetime_list.append(dt_obj)
    except ValueError:
        print(f"Warnung: Konnte Datum/Zeit nicht parsen für Zeile {index}: {date_str} {time_str}")
        datetime_list.append(pd.NaT) # Füge NaT (Not a Time) hinzu bei Fehlern

df['DateTime'] = datetime_list
df = df.dropna(subset=['DateTime']) # Entferne Zeilen mit Parsing-Fehlern
df = df.sort_values('DateTime') # Sortiere nach Zeit

# --- Plot erstellen ---
fig = make_subplots(
    rows=2, cols=3,
    subplot_titles=("Blutdruck & Puls über Zeit", "Verteilung Systolisch", "Verteilung Diastolisch", "Verteilung Puls"),
    specs=[[{"colspan": 3}, None, None],
           [{}, {}, {}]],
    row_heights=[0.6, 0.4] # Höhe der Zeilen anpassen
)

# 1. Zeitverlauf (obere Reihe)
fig.add_trace(go.Scatter(x=df['DateTime'], y=df['Syst.'], mode='lines+markers', name='Systolisch (mmHg)', line=dict(color='red')), row=1, col=1)
fig.add_trace(go.Scatter(x=df['DateTime'], y=df['Diast.'], mode='lines+markers', name='Diastolisch (mmHg)', line=dict(color='blue')), row=1, col=1)
fig.add_trace(go.Scatter(x=df['DateTime'], y=df['Pulse'], mode='lines+markers', name='Puls (bpm)', line=dict(color='green')), row=1, col=1)

# Referenzlinien für Blutdruck
fig.add_hline(y=140, line_dash="dash", line_color="orange", annotation_text="Grenzwert Hoch (Syst.)", annotation_position="bottom right", row=1, col=1)
fig.add_hline(y=90, line_dash="dash", line_color="lightblue", annotation_text="Grenzwert Hoch (Diast.)", annotation_position="bottom right", row=1, col=1)


# 2. Histogramme (untere Reihe)
fig.add_trace(go.Histogram(x=df['Syst.'], name='Syst.', marker_color='red', showlegend=False), row=2, col=1)
fig.add_trace(go.Histogram(x=df['Diast.'], name='Diast.', marker_color='blue', showlegend=False), row=2, col=2)
fig.add_trace(go.Histogram(x=df['Pulse'], name='Pulse', marker_color='green', showlegend=False), row=2, col=3)

# Layout anpassen
fig.update_layout(
    title_text="Auswertung Blutdruck- und Pulsmessungen",
    height=700, # Gesamthöhe der Grafik
    hovermode='x unified' # Zeigt alle Werte für einen Zeitpunkt beim Hovern
)

# Achsenbeschriftungen für Histogramme
fig.update_xaxes(title_text="Systolischer Druck (mmHg)", row=2, col=1)
fig.update_yaxes(title_text="Häufigkeit", row=2, col=1)
fig.update_xaxes(title_text="Diastolischer Druck (mmHg)", row=2, col=2)
fig.update_yaxes(title_text="Häufigkeit", row=2, col=2)
fig.update_xaxes(title_text="Puls (bpm)", row=2, col=3)
fig.update_yaxes(title_text="Häufigkeit", row=2, col=3)

# Achsenbeschriftung für Zeitreihe
fig.update_yaxes(title_text="Wert", row=1, col=1)
fig.update_xaxes(title_text="Datum und Uhrzeit", row=1, col=1)


fig.show()