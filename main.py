import ipaddress
from colorama import Fore, Style, init
from datetime import datetime
import os

# Initialize colorama
init()

def write_to_log(content, log_file):
    """Write content to both terminal and log file with ANSI color codes."""
    print(content)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(content + '\n')

def calculate_prefix_length(hosts):
    """Calculate the prefix length needed for a given number of hosts."""
    import math
    total_addresses = hosts + 2
    prefix_length = 32 - math.ceil(math.log2(total_addresses))
    return prefix_length

def subnet_calculator(ip, subnet_mask, num_subnets, log_file='subnet_calculator_log.txt'):
    """Perform standard subnetting with equal-sized subnets (FLSM)."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_to_log(Fore.CYAN + Style.BRIGHT + f"\n--- FLSM Subnetting started at {timestamp} ---" + Style.RESET_ALL, log_file)
    
    try:
        network = ipaddress.IPv4Network(f"{ip}/{subnet_mask}", strict=False)
        original_prefix_length = network.prefixlen
        subnet_bits = 0
        
        while (2 ** subnet_bits) < num_subnets:
            subnet_bits += 1
        
        new_prefix_length = original_prefix_length + subnet_bits
        if new_prefix_length > 32:
            raise ValueError("The number of requested subnets exceeds the maximum possible with this network.")
        
        new_networks = list(network.subnets(new_prefix=new_prefix_length))[:num_subnets]
        
        write_to_log(Fore.CYAN + Style.BRIGHT + f"Original Network: {network}" + Style.RESET_ALL, log_file)
        write_to_log(Fore.GREEN + f"Original Subnet Mask: {ipaddress.IPv4Network(f'0.0.0.0/{subnet_mask}').netmask}" + Style.RESET_ALL, log_file)
        write_to_log(Fore.YELLOW + f"Number of Subnets Requested: {num_subnets}" + Style.RESET_ALL, log_file)
        write_to_log(Fore.BLUE + f"New Prefix Length: /{new_prefix_length}" + Style.RESET_ALL, log_file)
        write_to_log(Fore.MAGENTA + f"New Subnet Mask: {ipaddress.IPv4Network(f'0.0.0.0/{new_prefix_length}').netmask}" + Style.RESET_ALL, log_file)
        
        for idx, subnetwork in enumerate(new_networks):
            write_to_log(Fore.RED + Style.BRIGHT + f"\nSubnet {idx + 1}:" + Style.RESET_ALL, log_file)
            write_to_log(Fore.GREEN + f"  Network Address: {subnetwork.network_address}" + Style.RESET_ALL, log_file)
            write_to_log(Fore.GREEN + f"  Broadcast Address: {subnetwork.broadcast_address}" + Style.RESET_ALL, log_file)
            usable_ips = list(subnetwork.hosts())
            if usable_ips:
                write_to_log(Fore.GREEN + f"  Usable IP Range: {usable_ips[0]} - {usable_ips[-1]}" + Style.RESET_ALL, log_file)
                write_to_log(Fore.GREEN + f"  Total Usable IPs: {len(usable_ips)}" + Style.RESET_ALL, log_file)
            else:
                write_to_log(Fore.RED + "  No usable IPs in this subnet." + Style.RESET_ALL, log_file)
    
    except ValueError as e:
        write_to_log(Fore.RED + f"Error: {e}" + Style.RESET_ALL, log_file)
    
    end_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_to_log(Fore.CYAN + Style.BRIGHT + f"--- FLSM Subnetting ended at {end_timestamp} ---" + Style.RESET_ALL, log_file)

def vlsm_calculator(ip, subnet_mask, subnet_hosts, log_file='subnet_calculator_log.txt'):
    """Perform VLSM subnetting based on host requirements."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_to_log(Fore.CYAN + Style.BRIGHT + f"\n--- VLSM Subnetting started at {timestamp} ---" + Style.RESET_ALL, log_file)
    
    try:
        network = ipaddress.IPv4Network(f"{ip}/{subnet_mask}", strict=False)
        write_to_log(Fore.CYAN + Style.BRIGHT + f"Original Network: {network}" + Style.RESET_ALL, log_file)
        write_to_log(Fore.GREEN + f"Original Subnet Mask: {network.netmask}" + Style.RESET_ALL, log_file)
        write_to_log(Fore.YELLOW + f"Number of Subnets Requested: {len(subnet_hosts)}" + Style.RESET_ALL, log_file)
        
        sorted_subnets = sorted(subnet_hosts, key=lambda x: x[1], reverse=True)
        
        current_network = network
        for idx, (subnet_name, hosts) in enumerate(sorted_subnets):
            prefix_length = calculate_prefix_length(hosts)
            if prefix_length < network.prefixlen:
                raise ValueError(f"Subnet {subnet_name} requires more addresses than available in the original network.")
            
            subnetworks = list(current_network.subnets(new_prefix=prefix_length))
            if not subnetworks:
                raise ValueError(f"Cannot allocate subnet {subnet_name} with {hosts} hosts.")
            
            subnetwork = subnetworks[0]
            write_to_log(Fore.RED + Style.BRIGHT + f"\nSubnet {idx + 1} ({subnet_name}):" + Style.RESET_ALL, log_file)
            write_to_log(Fore.GREEN + f"  Network Address: {subnetwork.network_address}" + Style.RESET_ALL, log_file)
            write_to_log(Fore.GREEN + f"  Broadcast Address: {subnetwork.broadcast_address}" + Style.RESET_ALL, log_file)
            write_to_log(Fore.BLUE + f"  Prefix Length: /{prefix_length}" + Style.RESET_ALL, log_file)
            write_to_log(Fore.MAGENTA + f"  Subnet Mask: {subnetwork.netmask}" + Style.RESET_ALL, log_file)
            usable_ips = list(subnetwork.hosts())
            if usable_ips:
                write_to_log(Fore.GREEN + f"  Usable IP Range: {usable_ips[0]} - {usable_ips[-1]}" + Style.RESET_ALL, log_file)
                write_to_log(Fore.GREEN + f"  Total Usable IPs: {len(usable_ips)}" + Style.RESET_ALL, log_file)
            else:
                write_to_log(Fore.RED + "  No usable IPs in this subnet." + Style.RESET_ALL, log_file)
            
            current_network = ipaddress.IPv4Network(f"{subnetwork.broadcast_address + 1}/{network.prefixlen}", strict=False)
            if current_network.network_address > network.broadcast_address:
                raise ValueError("Not enough address space for remaining subnets.")
    
    except ValueError as e:
        write_to_log(Fore.RED + f"Error: {e}" + Style.RESET_ALL, log_file)
    
    end_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_to_log(Fore.CYAN + Style.BRIGHT + f"--- VLSM Subnetting ended at {end_timestamp} ---" + Style.RESET_ALL, log_file)

def route_summarization(networks, log_file='subnet_calculator_log.txt'):
    """Perform route summarization for a list of IP networks."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_to_log(Fore.CYAN + Style.BRIGHT + f"\n--- Route Summarization started at {timestamp} ---" + Style.RESET_ALL, log_file)
    
    try:
        # Convert input networks to ipaddress.IPv4Network objects
        ip_networks = [ipaddress.IPv4Network(net, strict=False) for net in networks]
        if not ip_networks:
            raise ValueError("No networks provided for summarization.")
        
        # Log input networks
        write_to_log(Fore.YELLOW + "Input Networks:" + Style.RESET_ALL, log_file)
        for idx, net in enumerate(ip_networks, 1):
            write_to_log(Fore.GREEN + f"  Network {idx}: {net}" + Style.RESET_ALL, log_file)
        
        # Convert network addresses to binary for common prefix calculation
        binary_addresses = [int(net.network_address) for net in ip_networks]
        min_address = min(binary_addresses)
        max_address = max(binary_addresses)
        
        # Find the common prefix length
        diff = min_address ^ max_address  # XOR to find differing bits
        common_prefix = 32
        while diff:
            diff >>= 1
            common_prefix -= 1
        
        # Create the summary network
        summary_network = ipaddress.IPv4Network(f"{ipaddress.IPv4Address(min_address)}/{common_prefix}", strict=False)
        
        write_to_log(Fore.RED + Style.BRIGHT + "\nSummary Route:" + Style.RESET_ALL, log_file)
        write_to_log(Fore.GREEN + f"  Network Address: {summary_network.network_address}" + Style.RESET_ALL, log_file)
        write_to_log(Fore.GREEN + f"  Subnet Mask: {summary_network.netmask}" + Style.RESET_ALL, log_file)
        write_to_log(Fore.BLUE + f"  Prefix Length: /{summary_network.prefixlen}" + Style.RESET_ALL, log_file)
        write_to_log(Fore.GREEN + f"  Address Range: {summary_network.network_address} - {summary_network.broadcast_address}" + Style.RESET_ALL, log_file)
    
    except ValueError as e:
        write_to_log(Fore.RED + f"Error: {e}" + Style.RESET_ALL, log_file)
    
    end_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_to_log(Fore.CYAN + Style.BRIGHT + f"--- Route Summarization ended at {end_timestamp} ---" + Style.RESET_ALL, log_file)

def main():
    log_file = 'subnet_calculator_log.txt'
    
    # Create log file with header if it doesn't exist
    if not os.path.exists(log_file):
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("Subnet Calculator Log\n" + "="*20 + "\n")
    
    # Display header
    print(Fore.CYAN + Style.BRIGHT + "Subnet Calculator by Akinwande Fredrick" + Style.RESET_ALL)
    print(Fore.GREEN + "A tool for subnetting (FLSM/VLSM) and route summarization to optimize IP address allocation." + Style.RESET_ALL)
    print(Fore.YELLOW + "\nSelect your option:" + Style.RESET_ALL)
    print(Fore.YELLOW + "1. Subnet a network" + Style.RESET_ALL)
    print(Fore.YELLOW + "2. Route Summarization" + Style.RESET_ALL)
    
    try:
        choice = input(Fore.YELLOW + "Enter your choice (1 or 2): " + Style.RESET_ALL)
        
        if choice not in ['1', '2']:
            raise ValueError("Invalid choice. Please select 1 or 2.")
        
        if choice == '1':
            print(Fore.YELLOW + "\nSelect your option:" + Style.RESET_ALL)
            print(Fore.YELLOW + "1. Fixed Length Subnet Mask (FLSM)" + Style.RESET_ALL)
            print(Fore.YELLOW + "2. Variable Length Subnet Mask (VLSM)" + Style.RESET_ALL)
            subnet_choice = input(Fore.YELLOW + "Enter your choice (1 or 2): " + Style.RESET_ALL)
            
            if subnet_choice not in ['1', '2']:
                raise ValueError("Invalid choice. Please select 1 or 2.")
            
            ip = input(Fore.YELLOW + "Enter IP address (e.g., 192.168.1.0): " + Style.RESET_ALL)
            subnet_mask = input(Fore.YELLOW + "Enter subnet mask (e.g., 24 for 255.255.255.0): " + Style.RESET_ALL)
            
            if subnet_choice == '1':
                num_subnets = int(input(Fore.YELLOW + "Enter number of subnets required: " + Style.RESET_ALL))
                if num_subnets <= 0:
                    raise ValueError("Number of subnets must be greater than 0.")
                subnet_calculator(ip, subnet_mask, num_subnets, log_file)
            
            elif subnet_choice == '2':
                num_subnets = int(input(Fore.YELLOW + "Enter number of subnets required: " + Style.RESET_ALL))
                if num_subnets <= 0:
                    raise ValueError("Number of subnets must be greater than 0.")
                subnet_hosts = []
                for i in range(num_subnets):
                    name = input(Fore.YELLOW + f"Enter name for subnet {i+1} (e.g., LAN1): " + Style.RESET_ALL)
                    hosts = int(input(Fore.YELLOW + f"Enter number of hosts required for {name}: " + Style.RESET_ALL))
                    if hosts < 0:
                        raise ValueError("Number of hosts cannot be negative.")
                    subnet_hosts.append((name, hosts))
                vlsm_calculator(ip, subnet_mask, subnet_hosts, log_file)
        
        elif choice == '2':
            num_networks = int(input(Fore.YELLOW + "Enter number of networks to summarize: " + Style.RESET_ALL))
            if num_networks <= 0:
                raise ValueError("Number of networks must be greater than 0.")
            networks = []
            for i in range(num_networks):
                net_ip = input(Fore.YELLOW + f"Enter IP address for network {i+1} (e.g., 192.168.1.0): " + Style.RESET_ALL)
                net_mask = input(Fore.YELLOW + f"Enter subnet mask for network {i+1} (e.g., 24): " + Style.RESET_ALL)
                networks.append(f"{net_ip}/{net_mask}")
            route_summarization(networks, log_file)
    
    except ValueError as e:
        print(Fore.RED + f"Input Error: {e}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
