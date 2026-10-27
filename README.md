# Sonic Symbiosis

A FastAPI prototype that turns **simulated plant readings** into synthesized tones and audio-feature visualizations. It uses three virtual plants, NumPy for harmonic signals, librosa for features, and an HTML/JavaScript frontend.

There is no implemented sensor connection, trained AI model or measured therapeutic outcome in this repository.

## What the code does

1. Generates random moisture, temperature, humidity, growth and stress values.
2. Builds a two-second signal from plant-type frequencies, adjusted by the simulated moisture, stress and selected mood.
3. Calculates spectral-centroid and MFCC summaries.
4. Returns those summaries through HTTP and a WebSocket handler for visualization.

Sessions live in memory. The browser draws a waveform representation from the features; it does not play or receive the synthesized audio samples. The values named `therapeutic_score`, stress reduction, focus improvement and satisfaction are random placeholders, **not health measurements**.

## Local development

```bash
git clone https://github.com/Zinga18018/sonic-symbiosis.git
cd sonic-symbiosis
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdir static
uvicorn app:app --host 127.0.0.1 --port 8000
```

On Windows, activate with `.venv\Scripts\activate`. The empty `static` directory is required by the app's static-files mount but is not tracked. The dependency list includes packages unused by the current app; installation and end-to-end operation have not been revalidated.

**Known live-update issue:** the WebSocket handler passes a Python `datetime` from the plant model to `json.dumps` without conversion. That path needs correction before claiming working live updates. Creating `static` does not fix this separate issue.

## Source and endpoints

- [app.py](app.py): simulation, tone generation, session routes and WebSocket handler.
- [templates/index.html](templates/index.html): plant selection and SVG visualization.
- `GET /api/plants`, `POST /api/therapy/start`, `DELETE /api/therapy/{session_id}`.
- `GET /api/soundscape/{session_id}`, `GET /api/analytics/{session_id}`, `WS /ws/live-soundscape/{session_id}`.

There is no database integration, sensor configuration, clinical evaluation or test suite in the checked source. This is a signal-processing demo, not a therapy tool. Any future plot should label simulated inputs and avoid presenting the placeholder scores as evidence.

## License and acknowledgments

[MIT License](LICENSE), with the existing Sonic Symbiosis copyright notice.

The original inspiration was plant bioacoustics and music therapy, at the intersection of nature, technology and wellness. Thanks to the open-source audio-processing and IoT communities. Those inspirations are not evidence of an implemented sensor system or therapeutic benefit. Issues and pull requests are welcome.
