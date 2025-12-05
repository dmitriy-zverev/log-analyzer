# Nginx Log Analyzer

A Python application for analyzing Nginx access logs and generating HTML reports with request statistics grouped by URL.

## Overview

This tool processes Nginx log files in the `ui_short` format, extracts request information, calculates comprehensive statistics for each URL endpoint, and generates interactive HTML reports for performance analysis.

## Features

### Implemented Functionality

- **Multi-format Log Support**: Processes both plain text (`.log`) and gzip-compressed (`.gz`) log files
- **Regex-based Parsing**: Extracts detailed information from each log line including:
  - Remote address and user information
  - Timestamp and request details (method, URL, HTTP version)
  - Response status and body size
  - Request time for performance analysis
  - Various HTTP headers (referer, user agent, X-headers)
  
- **URL-based Aggregation**: Groups all requests by URL endpoint for consolidated analysis

- **Statistical Analysis**: Calculates comprehensive metrics for each URL:
  - `count`: Total number of requests to the URL
  - `count_perc`: Percentage of requests (relative to all requests)
  - `time_sum`: Total time spent processing requests
  - `time_perc`: Percentage of total processing time
  - `time_avg`: Average request processing time
  - `time_max`: Maximum request processing time
  - `time_med`: Median request processing time

- **Structured Logging**: Uses `structlog` for JSON-formatted structured logging with ISO timestamps

- **HTML Report Generation**: Creates interactive HTML reports with sortable tables for easy data exploration

- **Batch Processing**: Processes all log files matching the configured pattern in one run

## Technical Stack

- **Python**: 3.11+
- **Dependencies**:
  - `structlog` - Structured logging library
  - `ruff` - Fast Python linter and formatter
  - `pre-commit` - Git pre-commit hooks framework
- **Package Management**: uv
- **Linting & Formatting**: Ruff with 120 character line length

## Configuration

The application uses a configuration dictionary with the following parameters:

```python
config = {
    "REPORT_SIZE": 1000,              # Maximum number of URLs in report
    "REPORT_DIR": "../reports",        # Directory for output reports
    "LOG_DIR": "../log",               # Directory containing log files
    "LOG_FILE_NAME": "nginx-access-ui", # Log file name prefix
    "TIME_FORMAT": "%d/%b/%Y:%H:%M:%S %z",  # Timestamp parsing format
    "REPORT_REPLACE_STRING": "$table_json",  # Placeholder in HTML template
}
```

## Expected Log Format

The analyzer expects Nginx logs in the following format:

```
log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
                    '$request_time';
```

## Usage

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Place your Nginx log files in the configured `LOG_DIR` directory

3. Run the analyzer:
```bash
cd homework/log_analyzer
python log_analyzer.py
```

4. Find generated reports in the `REPORT_DIR` directory with filenames like `report-YYYYMMDD.html`

## Project Structure

```
homework/
├── log_analyzer/
│   ├── __init__.py
│   └── log_analyzer.py       # Main analyzer logic
├── log/                       # Input log files directory
├── reports/                   # Generated HTML reports
│   ├── report.html           # HTML template
│   ├── jquery.tablesorter.min.js  # Table sorting JavaScript
│   └── report-*.html         # Generated reports
├── tests/
│   └── tests.py              # Test suite (placeholder)
├── docs/
│   └── homework.pdf          # Assignment description
├── pyproject.toml            # Project configuration
├── requirements.txt          # Python dependencies
├── .pre-commit-config.yaml   # Pre-commit hooks
├── makefile                  # Build automation
└── README.md                 # This file
```

## Development

### Code Quality Tools

- **Ruff**: Configured for linting and formatting
- **Pre-commit**: Automated code quality checks before commits

### Run Linting

```bash
make lint
# or
ruff check .
```

### Format Code

```bash
ruff format .
```

## Areas for Improvement

### Critical

1. **Error Handling**: 
   - Add try-catch blocks for file operations
   - Handle malformed log lines gracefully
   - Validate parsed data before processing
   - Check for missing or corrupted files

2. **Testing**:
   - Implement unit tests for parsing logic
   - Add integration tests for full workflow
   - Test edge cases (empty files, malformed data, etc.)
   - Add test coverage reporting

3. **Bug Fixes**:
   - Fix `time_max` calculation (currently uses minimum from sorted list instead of maximum)
   - Validate date parsing from filename
   - Check if report already exists before overwriting

### High Priority

4. **Configuration Management**:
   - Support external configuration files (YAML/JSON)
   - Add command-line argument parsing (argparse)
   - Support environment variables for deployment flexibility
   - Validate configuration values

5. **Code Quality**:
   - Add type hints for better IDE support and error prevention
   - Add comprehensive docstrings for functions and modules
   - Remove global variable `all_logs` (use return values or class-based approach)
   - Split large `main()` function into smaller testable units

6. **Logging Improvements**:
   - Log parsing errors with problematic line content
   - Add progress indicators for large file processing
   - Separate error logs from info logs
   - Add log levels configuration

### Medium Priority

7. **Performance Optimization**:
   - Stream processing for large files (don't load all into memory)
   - Parallel processing of multiple log files
   - Add progress bars for long-running operations
   - Optimize regex compilation (compile once, reuse)

8. **Feature Enhancements**:
   - Support for additional Nginx log formats
   - Configurable report size limits
   - Export to multiple formats (JSON, CSV, etc.)
   - Date range filtering
   - Status code analysis
   - Response size analysis

9. **Reporting**:
   - Add charts/visualizations (e.g., using Chart.js)
   - Summary statistics in report header
   - Timestamp your reports with generation time
   - Support for custom report templates

### Low Priority

10. **User Experience**:
    - Better CLI interface with help messages
    - Verbose/debug mode options
    - Dry-run mode to preview operations
    - Summary output to console

11. **CI/CD**:
    - GitHub Actions workflow
    - Automated testing on push
    - Code coverage enforcement
    - Docker containerization

12. **Documentation**:
    - API documentation (Sphinx)
    - Example log files for testing
    - Troubleshooting guide
    - Performance benchmarks

## License

This project is part of an educational assignment.

## Author

OTUS Python Pro Course - Homework Assignment
