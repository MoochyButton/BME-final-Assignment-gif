import matplotlib.animation as animation
import matplotlib.pyplot as plt
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
num_steps = 10  # Number of steps to take for threshold calibration
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
    manager = SensorEmulator('PidisSpeedyPodi')
    # manager = SensorManager(sensor_names)
    # manager.set_sample_rate(sample_rate)
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
    return peaks, mean_impact_acceleration_tibia


def calibrate_threshold():
    """
    Calibrate the threshold based on mean impact accelerations.

    Returns:
        float: Calibrated threshold value or None if not enough data.
    """
    if len(mean_values) == num_steps:
        return np.mean(mean_values) + 0.5
    return None


def update_plot(i, manager, ax, sample_rate):
    """
    Update the plot with new accelerometer data and peaks.

    Args:
        i (int): Frame index for the animation.
        manager (SensorEmulator): Sensor manager instance.
        ax (matplotlib.axes.Axes): Matplotlib Axes object for plotting.
        sample_rate (int): Sample rate of the sensor data.
    """
    global threshold, above_threshold
    update_data(manager)
    vertical_acceleration = get_vertical_acceleration()
    peaks, mean_impact = find_peaks(vertical_acceleration, sample_rate)

    if threshold is None and len(mean_values) >= num_steps:
        threshold = calibrate_threshold()
        if threshold is None:
            threshold = -1  # Default value if calibration fails

    # Clear and update the plot
    ax.cla()
    ax.plot(vertical_acceleration)
    ax.scatter(peaks, vertical_acceleration[peaks], color='red')
    ax.set_title('Vertical (Y) Acceleration Data')
    ax.set_xlabel('Data point')
    ax.set_ylabel('Vertical Acceleration (m/s^2)')
    ax.set_ylim(y_axis_limits)

    # Plot the threshold line if calibrated
    if threshold is not None and threshold != -1:
        ax.axhline(y=threshold, color='green', linestyle='--', label=f'Threshold: {threshold:.2f}')
        ax.legend()

    # Set x-axis limits to show the entire data up to the current point
    ax.set_xlim(0, len(vertical_acceleration))

    # Check if the current vertical acceleration is above the threshold
    if threshold is not None and threshold != -1:
        above_threshold = vertical_acceleration[-1] > threshold
        if above_threshold:
            print(f"Above Threshold: {above_threshold}")
            osc_client.send_message("/threshold_exceeded", 1)  # Sending OSC message


def main():
    """
    Main function to initialize the sensor manager, set up the plot, and start the animation.
    """
    sensor_names = ['F672']
    sample_rate = 120
    interval = 1000 / sample_rate

    manager = initialize_sensor_manager(sensor_names, sample_rate)

    fig, ax = plt.subplots(1, 1)
    ani = animation.FuncAnimation(fig, update_plot, fargs=(manager, ax, sample_rate), interval=interval, cache_frame_data=False)

    plt.show()


if __name__ == '__main__':
    main()
