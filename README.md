# Sonic Symbiosis

**AI-powered platform that generates therapeutic soundscapes from plant bioacoustic data**

Sonic Symbiosis bridges the gap between nature and technology by creating personalized therapeutic audio experiences based on real-time plant bioacoustic signals. This innovative platform combines IoT sensors, AI-driven sound synthesis, and therapeutic audio principles to deliver unique wellness experiences.

## 🌟 Features

- **Real-time Plant Monitoring**: Connect to multiple plants via IoT sensors to capture bioacoustic data
- **AI-Powered Sound Generation**: Advanced algorithms create therapeutic tones based on plant health and environmental factors
- **Personalized Therapy Sessions**: Customizable sessions based on user mood, goals, and plant selection
- **Live Soundscape Streaming**: WebSocket-powered real-time audio visualization and streaming
- **Analytics Dashboard**: Track therapy effectiveness, stress reduction, and plant-human synchronization
- **Multi-Plant Garden**: Support for various plant species with different acoustic signatures

## 🛠️ Technology Stack

- **Backend**: Python, FastAPI, WebSockets
- **AI/ML**: TensorFlow, NumPy, Librosa for audio processing
- **Database**: PostgreSQL with TimescaleDB for time-series data
- **Hardware**: Arduino/Raspberry Pi for IoT sensors
- **Frontend**: HTML5, CSS3, JavaScript, Web Audio API
- **Real-time**: WebSocket connections for live data streaming

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL database (optional for full functionality)
- Audio output device
- IoT sensors (Arduino/Raspberry Pi) for real plant data (optional - demo mode available)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/sonic-symbiosis.git
   cd sonic-symbiosis
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional)
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and API keys
   ```

5. **Initialize the database** (optional)
   ```bash
   # If using PostgreSQL
   python -c "from app import create_tables; create_tables()"
   ```

## 🎵 Usage

1. **Start the server**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Open your browser**
   Navigate to `http://localhost:8000`

3. **Start a therapy session**
   - Select your current mood and therapy goal
   - Choose session duration (5-60 minutes)
   - Click "Start Therapy Session"
   - Enjoy the AI-generated soundscape based on your connected plants

4. **Monitor your session**
   - Watch the live soundwave visualization
   - Track real-time analytics including stress reduction and focus improvement
   - End the session when complete

## 🌱 Plant Setup (Optional)

For real plant data integration:

1. **Hardware Setup**
   - Connect soil moisture sensors to Arduino/Raspberry Pi
   - Set up temperature and humidity sensors
   - Configure WiFi connectivity for data transmission

2. **Sensor Configuration**
   - Update plant sensor endpoints in the configuration
   - Calibrate sensors for your specific plant types
   - Test data transmission to the platform

## 📊 API Endpoints

- `GET /` - Main application interface
- `GET /api/plants` - List connected plants
- `POST /api/therapy/start` - Start therapy session
- `DELETE /api/therapy/{session_id}` - End therapy session
- `GET /api/soundscape/{session_id}` - Get soundscape data
- `WS /ws/live-soundscape/{session_id}` - Live soundscape streaming
- `GET /api/analytics/{session_id}` - Session analytics

## 🧪 Demo Mode

The platform includes a demo mode with simulated plant data for testing without physical sensors:

- Simulated plant health metrics
- Generated bioacoustic patterns
- Realistic therapy session analytics
- Multiple virtual plant species

## 🔬 How It Works

1. **Data Collection**: IoT sensors monitor plant health metrics (soil moisture, temperature, growth patterns)
2. **Signal Processing**: Raw sensor data is converted into bioacoustic signatures using AI algorithms
3. **Sound Synthesis**: Therapeutic tones are generated based on plant data and user preferences
4. **Real-time Streaming**: Soundscapes are delivered via WebSocket for immediate playback
5. **Analytics**: User response and plant correlation data is analyzed for session effectiveness

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by research in plant bioacoustics and music therapy
- Built with love for the intersection of nature, technology, and wellness
- Special thanks to the open-source audio processing and IoT communities

## 📞 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Join our community discussions
- Check out our documentation wiki

---

**Experience the harmony between nature and technology with Sonic Symbiosis** 🌱🎵