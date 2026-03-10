#!/usr/bin/env python3
import socket
import argparse
import subprocess
import platform
import ipaddress

def get_ports(port_arg):
    ports = []
    try:
        for section in port_arg.split(','):
            section = section.strip()
            if '-' in section:
                low, high = section.split('-')
                for p in range(int(low.strip()), int(high.strip()) + 1):
                    ports.append(p)
            else:
                ports.append(int(section))
    except:
        return []
    return sorted(list(set(ports)))

def check_host(ip):
    flag = '-n' if platform.system().lower() == 'windows' else '-c'
    cmd = ['ping', flag, '1', '-W', '1', str(ip)]
    response = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return response == 0

def scan_target_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.8)
        result = s.connect_ex((str(ip), port))
        
        if result == 0:
            try:
                service_name = socket.getservbyport(port, "tcp").upper()
                return True, service_name
            except:
                return True, "UNKNOWN"
    return False, None

def main():
    parser = argparse.ArgumentParser(description="Porthole: IP & Port Scanner")
    parser.add_argument("cidr", help="Network range")
    parser.add_argument("-p", "--ports", help="Port range/list")
    
    args = parser.parse_args()
    target_ports = get_ports(args.ports) if args.ports else []

    print(f"Starting scan on {args.cidr}...\n")

    try:
        network = ipaddress.ip_network(args.cidr, strict=False)
        
        for ip in network:
            ip_str = str(ip)
            if check_host(ip_str):
                print(f"{ip_str:<15} (UP)")
                
                if target_ports:
                    for p in target_ports:
                        is_open, service = scan_target_port(ip_str, p)
                        if is_open:
                            print(f"  - Port {p:<5} (OPEN - {service})")
            else:
                print(f"{ip_str:<15} (DOWN)")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()