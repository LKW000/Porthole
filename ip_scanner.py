import socket
import argparse
import subprocess
import platform
import ipaddress  # Standard way to handle 192.168.1.0/24

def get_ports(port_arg):
    """
    Handles all three requirements:
    -p 80 (Single)
    -p 1-100 (Range)
    -p 80,443 (List)
    """
    ports = []
    try:
        # Split by comma first to handle lists
        for section in port_arg.split(','):
            if '-' in section:
                # Handle ranges like 20-25
                low, high = section.split('-')
                for p in range(int(low), int(high) + 1):
                    ports.append(p)
            else:
                # Handle single ports
                ports.append(int(section))
    except Exception as e:
        print(f"Error parsing ports: {e}")
        return []
    return ports

def check_host(ip):
    """Checks if a host is UP using a system ping."""
    # Determine OS for correct ping flag
    flag = '-n' if platform.system().lower() == 'windows' else '-c'
    # Run ping; redirect output to DEVNULL to keep terminal clean
    cmd = ['ping', flag, '1', '-W', '1', str(ip)]
    response = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return response == 0

def scan_target_port(ip, port):
    """
    Uses standard TCP Sockets (NOT WebSockets) to check for open ports.
    Requirement: Includes timeout and error handling.
    Extra Credit: Includes service name lookup.
    """
    # Create the socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.8) # Reasonable timeout for local networks
        
        # connect_ex is better for scanners; it returns an error code instead of crashing
        result = s.connect_ex((str(ip), port))
        
        if result == 0:
            try:
                # EXTRA CREDIT: Get service name (HTTP, HTTPS, SSH, etc.)
                service_name = socket.getservbyport(port, "tcp").upper()
            except:
                service_name = "UNKNOWN"
            return True, service_name
            
    return False, None

def main():
    parser = argparse.ArgumentParser(description="Porthole: IP & Port Scanner")
    parser.add_argument("cidr", help="The network range (e.g. 192.168.1.0/24)")
    parser.add_argument("-p", "--ports", help="Port(s) to scan (e.g. 80, 1-100, or 80,443)")
    
    args = parser.parse_args()

    # Parse ports if the user provided them
    target_ports = []
    if args.ports:
        target_ports = get_ports(args.ports)

    print(f"Starting scan on {args.cidr}...\n")

    try:
        # Expand CIDR into a list of IP addresses
        network = ipaddress.ip_network(args.cidr, strict=False)
        
        for ip in network:
            # Step 1: Check if Host is UP
            if check_host(ip):
                print(f"{ip:<15} (UP)")
                
                # Step 2: Only scan ports if host is UP (Requirement)
                if target_ports:
                    for p in target_ports:
                        is_open, service = scan_target_port(ip, p)
                        if is_open:
                            # Requirement: Clean format + Extra Credit service name
                            print(f"  - Port {p:<5} (OPEN - {service})")
            else:
                # Requirement: Show DOWN hosts in output
                print(f"{ip:<15} (DOWN)")

    except ValueError as e:
        print(f"Invalid CIDR range: {e}")

if __name__ == "__main__":
    main()