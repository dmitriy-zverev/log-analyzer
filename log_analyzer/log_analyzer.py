# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';
import gzip
import os
import re
from collections import defaultdict
from datetime import datetime

import structlog

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "../reports",
    "LOG_DIR": "../log",
    "LOG_FILE_NAME": "nginx-access-ui",
    "TIME_FORMAT": "%d/%b/%Y:%H:%M:%S %z",
}

logger = structlog.get_logger()


def get_log_files():
    return [
        os.path.join(config["LOG_DIR"], f)
        for f in os.listdir(config["LOG_DIR"])
        if os.path.isfile(os.path.join(config["LOG_DIR"], f)) and f.startswith(config["LOG_FILE_NAME"])
    ]


def get_log_data(log_file):
    if log_file.endswith(".gz"):
        with gzip.open(log_file, "rb") as f:
            return str(gzip.decompress(f.read())).split("b'")[1].split("\\n")
    with open(log_file, "rb") as f:
        return str(f.read()).split("b'")[1].split("\\n")


def extract_data(log_line):
    pattern = r"(\S+)\s+(\S+)\s+(\S+)\s+\[(.*?)\]\s+\"(.*?)\"\s+(\d+)\s+(\d+)\s+\"(\S+)\"\s+\"(.*?)\"\s+\"(.*?)\"\s+\"(.*?)\"\s+\"(.*?)\"\s+(\d+\.\d+)"

    match = re.match(pattern, log_line)
    if match:
        request = match.group(5)
        parts = request.split()

        if len(parts) == 3:
            http_method, url, http_version = parts
        else:
            http_method, url, http_version = parts[0] if parts else "-", "-", "-"

        return {
            "remote_addr": match.group(1),
            "remote_user": match.group(2),
            "http_x_real_ip": match.group(3),
            "time_local": datetime.strptime(match.group(4), config["TIME_FORMAT"]),
            "request": request,
            "http_method": http_method,
            "url": url,
            "http_version": http_version,
            "status": int(match.group(6)),
            "body_bytes_sent": int(match.group(7)),
            "http_referer": match.group(8),
            "http_user_agent": match.group(9),
            "http_x_forwarded_for": match.group(10),
            "http_x_request_id": match.group(11),
            "http_x_rb_user": match.group(12),
            "request_time": float(match.group(13)),
        }


def group_by_url(log_content):
    groups = defaultdict(list)

    for log in log_content:
        if log is not None:
            groups[log["url"]].append(log)

    return groups


def get_group_stats(log_groups, total_logs):
    group_totals = {url: sum(log["request_time"] for log in group) for url, group in log_groups.items()}
    total_time = sum(group_totals.values())

    for log_url, log_group in log_groups.items():
        sorted_group = sorted(log_group, key=lambda log: log["request_time"], reverse=True)

        len_group = len(log_group)
        time_sum = sum(log["request_time"] for log in log_group)

        stats = {
            "count": len_group,
            "count_perc": len_group / total_logs,
            "time_sum": time_sum,
            "time_perc": time_sum / total_time,
            "time_avg": time_sum / len_group if len_group > 0 else 0,
            "time_max": sorted_group[-1]["request_time"],
            "time_med": sorted_group[len(sorted_group) // 2]["request_time"],
        }

        logger.info(log_url, **stats)


def main():
    log_files = get_log_files()[:1]
    for log_file in log_files:
        # log_date = log_file.split("log-")[-1]
        log_content = [extract_data(log_line) for log_line in get_log_data(log_file)][:200]
        get_group_stats(group_by_url(log_content), len(log_content))


if __name__ == "__main__":
    main()
