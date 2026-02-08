import os
import subprocess
from PySide6 import QtWidgets, QtCore
import sys
import time

# Create the main application
input_dir = "Input"
output_dir = "Output"
app = QtWidgets.QApplication(sys.argv)

# Define the function that will be executed when the button is pressed
def on_start_button_clicked():
    # Create the directories if they don't exist
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Get selected encoder
    selected_encoder = encoder_combo.currentText()
    
    # Loop through all files in the input directory
    for filename in os.listdir(input_dir):
        # Check if the file is a .webm file
        if filename.endswith(".webm"):
            # Define the full path to the input and output files
            input_path = os.path.join(input_dir, filename)
            output_filename = filename.replace(".webm", ".mp4")
            output_path = os.path.join(output_dir, output_filename)
           
            # Construct the ffmpeg command based on selected encoder
            if selected_encoder == "NVIDIA GPU (h264_nvenc)":
                ffmpeg_command = [
                    "ffmpeg",
                    "-i", input_path,
                    "-c:v", "h264_nvenc",
                    "-preset", "fast",
                    "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                    output_path
                ]
            elif selected_encoder == "AMD GPU (h264_amf)":
                ffmpeg_command = [
                    "ffmpeg",
                    "-i", input_path,
                    "-c:v", "h264_amf",
                    "-quality", "speed",
                    "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                    output_path
                ]
            elif selected_encoder == "Intel GPU (h264_qsv)":
                ffmpeg_command = [
                    "ffmpeg",
                    "-i", input_path,
                    "-c:v", "h264_qsv",
                    "-preset", "fast",
                    "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                    output_path
                ]
            else:  # CPU encoding (default)
                ffmpeg_command = [
                    "ffmpeg",
                    "-i", input_path,
                    "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                    output_path
                ]
           
            # Run the ffmpeg command
            try:
                subprocess.run(ffmpeg_command, check=True)
                # Wait a moment to ensure file is released
                time.sleep(0.5)
                # Try to remove the file with retries
                for attempt in range(3):
                    try:
                        os.remove(input_path)
                        break
                    except PermissionError:
                        time.sleep(1)  # Wait longer and try again
                        if attempt == 2:  # Last attempt failed
                            print(f"Warning: Could not delete {filename} - file may be in use")
                            
            except subprocess.CalledProcessError:
                print(f"Error converting {filename}, trying CPU encoding...")
                # Fallback to CPU encoding if GPU fails
                ffmpeg_command = [
                    "ffmpeg",
                    "-i", input_path,
                    "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                    output_path
                ]
                subprocess.run(ffmpeg_command, check=True)
                # Wait and try to remove with retries
                time.sleep(0.5)
                for attempt in range(3):
                    try:
                        os.remove(input_path)
                        break
                    except PermissionError:
                        time.sleep(1)
                        if attempt == 2:
                            print(f"Warning: Could not delete {filename} - file may be in use")
                
    print("Conversión completada.")

# Create the main window
window = QtWidgets.QWidget()
window.setWindowTitle('WEBM to MP4 Converter')
window.setFixedSize(400, 350)

# Create the layout
layout = QtWidgets.QVBoxLayout()

# Add encoder selection
encoder_label = QtWidgets.QLabel('Select Encoder:')
encoder_combo = QtWidgets.QComboBox()
encoder_combo.addItems([
    "CPU (libx264) - Default",
    "NVIDIA GPU (h264_nvenc)",
    "AMD GPU (h264_amf)", 
    "Intel GPU (h264_qsv)"
])

# Create the start button
start_button = QtWidgets.QPushButton('Start')

# Connect the button's clicked signal to the function
start_button.clicked.connect(on_start_button_clicked)

# Add widgets to layout
layout.addStretch(1)
layout.addWidget(encoder_label, alignment=QtCore.Qt.AlignCenter)
layout.addWidget(encoder_combo, alignment=QtCore.Qt.AlignCenter)
layout.addStretch(1)
layout.addWidget(start_button, alignment=QtCore.Qt.AlignCenter)
layout.addStretch(1)

# Set the layout on the window
window.setLayout(layout)

# Show the window
window.show()

# Run the application's event loop
sys.exit(app.exec())