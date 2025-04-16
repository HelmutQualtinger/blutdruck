# Dokumentation: Blutdruckanalyse-Skript

## Übersicht

Dieses Skript analysiert und visualisiert Blutdruck- und Pulsmessdaten aus einer CSV-Datei. Es erstellt Diagramme, berechnet Mittelwerte, generiert eine formatierte Tabelle und speichert die Ergebnisse in verschiedenen Dateiformaten (PDF, PNG, HTML). Zusätzlich werden die generierten Dateien automatisch im Browser geöffnet.

---

## Funktionen

### 1. **Datenvorbereitung**
- **Eingabedatei:** `puls_data.csv`
- Die Spalten `Datum` und `Uhrzeit` werden kombiniert und in ein `datetime`-Objekt umgewandelt, um Zeitreihenanalysen zu ermöglichen.
- Ein separater DataFrame (`table_df`) wird für die tabellarische Darstellung erstellt.

### 2. **Visualisierung**
#### Zeitreihendiagramm
- **Darstellung:** Systolischer und diastolischer Blutdruck sowie Puls über die Zeit.
- **Hervorhebungen:**
  - Referenzlinien bei 80, 90, 120 und 140 mmHg.
  - Farbige Bereiche für normale Werte (80–90 mmHg und 120–140 mmHg).

#### Histogramme
- **Darstellung:** Verteilung der systolischen, diastolischen Werte und des Pulses.
- **Hervorhebungen:**
  - Vertikale Linien und Textbeschriftungen für Mittelwerte.
  - Referenzlinien für normale Wertebereiche.

### 3. **Tabellarische Darstellung**
- **Formatierung:** Kritische Werte werden farblich hervorgehoben:
  - Systolisch ≥ 140 mmHg.
  - Diastolisch ≥ 90 mmHg.
- **Speicherung:** Tabelle wird als HTML-Datei gespeichert.

### 4. **PDF-Generierung**
- **Diagramme:** Zeitreihen- und Histogramm-Diagramme werden als PDF und PNG gespeichert.
- **Tabelle:** HTML-Tabelle wird mit benutzerdefiniertem CSS in ein PDF-Dokument umgewandelt:
  - Querformat.
  - Drei Spalten.
  - Angepasste Schriftgröße.

### 5. **Automatisches Öffnen der Dateien**
- Die generierten Dateien (HTML, PDF, PNG) werden automatisch im Safari-Browser geöffnet.

---

## Abhängigkeiten

- **Python-Version:** 3.x
- **Benötigte Bibliotheken:**
  - `pandas`
  - `matplotlib`
  - `numpy`
  - `weasyprint`

### Installation der Bibliotheken
```bash
pip install pandas matplotlib numpy weasyprint
