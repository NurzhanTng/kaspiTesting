# Kaspi Terminal Payment Tracker Bot

**Kaspi Terminal Payment Tracker Bot** is an automation tool designed to track the presence of Kaspi terminals using a camera. Once a terminal is detected, the bot updates the payment link for the user, enabling online payments even when there are limitations imposed by the Kaspi bank's system. This bot provides a seamless solution for making payments online without requiring physical interaction with the terminal.

## Key Features
- **Terminal Detection**: Uses computer vision to detect Kaspi terminals in the camera feed.
- **Payment Link Update**: Automatically updates the payment link for the user when a terminal is detected.
- **Bypass Kaspi Bank Limitations**: Allows users to perform online payments despite the bank's restrictions.
- **Real-time Monitoring**: Monitors the camera feed in real-time and provides instant updates.
- **Error Handling**: Ensures reliable performance even in fluctuating network conditions or camera issues.

## Tech Stack
- **Python Libraries**:
  - **aiohttp**: Asynchronous HTTP client/server framework.
  - **opencv-python**: OpenCV library for computer vision tasks.
  - **pyzbar**: Barcode and QR code reading for terminal identification.
  - **numpy**: Numerical operations to support computer vision algorithms.
  - **aiohappyeyeballs**: Asynchronous operations for handling camera input and detection.
  - **marshmallow**: Serialization and deserialization of data.
  - **python-dotenv**: Environment variable management.
- **Backend**:
  - **Asynchronous processing** with **aiohttp** for non-blocking, real-time operations.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NurzhanTng/Kaspi-Tracker-Bot.git
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file and specify the necessary variables for the bot’s operation. You may need camera-related configurations and Kaspi bank API credentials.

4. Run the bot:
   ```bash
   python main.py
   ```

5. The bot will start monitoring the camera feed for Kaspi terminals and automatically update payment links when a terminal is detected.


## Links
- [Русская версия README.md](./README.ru.md)

---

**Kaspi Terminal Payment Tracker Bot** is open-source and free to use. Contributions are always welcome! If you find any issues or have ideas for new features, feel free to create an issue or submit a pull request.


