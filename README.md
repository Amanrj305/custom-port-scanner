# Custom Port Scanner with Service Detection

## Overview
This project implements a TCP port scanner using socket programming.

## Features
- TCP connect scanning
- Concurrent scanning using threads
- Banner grabbing
- Service detection
- Performance measurement

## Technologies Used
- Python
- Socket Programming
- ThreadPoolExecutor

## Project Structure
scanner.py – core TCP scanning
advanced_scan.py – concurrency + banner grabbing
main.py – program entry point

## How to Run

python main.py

## Example Output
(22, 'OPEN', 'SSH', 'SSH-2.0-OpenSSH')
(80, 'OPEN', 'HTTP', 'HTTP/1.1 200 OK')

