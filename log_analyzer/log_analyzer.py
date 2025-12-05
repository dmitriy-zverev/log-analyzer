# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';
import gzip

config = {"REPORT_SIZE": 1000, "REPORT_DIR": "./reports", "LOG_DIR": "./log"}


def main():
    with gzip.open("nginx-access-ui.log-20170630.gz", "rt", encoding="utf-8") as f:
        content = f.read().split("\n")[:1]
        for c in content:
            print(c)


if __name__ == "__main__":
    main()
