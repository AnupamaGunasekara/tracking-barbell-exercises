# Barbell Exercise Tracker - Frontend Dashboard

## Overview
Interactive ML-powered fitness tracking dashboard displaying real-time sensor data, model predictions, and performance metrics.

## Features
- **Live Sensor Analytics**: Real-time accelerometer and gyroscope data visualization
- **99.7% Model Accuracy**: Display of trained ML model performance
- **Confusion Matrix**: Visual representation of classification accuracy
- **Neural Network Visualization**: Interactive neural network architecture display
- **Exercise Selection**: Switch between 5 different barbell exercises
- **Performance Metrics**: Accuracy, Precision, Recall, and F1 Score

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Open `index.html` in your web browser:
```bash
# macOS
open index.html

# Or simply drag the file into your browser
```

## Usage

### Running Locally
Simply open `index.html` in any modern web browser. No server required!

### Viewing Live Data
The dashboard automatically updates with simulated sensor data every 3 seconds.

### Selecting Exercises
Click on any exercise icon (Bench Press, Squat, Deadlift, Row, Overhead Press) to see the corresponding data.

## Technologies Used
- **HTML5**: Structure and layout
- **CSS3**: Styling with gradients, animations, and responsive design
- **JavaScript (ES6+)**: Interactive functionality
- **Chart.js**: Real-time data visualization

## File Structure
```
frontend/
├── index.html      # Main HTML structure
├── styles.css      # All styling and animations
├── script.js       # Interactive functionality and charts
└── README.md       # This file
```

## Customization

### Connecting Real Data
To connect real sensor data from your ML model:

1. Edit `script.js` and replace the `generateChartData()` function with actual data fetching:
```javascript
async function fetchRealData() {
    const response = await fetch('YOUR_API_ENDPOINT');
    const data = await response.json();
    return data;
}
```

2. Update the metrics by modifying the HTML values or creating dynamic updates.

### Styling
All colors and styles can be customized in `styles.css`. Key variables:
- Primary color: `#00d4ff` (cyan)
- Secondary color: `#ff9900` (orange)
- Accent color: `#aa00ff` (purple)

## Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Performance
The dashboard is optimized for:
- Smooth 60fps animations
- Minimal CPU usage
- Responsive design (mobile & desktop)

## Future Enhancements
- [ ] WebSocket integration for real-time data
- [ ] Export reports as PDF
- [ ] Historical data comparison
- [ ] User authentication
- [ ] Mobile app version

## License
MIT License - Feel free to use for your projects!

## Contact
For questions or suggestions, please open an issue on GitHub.
