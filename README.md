
# Serial-Messager

Serial-Messager is a Python project for handling serial commlon and stage4 procotol. It provides tools and interfaces to manage commlon communications, display mockups, and handle stage4 messaging sequences.

## Installation

1. **Clone the Repository** (if you haven't already):
Clone the repository and navigate into the project directory:

    ```
    git clone https://github.com/zxia545/Serial-Messager.git
    cd Serial-Messager
    ```

2. **Create a Source Distribution**:
   ```
   python3 setup.py sdist
   ```
   This command will create a source distribution in the `dist` directory.

3. **Install Using `pip`**:
- To install the package directly from the source code, use:
    ```
    pip install .
    ```

## Usage

Describe how to use your project, including example code if possible. For instance:

```python
from mockDisplay import MockDisplay

# Use the module functions
mockDisplay = MockDisplay("/dev/commlon0")
```

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- **Tony Xiao** - *Initial work* - [zxia545](https://github.com/zxia545)

## Acknowledgments

- Hat tip to anyone whose code was used
- Inspiration
- etc
