# Blutdruckanalyse

Dieses Projekt visualisiert und analysiert Blutdruck- und Pulsmessdaten aus der CSV-Datei [puls_data.csv](//PythonProjects/blutdruck/puls_data.csv).

## Inhalt

- **Datenvisualisierung:** Zeitreihen-Diagramm für systolische und diastolische Werte sowie Puls.
- **Histogramme:** Darstellung der Häufigkeit der Messwerte.
- **Tabellarische Darstellung:** Stilisiertes HTML-Layout der Daten mit farblicher Hervorhebung kritischer Werte.
- **PDF-Generierung:** Umwandlung der HTML-Tabelle in ein PDF-Dokument.

## Voraussetzungen

- Python 3.x
- Bibliotheken: `pandas`, `matplotlib`, `numpy`, `weasyprint`

Installiere die benötigten Pakete:

```sh
pip install pandas matplotlib numpy weasyprint