# Blutdruckanalyse-Projekt

Dieses Projekt ermöglicht die Analyse und Visualisierung von Blutdruck- und Pulsmessdaten, die in einer CSV-Datei gespeichert sind. Es generiert interaktive Diagramme, Berichte und Tabellen in verschiedenen Formaten (HTML, PDF, PNG, Markdown).

---

## Inhaltsverzeichnis

- [Installation](#installation)
  - [Voraussetzungen](#voraussetzungen)
  - [Installation der Abhängigkeiten](#installation-der-abhängigkeiten)
- [Datenquelle](#datenquelle)
  - [Format der CSV-Datei](#format-der-csv-datei)
- [Nutzung](#nutzung)
  - [Skripte ausführen](#skripte-ausführen)
- [Generierte Dateien](#generierte-dateien)
  - [Visualisierungen](#visualisierungen)
  - [Tabellen](#tabellen)
  - [Automatisches Öffnen](#automatisches-öffnen)
- [Beispielausgabe](#beispielausgabe)
  - [Beispiel-Plot](#beispiel-plot)
  - [Beispiel-Tabelle (Markdown)](#beispiel-tabelle-markdown)
- [Hinweise](#hinweise)
- [Lizenz](#lizenz)# Blutdruck Analyse und Visualisierung Skript

Dieses Python-Skript (`blutdruck_plotly.py`) dient zur Analyse und Visualisierung von Blutdruck- und Pulsdaten, die in einer CSV-Datei gespeichert sind. Es generiert interaktive Diagramme mit Plotly, erstellt formatierte Tabellen (HTML, PDF, Markdown) und öffnet einige der erzeugten Dateien automatisch im Webbrowser.

## Inhaltsverzeichnis

- Beschreibung
- Installation
- Datenquelle
- Verwendung
- Erzeugte / Geöffnete Dateien
- Konfiguration
- Abhängigkeiten

## Beschreibung

Das Skript führt folgende Schritte aus:

1.  **Einlesen der Daten:** Liest Blutdruck- und Pulsdaten aus einer CSV-Datei (`puls_data.csv`).
2.  **Datenbereinigung:** Konvertiert Datums- und Zeitangaben in ein für die Analyse geeignetes Datetime-Format.
3.  **Visualisierung:** Erstellt mithilfe von Plotly ein kombiniertes Diagramm, das Folgendes anzeigt:
    *   Einen Zeitverlauf der systolischen, diastolischen und Pulswerte mit Markern, Linien und Mittelwertlinien.
    *   Überlagerte Histogramme für Systolisch, Diastolisch und Puls zur Darstellung der Häufigkeitsverteilung.
    *   Farbige Bänder in beiden Diagrammen zur Kennzeichnung der Normbereiche.
    *   Das Diagramm wird als interaktive HTML-Datei und als statisches PNG-Bild gespeichert.
4.  **Tabellenerstellung:** Generiert eine formatierte Tabelle der Messwerte:
    *   Werte außerhalb der Normbereiche werden farblich hervorgehoben (Rot für zu hohe, Blau für zu niedrige Werte).
    *   Die Tabelle wird als HTML-, PDF- (A4 Querformat, 4 Spalten, kleine Schrift) und Markdown-Datei gespeichert.
5.  **Automatisches Öffnen:** Öffnet die erzeugte Plot-HTML-Datei sowie die Tabellen-HTML- und PDF-Dateien im Standard-Webbrowser (im Skript ist "safari" fest codiert, kann aber angepasst werden).

## Installation

**Voraussetzungen:**

*   Python 3.x
*   pip (Python Paketmanager)
*   Git (optional, falls das Skript aus einem Repository geklont wird)

**Installationsschritte:**

1.  **Skript herunterladen/klonen:**
    *   Speichere die Datei `blutdruck_plotly.py` auf deinem Computer.
    *   *Oder (falls in Git):*
      ```bash
      git clone [URL deines Git-Repositories]
      cd [Projektverzeichnis-Name]
      ```

2.  **Abhängigkeiten installieren:**
    Öffne ein Terminal oder eine Eingabeaufforderung im Verzeichnis, in dem sich das Skript befindet, und installiere die benötigten Python-Bibliotheken:
    ```bash
    pip install pandas plotly numpy weasyprint kaleido
    ```
    *   `pandas`: Für Datenmanipulation und das Einlesen der CSV-Datei.
    *   `plotly`: Für die Erstellung der interaktiven Diagramme.
    *   `numpy`: Für numerische Operationen (wird oft von pandas/plotly benötigt).
    *   `weasyprint`: Zum Erstellen der PDF-Datei aus HTML.
    *   `kaleido`: Wird von Plotly benötigt, um Diagramme als statische Bilder (z.B. PNG) zu speichern.

3.  **Daten vorbereiten:** Stelle sicher, dass die Eingabedatei `puls_data.csv` im selben Verzeichnis wie das Skript liegt oder passe den Pfad im Skript an (siehe Konfiguration).

## Datenquelle

*   **Datei:** Das Skript erwartet die Eingabedaten in einer Datei namens `puls_data.csv`.
*   **Speicherort:** Diese Datei muss sich standardmäßig im selben Verzeichnis befinden, von dem aus das Skript `blutdruck_plotly.py` ausgeführt wird. Der Pfad ist im Skript als Variable `csv_path` definiert.
*   **Format:** CSV (Comma Separated Values).
*   **Erwartete Spalten:** Die CSV-Datei muss mindestens die folgenden Spalten enthalten:
    *   `Datum`: Das Datum der Messung (z.B. `TT.MM`).
    *   `Uhrzeit`: Die Uhrzeit der Messung (z.B. `HH:MM`).
    *   `Systolisch`: Der systolische Blutdruckwert (Zahl).
    *   `Diastolisch`: Der diastolische Blutdruckwert (Zahl).
    *   `Pulse`: Der Pulswert (Zahl).

## Verwendung

1.  Öffne ein Terminal oder eine Eingabeaufforderung.
2.  Navigiere in das Verzeichnis, das `blutdruck_plotly.py` und `puls_data.csv` enthält.
3.  Führe das Skript aus:
    ```bash
    python blutdruck_plotly.py
    ```
4.  Das Skript verarbeitet die Daten, generiert die Ausgabedateien im konfigurierten `output_dir` und öffnet anschließend automatisch die HTML- und PDF-Dateien im Webbrowser. Die Konsolenausgabe zeigt den Fortschritt und die Pfade der gespeicherten Dateien an. Außerdem wird die formatierte Tabelle in der Konsole ausgegeben.

## Erzeugte / Geöffnete Dateien

Das Skript interagiert mit folgenden Dateien:

**Eingabe (wird gelesen):**

*   `puls_data.csv`: (Standardname) Enthält die rohen Blutdruck- und Pulsdaten im CSV-Format. Der Pfad ist im Skript konfigurierbar (`csv_path`).

**Ausgabe (wird erzeugt im `output_dir`):**

*   `[output_dir]/combined_plotly.html`: Interaktives Plotly-Diagramm mit Zeitverlauf und Histogrammen.
*   `[output_dir]/combined_plotly.png`: Statisches PNG-Bild des Plotly-Diagramms.
*   `[output_dir]/blutdruck_table.html`: Formatierte HTML-Tabelle der Messwerte mit farblichen Hervorhebungen.
*   `[output_dir]/blutdruck_table_landscape_4col.pdf`: Formatierte PDF-Tabelle der Messwerte (A4 Querformat, 4 Spalten, kleine Schrift).
*   `[output_dir]/blutdruck_protocol.md`: Eine einfache Markdown-Tabelle der Messwerte.

**Automatisch geöffnet (im Webbrowser):**

*   `[output_dir]/combined_plotly.html`
*   `[output_dir]/blutdruck_table.html`
*   `[output_dir]/blutdruck_table_landscape_4col.pdf`

*(Hinweis: Das Skript versucht, diese Dateien mit dem `webbrowser`-Modul zu öffnen. Das Öffnen der Markdown-Datei ist im Code vorbereitet, aber auskommentiert.)*

## Konfiguration

Einige Pfade sind direkt am Anfang des Skripts `blutdruck_plotly.py` festgelegt und müssen bei Bedarf angepasst werden:

*   `output_dir`: Das Verzeichnis, in dem alle Ausgabedateien (Diagramme, Tabellen) gespeichert werden.
    *   Standard: `/Users/haraldbeker/PythonProjects/blutdruck/` *(Dies ist ein absoluter Pfad und sollte wahrscheinlich an deine Systemumgebung angepasst werden, z.B. zu einem relativen Pfad wie `.` für das aktuelle Verzeichnis oder `output/`)*.
*   `csv_path`: Der Pfad zur Eingabe-CSV-Datei.
    *   Standard: `puls_data.csv` (erwartet die Datei im selben Verzeichnis wie das Skript).
*   `webbrowser.get("safari")`: Legt fest, dass Safari zum Öffnen der Dateien verwendet werden soll. Ändere dies zu `webbrowser.open()` um den Standardbrowser zu verwenden oder gib einen anderen Browser an.

## Abhängigkeiten

*   pandas
*   plotly
*   numpy
*   weasyprint
*   kaleido

- [Kontakt](#kontakt)

---

## Installation

### Voraussetzungen

Stellen Sie sicher, dass die folgenden Komponenten auf Ihrem System installiert sind:

1.  **Python**: Version 3.8 oder höher. Sie können Ihre Python-Version überprüfen, indem Sie `python --version` oder `python3 --version` im Terminal eingeben.
2.  **pip**: Der Python-Paketmanager. Er ist normalerweise bei aktuellen Python-Installationen enthalten.

### Installation der Abhängigkeiten

Dieses Projekt verwendet mehrere Python-Bibliotheken. Installieren Sie diese über die Kommandozeile (Terminal) mit `pip`:

```bash
pip install pandas numpy plotly weasyprint webbrowser