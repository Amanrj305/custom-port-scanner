import socket
from advanced_scan import run_scan, save_report

target = input("Target: ")

try:
    ip = socket.gethostbyname(target)
except:
    print("Invalid host")
    exit()

start_port = int(input("Start port: "))
end_port = int(input("End port: "))

results = run_scan(ip, start_port, end_port)

print("\nOPEN PORTS\n")

for r in results:
    if r[1] == "OPEN":
        print(r)

save_report(results)

print("\nReport saved to report.txt")