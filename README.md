
# 🧮 Subnet Calculator (with Colorama)

A Python-based **interactive subnet calculator** that computes network details — including network address, broadcast address, usable IP range, and total usable IPs — based on an IP address, subnet mask, and the number of subnets. Results are color-coded for clarity using the `colorama` library.

---

## 🚀 Features

- ✅ Accepts any valid IPv4 address and CIDR subnet
- 🎯 Dynamically generates multiple subnets
- 🌈 Color-coded terminal output for readability
- ⚠️ Handles invalid input and subnet overflow errors
- 💡 Ideal for networking students and IT professionals

---

## 🛠 Requirements

- Python 3.6+
- `colorama` library

Install with:

```bash
pip install colorama
```

---

## 📦 Usage

Clone the repository or copy the script, then run:

```bash
python subnet_calculator.py
```

You'll be prompted to enter:

- IP address (e.g., `10.10.10.0`)
- Subnet mask (e.g., `24`)
- Number of subnets (e.g., `4`)

---

## 🖥 Example Output

```text
Original Network: 10.10.10.0/24
Original Subnet Mask: 255.255.255.0
Number of Subnets Requested: 4
New Prefix Length: /26
New Subnet Mask: 255.255.255.192

Subnet 1:
  Network Address: 10.10.10.0
  Broadcast Address: 10.10.10.63
  Usable IP Range: 10.10.10.1 - 10.10.10.62
  Total Usable IPs: 62
...
```

---

## 🧾 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Feel free to fork this project, improve it, and submit a pull request!

---


