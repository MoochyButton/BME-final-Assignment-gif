import numpy as np
from CreaTeBME import SensorManager, SensorEmulator
import scipy.signal as signal
from pythonosc import udp_client

# OSC settings
OSC_IP = "127.0.0.1"  # IP address of the OSC server
OSC_PORT = 12345  # Port number for OSC communication
# Initialize OSC client
osc_client = udp_client.SimpleUDPClient(OSC_IP, OSC_PORT)
# Global variables
peak_array = []  # Stores the peak values of vertical acceleration
impact_acceleration_tibia = []  # Stores the impact acceleration values for tibia
mean_values = []  # Stores mean impact accelerations for calibration
num_steps = 5  # Number of steps to take for threshold calibration
accelerometer_data = np.zeros((0, 3))  # Stores accelerometer data
threshold = None  # Threshold value for vertical acceleration peaks
window_size = 20  # Size of the visible window for plotting
above_threshold = False  # Flag indicating if the current value is above threshold

# Fixed y-axis limits
y_axis_limits = (-10, 10)  # Adjust these values based on expected data range

def initialize_sensor_manager(sensor_names, sample_rate):
    """
    Initialize the sensor manager with the given sensor names and sample rate.

    Args:
        sensor_names (list): List of sensor names to initialize.
        sample_rate (int): Sample rate for the sensors.

    Returns:
        SensorEmulator: Initialized sensor emulator instance.
    """
    # manager = SensorEmulator('PidisSpeedyPodi')
    manager = SensorManager(sensor_names)
    manager.set_sample_rate(sample_rate)
    manager.start()
    return manager

def get_sensor_measurements(manager):
    """
    Get the latest sensor measurements from the manager.

    Args:
        manager (SensorEmulator): Sensor manager instance.

    Returns:
        dict: Dictionary of sensor data.
    """
    measurements = manager.get_measurements()
    sensor_data = {sensor: data for sensor, data in measurements.items() if data}
    return sensor_data

def update_data(manager):
    """
    Update the global accelerometer data with the latest sensor measurements.

    Args:
        manager (SensorEmulator): Sensor manager instance.
    """
    global accelerometer_data
    measurements = get_sensor_measurements(manager)
    for sensor, data in measurements.items():
        accelerometer_data = np.vstack((accelerometer_data, data[0][:3]))

def get_vertical_acceleration():
    """
    Extract the vertical (Y-axis) acceleration from the accelerometer data.

    Returns:
        np.ndarray: Array of vertical acceleration values.
    """
    return accelerometer_data[:, 1]

def find_peaks(vertical_acceleration, sample_rate):
    """
    Find peaks in the vertical acceleration data and calculate the mean impact acceleration.

    Args:
        vertical_acceleration (np.ndarray): Array of vertical acceleration values.
        sample_rate (int): Sample rate of the sensor data.

    Returns:
        tuple: Peaks indices and mean impact acceleration.
    """
    peaks, properties = signal.find_peaks(vertical_acceleration, height=2, distance=sample_rate / 2)
    mean_impact_acceleration_tibia = np.mean(properties['peak_heights'])
    if mean_impact_acceleration_tibia > 1 and mean_impact_acceleration_tibia not in mean_values and len(mean_values) < num_steps:
        mean_values.append(mean_impact_acceleration_tibia)
    return peaks

def calibrate_threshold():
    """
    Calibrate the threshold based on mean impact accelerations.

    Returns:
        float: Calibrated threshold value or None if not enough data.
    """
    if len(mean_values) == num_steps:
        return np.mean(mean_values) + 0.5
    return None

def main(input_queue = None):
    """
    Main function to initialize the sensor manager, set up the plot, and start the animation.
    """
    sensor_names = ['F672']
    sample_rate = 120

    manager = initialize_sensor_manager(sensor_names, sample_rate)

    potential = False
    count = 0
    prev_len: int = 0

    while True:
        global threshold        # no global
        update_data(manager)
        vertical_acceleration = get_vertical_acceleration()
        peaks = find_peaks(vertical_acceleration, sample_rate)

        if threshold is None and len(mean_values) >= num_steps:
            threshold = calibrate_threshold()
            if threshold is None:
                threshold = -1  # Default value if calibration fails

        if prev_len < vertical_acceleration[peaks].size:
            potential = True

        # Check if the current vertical acceleration is above the threshold
        if threshold is not None:
            if vertical_acceleration[peaks][-1] > threshold and potential:
                potential = False
                if input_queue:
                    input_queue.put(True)
                print(count := count + 1)
                print(threshold)
                print(vertical_acceleration[peaks])
                print(f"Above Threshold")

        prev_len = vertical_acceleration[peaks].size


if __name__ == '__main__':
    main()