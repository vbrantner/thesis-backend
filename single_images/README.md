# README

## Projektübersicht

Dieses Projekt dient dazu, einen Stream von Einzelbildern zu erzeugen. Zur Aufnahme wird OpenCV verwendet. Für Übertragung werden WebSocket und Flask (ein HTTP-Webserver) verwendet.

## Systemvoraussetzungen

- Python 3.x
- Betriebssystem: Linux

## Installation

Zur Installation der erforderlichen Pakete und Libraries führen Sie den folgenden Befehl im Hauptverzeichnis des Projekts aus:

```bash
pip install -r requirements.txt
```

Dies wird alle benötigten Abhängigkeiten installieren, die in der `requirements.txt`-Datei aufgeführt sind.

## Dateibeschreibung

- `single_images_yield.py`: [Verwendet HTTP-Stream]
- `single_images_ws.py`: [Verwendet WebSocket]

## Ausführung der Skripte

Um ein Skript auszuführen, navigieren Sie im Terminal oder in der Kommandozeile zum Projektverzeichnis und verwenden Sie den folgenden Befehl:

```bash
python [Skriptname].py
```

Ersetzen Sie `[Skriptname]` durch den tatsächlichen Namen des Skripts, das Sie ausführen möchten.

## Weiterführende Informationen

Für detailliertere Informationen zu den einzelnen Skripten, einschließlich spezifischer Funktionen und Optionen, lesen Sie bitte die Kommentare und die Dokumentation innerhalb der Skripte selbst.
