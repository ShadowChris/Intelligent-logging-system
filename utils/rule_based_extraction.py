# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import re
from collections import defaultdict


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def analyze_all_logs(log_text):
    logs = defaultdict(list)

    pattern = r'\[(INFO|ERROR)\]\[server.go:\d+\] ([\s\S]*?)\n'

    matches = re.findall(pattern, log_text)

    for match in matches:
        logs[match[0]].append(match[1])

    for log_type, log_msgs in logs.items():
        print(f"{log_type}：{len(log_msgs)} in total")
        for log_msg in log_msgs:
            print(log_msg)
        print()


def analyze_err_logs(log_text):
    logs = defaultdict(list)

    pattern = r'\[(ERROR)\]\[server.go:\d+\] ([\s\S]*?)\n'

    matches = re.findall(pattern, log_text)

    for match in matches:
        logs[match[0]].append(match[1])

    for log_type, log_msgs in logs.items():
        print(f"{log_type}：{len(log_msgs)} in total")
        for log_msg in log_msgs:
            print(log_msg)
        print()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    log_text = """
    [INFO][server.go:45] 2023/03/05 21:37:56 bind: 127.0.0.1:6399, start listening...
    [INFO][server.go:77] 2023/03/05 21:39:10 accept link
    [INFO][server.go:58] 2023/03/05 21:52:17 get exit signal
    [INFO][server.go:62] 2023/03/05 21:52:17 shutting down...
    [ERROR][server.go:72] 2023/03/05 21:52:17 listener accept err: accept tcp 127.0.0.1:6399: use of closed network connection
    [INFO][server.go:108] 2023/03/05 21:52:17 handler shutting down...
    [ERROR][server.go:72] 2023/03/05 22:56:56 listener accept err: accept tcp 127.0.0.1:6399: use of closed network connection
    """
    analyze_all_logs(log_text)
    analyze_err_logs(log_text)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
