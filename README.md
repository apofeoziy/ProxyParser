# ProxyParser

This Python script is designed for automatic collection and validation of HTTP/HTTPS proxy servers.

## Key Parameters

The script settings are defined through constants at the beginning of the file:

*   `API_URL`: Base URL for fetching proxy lists.
*   `DAYS_BACK`: Number of past days from which proxies will be requested.
*   `TIMEOUT`: Maximum response wait time for a proxy server during validation (in seconds).
*   `TEST_URL`: URL used to test proxy functionality.
*   `MAX_WORKERS`: Maximum number of threads used for parallel proxy validation.
*   `PROXY_FILE`: Name of the file where working proxies will be saved.

## Dependencies

The script uses the following external libraries:

*   `requests`: for making HTTP requests.
*   `rich`: for formatted console output (tables, progress bars, colors).

Make sure these libraries are installed in your Python environment.

## Installation

1.  Clone the repository (if available) or simply download the file `proxy.py`.
    ```bash
    git clone https://github.com/apofeoziy/ProxyParser
    ```
2.  Install the required packages:

    ```bash
    pip install requests rich
    ```

## Usage

To run the script, execute the following command in your terminal from the script’s directory:

```bash
python proxy.py
```

After the script finishes, working proxy servers will be saved to the file specified in the `PROXY_FILE` variable (default is `proxy.txt`). 
