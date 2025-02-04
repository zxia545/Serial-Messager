# Serial-Messager

Serial-Messager is a Python project for handling serial commlon and stage4 protocols. It provides tools and interfaces to manage commlon communications, display mockups
## Installation

### 1. Clone the Repository

Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/zxia545/Serial-Messager.git
cd Serial-Messager
```

### 2. Build the Source Distribution

Create a source distribution:

```bash
python3 setup.py sdist
```

This command will create a source distribution in the `dist` directory.

### 3. Install Using `pip`

To install the package directly from the source code, run:

```bash
pip install .
```

### 4. Linux-Specific Prerequisites for the Fast C Extension

On Linux, Serial-Messager can build a fast C extension (using `fastserial`) to improve serial read performance. **If you are installing on Linux and want to use this extension, you must install the Python development headers.**

For Debian/Ubuntu-based systems, run:

```bash
sudo apt-get update
sudo apt-get install python3-dev
```

Other Linux distributions may require a similar package (e.g. `python3-devel` on Fedora/CentOS).

The setup script is configured to build the C extension only on Linux. If you are not on Linux, or if the extension build fails, Serial-Messager will automatically fall back to a pure-Python implementation.

## Usage

Here is a basic example of how to use the project:

```python
from commsHandler.mockDisplay import MockDisplay

# Create a MockDisplay instance (adjust the port as needed)
mockDisplay = MockDisplay("COM6")
```

> **Note:** On Linux, if the fast C extension is built successfully, it will be used automatically to improve performance. Otherwise, the Python fallback implementation will be used.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- **Tony Xiao** - *Initial work* - [zxia545](https://github.com/zxia545)

