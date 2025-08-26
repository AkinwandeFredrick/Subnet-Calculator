🧮 Subnet Calculator
A Python-based interactive subnet calculator that computes network details — including network address, broadcast address, usable IP range, and total usable IPs — for Fixed Length Subnet Mask (FLSM) and Variable Length Subnet Mask (VLSM) subnetting. It also supports route summarization to aggregate multiple networks into a single summary route. Results are color-coded using the colorama library and logged to a file for reference.

🚀 Features

✅ Supports Fixed Length Subnet Mask (FLSM) for equal-sized subnets
✅ Supports Variable Length Subnet Mask (VLSM) for subnets based on host requirements
✅ Performs route summarization to aggregate multiple IP networks
✅ Accepts any valid IPv4 address and CIDR subnet
🎯 Dynamically generates subnets or summary routes
🌈 Color-coded terminal output for readability
📝 Logs all calculations to subnet_calculator_log.txt
⚠️ Handles invalid input, subnet overflow, and summarization errors
💡 Ideal for networking students, IT professionals, and network administrators


🛠 Requirements

Python 3.6+
colorama library

Install with:
pip install colorama


📦 Usage
Clone the repository or copy the script, then run:
python subnet_calculator.py

You'll see the main menu:
Subnet Calculator by Akinwande Fredrick
A tool for subnetting (FLSM/VLSM) and route summarization to optimize IP address allocation.

Select your option:
1. Subnet a network
2. Route Summarization
Enter your choice (1 or 2):

Option 1: Subnet a Network

Choose between:
1. Fixed Length Subnet Mask (FLSM): Enter an IP address, subnet mask (e.g., 24), and number of subnets.
2. Variable Length Subnet Mask (VLSM): Enter an IP address, subnet mask, number of subnets, and the number of hosts required for each subnet (with a name for each).


Example inputs for FLSM:
IP address: 192.168.1.0
Subnet mask: 24
Number of subnets: 4


Example inputs for VLSM:
IP address: 192.168.1.0
Subnet mask: 24
Number of subnets: 3
Subnet details: LAN1 (100 hosts), LAN2 (50 hosts), LAN3 (20 hosts)



Option 2: Route Summarization

Enter the number of networks to summarize, followed by the IP address and subnet mask for each network.
Example inputs:
Number of networks: 2
Network 1: 192.168.1.0/24
Network 2: 192.168.2.0/24




🖥 Example Output
FLSM Subnetting
--- FLSM Subnetting started at 2025-08-26 23:20:00 ---
Original Network: 192.168.1.0/24
Original Subnet Mask: 255.255.255.0
Number of Subnets Requested: 4
New Prefix Length: /26
New Subnet Mask: 255.255.255.192

Subnet 1:
  Network Address: 192.168.1.0
  Broadcast Address: 192.168.1.63
  Usable IP Range: 192.168.1.1 - 192.168.1.62
  Total Usable IPs: 62
...
--- FLSM Subnetting ended at 2025-08-26 23:20:01 ---

VLSM Subnetting
--- VLSM Subnetting started at 2025-08-26 23:20:00 ---
Original Network: 192.168.1.0/24
Original Subnet Mask: 255.255.255.0
Number of Subnets Requested: 3

Subnet 1 (LAN1):
  Network Address: 192.168.1.0
  Broadcast Address: 192.168.1.127
  Prefix Length: /25
  Subnet Mask: 255.255.255.128
  Usable IP Range: 192.168.1.1 - 192.168.1.126
  Total Usable IPs: 126

Subnet 2 (LAN2):
  Network Address: 192.168.1.128
  Broadcast Address: 192.168.1.191
  Prefix Length: /26
  Subnet Mask: 255.255.255.192
  Usable IP Range: 192.168.1.129 - 192.168.1.190
  Total Usable IPs: 62

Subnet 3 (LAN3):
  Network Address: 192.168.1.192
  Broadcast Address: 192.168.1.223
  Prefix Length: /27
  Subnet Mask: 255.255.255.224
  Usable IP Range: 192.168.1.193 - 192.168.1.222
  Total Usable IPs: 30

--- VLSM Subnetting ended at 2025-08-26 23:20:01 ---

Route Summarization
--- Route Summarization started at 2025-08-26 23:20:00 ---
Input Networks:
  Network 1: 192.168.1.0/24
  Network 2: 192.168.2.0/24

Summary Route:
  Network Address: 192.168.0.0
  Subnet Mask: 255.255.254.0
  Prefix Length: /23
  Address Range: 192.168.0.0 - 192.168.1.255
--- Route Summarization ended at 2025-08-26 23:20:01 ---


🧾 License
This project is licensed under the MIT License.

🤝 Contributing
Feel free to fork this project, improve it, and submit a pull request!
