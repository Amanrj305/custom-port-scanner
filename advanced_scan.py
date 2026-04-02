import socket
import time
from concurrent.futures import ThreadPoolExecutor
from scanner import scan_port

COMMON = {
    21:"FTP",22:"SSH",23:"TELNET",25:"SMTP",
    53:"DNS",80:"HTTP",110:"POP3",143:"IMAP",
    443:"HTTPS",3306:"MySQL"
}

def grab_banner(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)

        s.connect((ip, port))

        if port == 80 or port == 443:
            s.send(b"GET / HTTP/1.0\r\n\r\n")

        banner = ""

        try:
            banner = s.recv(1024).decode(errors="ignore").strip()
        except:
            pass

        s.close()
        return banner

    except:
        return ""


def detect_service(port, banner):
    service = COMMON.get(port, "UNKNOWN")

    b = banner.lower()

    if "http" in b:
        service = "HTTP"
    elif "ssh" in b:
        service = "SSH"
    elif "ftp" in b:
        service = "FTP"
    elif "smtp" in b:
        service = "SMTP"

    return service


def worker(ip, port):
    status = scan_port(ip, port)

    if status == "OPEN":
        banner = grab_banner(ip, port)
        service = detect_service(port, banner)
        return (port, "OPEN", service, banner)

    return (port, "CLOSED", None, None)


def run_scan(ip, start_port, end_port, threads=50):

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = list(executor.map(lambda p: worker(ip, p), range(start_port, end_port+1)))

    end_time = time.time()

    print("\nScan time:", round(end_time-start_time,2), "seconds")

    return results


def save_report(results):

    with open("report.txt","w") as f:
        for port,status,service,banner in results:
            if status == "OPEN":
                f.write(f"{port} | {service} | {banner}\n")


if __name__ == "__main__":

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