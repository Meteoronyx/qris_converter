
## Overview

This BOT is to convert Static QRIS to Dynamic QRIS with a certain nominal value using the Telegram Bot
<a href="https://gifyu.com/image/bLVm7"><img src="https://s4.gifyu.com/images/bLVm7.gif" alt="WhatsApp Video 2025 05 06 at 14.12.01 d865cce7" border="0" /></a>


## Requirements

*   Python 3.6+
*   Telegram Bot API token
*   Required Python packages (install using `pip install -r requirements.txt`)

## Setup

1.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Environment Variables:**

    *   Create a `.env` file based on `.env.example`.
    *   Set the `TELEGRAM_BOT_TOKEN` variable with your Telegram Bot API token.

3.  **Run the Bot:**

    ```bash
    python bot.py
    ```

## Usage

1.  Start the bot in Telegram.
2.  Use the available commands (e.g., `/start`, `/15000`).
3.  Follow the bot's instructions to generate a QRIS code.

## Functionality

*   **`/start`**:  Starts the bot and displays a welcome message.
*   **`/generate_qris`**: Initiates the QRIS code generation process.  The bot will likely prompt you for information such as the amount, recipient, or other relevant details needed to create the QRIS code.

## Contributing

Feel free to contribute to this project by submitting pull requests.
