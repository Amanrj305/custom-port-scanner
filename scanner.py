import socket
import time
import ssl 

def scan_port(ip, port, timeout=1, retries=3):
    attempt = 0

    while attempt < retries:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)

            if port == 443:
                context = ssl.create_default_context()
                s = context.wrap_socket(s, server_hostname=ip)

            res = s.connect_ex((ip, port))
            s.close()

            if res == 0:
                return "OPEN"

            attempt += 1

        except socket.timeout:
            attempt += 1
        except:
            attempt += 1

    return "CLOSED"


def scan_range(ip, start_port, end_port):
    results = {}
    start = time.time()

    print("\nScanning:", ip)
    print("Ports:", start_port, "-", end_port, "\n")

    for p in range(start_port, end_port + 1):
        status = scan_port(ip, p)
        results[p] = status
        print("Port", p, ":", status)

    end = time.time()
    print("\nScan finished")
    print("Time taken:", round(end - start, 2), "seconds")

    return results


if __name__ == "__main__":
    target = input("Enter target IP or domain: ")

    try:
        ip = socket.gethostbyname(target)
    except:
        print("Invalid host")
        exit()

    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))

    scan_range(ip, start_port, end_port)
