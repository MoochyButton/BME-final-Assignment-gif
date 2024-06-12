from pythonosc import dispatcher
from pythonosc import osc_server


# Define the function to handle received OSC messages
def threshold_handler(address, *args):
    print(f"Received message from {address}: {args}")


# Define the IP address and port for OSC server to listen on
OSC_IP = "0.0.0.0"  # Listen on all available network interfaces
OSC_PORT = 12345  # Port number to listen for OSC messages

# Create an OSC dispatcher
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/threshold_exceeded", threshold_handler)  # Map the OSC address to the handler function

# Create an OSC server
server = osc_server.ThreadingOSCUDPServer((OSC_IP, OSC_PORT), dispatcher)

# Start the OSC server to begin listening for messages
print(f"Listening for OSC messages on {OSC_IP}:{OSC_PORT}")
server.serve_forever()