import ipaddress
from colorama import Fore, Style, init
from datetime import datetime
import os

# Initialize colorama
init()

def write_to_log(content, log_file):
    """Write content to both terminal and log file with ANSI color codes."""
    print(content)  # Print to terminal
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(content + '\n')  # Write to log file with newline

def subnet_calculator(ip, subnet_mask, num_subnets, log_file='subnet_calculator_log.txt'):
    # Add timestamp to log file
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_to_log(Fore.CYAN + Style.BRIGHT + f"\n--- Calculation started at {timestamp} ---" + Style.RESET_ALL, log_file)
    
    try:
        # Create an IP network object
        network = ipaddress.IPv4Network(f"{ip}/{subnet_mask}", strict=False)
        
        # Calculate the number of new bits needed to create at least the requested number of subnets
        original_prefix_length = network.prefixlen
        subnet_bits = 0
        
        while (2 ** subnet_bits) < num_subnets:
            subnet_bits += 1
        
        new_prefix_length = original_prefix_length + subnet_bits
        if new_prefix_length > 32:
            raise ValueError("The number of requested subnets exceeds the maximum possible with this network.")
        
        # Calculate new subnets and take only the requested number
        new_networks = list(network.subnets(new_prefix=new_prefix_length))[:num_subnets]
        
        # Write subnet details with colors to both terminal and log file
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
    
    write_to_log(Fore.CYAN + Style.BRIGHT + f"--- Calculation ended at {timestamp} ---" + Style.RESET_ALL, log_file)

# Example usage
if __name__ == "__main__":
    # Create log file or append to it
    log_file = 'subnet_calculator_log.txt'
    
    # If log file doesn't exist, create it with a header
    if not os.path.exists(log_file):
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("Subnet Calculator Log\n" + "="*20 + "\n")
    
    try:
        ip = input(Fore.YELLOW + "Enter IP address (e.g., 10.10.10.0): " + Style.RESET_ALL)
        subnet_mask = input(Fore.YELLOW + "Enter subnet mask (e.g., 24 for 255.255.255.0): " + Style.RESET_ALL)
        num_subnets = int(input(Fore.YELLOW + "Enter number of subnets required: " + Style.RESET_ALL))
        
        if num_subnets <= 0:
            raise ValueError("Number of subnets must be greater than 0.")
        
        subnet_calculator(ip, subnet_mask, num_subnets, log_file)
    except ValueError as e:
        print(Fore.RED + f"Input Error: {e}" + Style.RESET_ALL)
