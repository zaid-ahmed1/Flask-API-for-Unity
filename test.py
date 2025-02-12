from flask import Flask, request, jsonify
import numpy as np
from flask_cors import CORS
import pyautogui
import os
from datetime import datetime
import pygetwindow as gw
import time

app = Flask(__name__)
CORS(app)  # This allows Unity to make requests to the API

# Create directory for screenshots if it doesn't exist
SCREENSHOT_DIR = "analyze_screen"
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        print("Received request headers:", dict(request.headers))
        print("Received raw data:", request.get_data(as_text=True))
        
        data = request.get_json()
        if data is None:
            return jsonify({'success': False, 'error': 'No JSON data received'}), 400
            
        print("Parsed JSON data:", data)
            
        numbers = data.get('numbers', [])
        if not numbers:
            return jsonify({'success': False, 'error': 'No numbers provided'}), 400
            
        # Print received data for debugging
        print(f"Received numbers: {numbers}")
        
        # Check if numbers is empty or contains invalid data
        if len(numbers) == 0:
            return jsonify({'success': False, 'error': 'Empty array received'}), 400
        
        # Using numpy for calculations (as an example of using Python packages)
        result = {
            'mean': float(np.mean(numbers)),
            'sum': float(np.sum(numbers)),
            'max': float(np.max(numbers))
        }
        
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        print(f"Error in calculate: {str(e)}")  # Debug print
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/process_text', methods=['POST'])
def process_text():
    try:
        print("Received request headers:", dict(request.headers))
        print("Received raw data:", request.get_data(as_text=True))
        
        data = request.get_json()
        print("Parsed JSON data:", data)
        
        text = data.get('text', '')
        
        # Simple text processing example
        result = {
            'word_count': len(text.split()),
            'char_count': len(text),
            'uppercase': text.upper()
        }
        
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        print(f"Error in process_text: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/analyze_screen', methods=['POST'])
@app.route('/analyze_screen', methods=['POST'])
def analyze_screen():
    try:
        data = request.get_json()
        window_title = data.get('window_title', '')
        
        print(f"Attempting to capture window with title: '{window_title}'")
        
        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        
        if window_title:
            # Try to find window
            windows = gw.getWindowsWithTitle(window_title)
            if not windows:
                print(f"No windows found with title: {window_title}")
                return jsonify({
                    'success': False,
                    'error': f'Window with title "{window_title}" not found'
                }), 404
            
            window = windows[0]
            print(f"Found window: {window.title}")
            
            # Try to activate window, if fails use minimize/maximize/restore workaround
            try:
                window.activate()
                print("Window activated normally")
            except:
                print("Normal activation failed, trying workaround...")
                window.minimize()
                time.sleep(0.2)
                window.maximize()
                time.sleep(0.2)
                window.restore()
                time.sleep(0.2)
                print("Workaround completed")
            
            # Take screenshot of the window
            try:
                screenshot = pyautogui.screenshot(region=(
                    window.left,
                    window.top,
                    window.width,
                    window.height
                ))
                print(f"Screenshot captured: {screenshot.size}")
            except Exception as capture_error:
                print(f"Error capturing window: {capture_error}")
                print("Falling back to full screen capture")
                screenshot = pyautogui.screenshot()
        else:
            print("No window title provided, capturing full screen")
            screenshot = pyautogui.screenshot()
        
        # Save the screenshot
        screenshot.save(filepath)
        print(f"Screenshot saved to: {filepath}")
        
        return jsonify({
            'success': True,
            'result': {
                'filename': filename,
                'filepath': filepath,
                'timestamp': timestamp,
                'window_title': window_title if window_title else 'full_screen',
                'size': {'width': screenshot.size[0], 'height': screenshot.size[1]}
            }
        })
            
    except Exception as e:
        print(f"General error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/list_windows', methods=['GET'])
def list_windows():
    try:
        # Get all windows and their titles
        windows = []
        for win in gw.getAllWindows():
            if win.title:  # Only include windows with non-empty titles
                windows.append({
                    'title': win.title,
                    'active': win.isActive,
                    'visible': win.visible,
                    'minimized': win.isMinimized
                })
        
        return jsonify({
            'success': True,
            'result': {
                'windows': windows
            }
        })
    except Exception as e:
        print(f"Error listing windows: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
