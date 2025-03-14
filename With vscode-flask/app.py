import bme680
import time
import sys
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

def read_bme680():
    """
    Reads sensor data from the BME680 sensor.
    """
    try:
        # Default address: 0x76 (I2C_ADDR_PRIMARY)
        sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
    except (RuntimeError, IOError) as e:
        print(f"Failed to initialize sensor: {e}")
        sys.exit(1)


    # Set oversampling settings for measurement quality
    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)
    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)


    # Attempt to read sensor data
    if sensor.get_sensor_data():
        # Get the current time (e.g., "14:35")
        current_time = datetime.now().strftime('%H:%M')
        data = {
            'time': current_time,
            'temperature': f"{sensor.data.temperature:.2f}",
            'humidity': f"{sensor.data.humidity:.2f}",
            'pressure': f"{sensor.data.pressure:.2f}",
            'gas_resistance': f"{sensor.data.gas_resistance:.2f}"
        }
        return data
    else:
        print("No data from sensor!")
        sys.exit(1)


@app.route('/')
def index():
    sensor_data = read_bme680()
    return render_template('index.html', sensor=sensor_data)


if __name__ == '__main__':
    # Run the Flask web server on all interfaces at port 5000
    app.run(host='0.0.0.0', port=5000)
