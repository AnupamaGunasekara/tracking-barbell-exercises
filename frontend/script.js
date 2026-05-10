// Initialize charts
let accelerometerChart, gyroscopeChart;

// Generate random data for charts
function generateChartData(length = 50) {
    return Array.from({ length }, () => ({
        x: Math.random() * 10,
        y: (Math.random() - 0.5) * 10,
        z: (Math.random() - 0.5) * 10
    }));
}

// Initialize Accelerometer Chart
function initAccelerometerChart() {
    const ctx = document.getElementById('accelerometerChart').getContext('2d');
    const data = generateChartData();
    
    accelerometerChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({ length: data.length }, (_, i) => i / 5),
            datasets: [{
                label: 'X',
                data: data.map(d => d.x),
                borderColor: '#00d4ff',
                backgroundColor: 'transparent',
                borderWidth: 2,
                pointRadius: 0,
                tension: 0.4
            }, {
                label: 'Y',
                data: data.map(d => d.y),
                borderColor: '#ff9900',
                backgroundColor: 'transparent',
                borderWidth: 2,
                pointRadius: 0,
                tension: 0.4
            }, {
                label: 'Z',
                data: data.map(d => d.z),
                borderColor: '#aa00ff',
                backgroundColor: 'transparent',
                borderWidth: 2,
                pointRadius: 0,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#888',
                        font: {
                            size: 10
                        }
                    },
                    title: {
                        display: true,
                        text: 'Time (s)',
                        color: '#888',
                        font: {
                            size: 10
                        }
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#888',
                        font: {
                            size: 10
                        }
                    }
                }
            },
            animation: {
                duration: 1000
            }
        }
    });
}

// Initialize Gyroscope Chart
function initGyroscopeChart() {
    const ctx = document.getElementById('gyroscopeChart').getContext('2d');
    const data = generateChartData();
    
    gyroscopeChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({ length: data.length }, (_, i) => i / 5),
            datasets: [{
                label: 'X',
                data: data.map(d => d.x),
                borderColor: '#00d4ff',
                backgroundColor: 'transparent',
                borderWidth: 2,
                pointRadius: 0,
                tension: 0.4
            }, {
                label: 'Y',
                data: data.map(d => d.y),
                borderColor: '#ff9900',
                backgroundColor: 'transparent',
                borderWidth: 2,
                pointRadius: 0,
                tension: 0.4
            }, {
                label: 'Z',
                data: data.map(d => d.z),
                borderColor: '#aa00ff',
                backgroundColor: 'transparent',
                borderWidth: 2,
                pointRadius: 0,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#888',
                        font: {
                            size: 10
                        }
                    },
                    title: {
                        display: true,
                        text: 'Time (s)',
                        color: '#888',
                        font: {
                            size: 10
                        }
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#888',
                        font: {
                            size: 10
                        }
                    }
                }
            },
            animation: {
                duration: 1000
            }
        }
    });
}

// Update charts with new data (simulate real-time)
function updateCharts() {
    const newData = generateChartData();
    
    if (accelerometerChart) {
        accelerometerChart.data.datasets[0].data = newData.map(d => d.x);
        accelerometerChart.data.datasets[1].data = newData.map(d => d.y);
        accelerometerChart.data.datasets[2].data = newData.map(d => d.z);
        accelerometerChart.update('none');
    }
    
    if (gyroscopeChart) {
        gyroscopeChart.data.datasets[0].data = newData.map(d => d.x);
        gyroscopeChart.data.datasets[1].data = newData.map(d => d.y);
        gyroscopeChart.data.datasets[2].data = newData.map(d => d.z);
        gyroscopeChart.update('none');
    }
}

// Exercise selection
document.querySelectorAll('.exercise-icon').forEach(icon => {
    icon.addEventListener('click', function() {
        document.querySelectorAll('.exercise-icon').forEach(i => i.classList.remove('active'));
        this.classList.add('active');
        updateCharts();
    });
});

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initAccelerometerChart();
    initGyroscopeChart();
    
    // Update charts every 3 seconds to simulate real-time data
    setInterval(updateCharts, 3000);
});

// Add animation to sensor points
document.addEventListener('DOMContentLoaded', function() {
    const sensorPoints = document.querySelectorAll('.sensor-point');
    sensorPoints.forEach((point, index) => {
        point.style.animationDelay = `${index * 0.2}s`;
    });
});
