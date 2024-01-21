# qtcowsay

A simple QtApplication based on [cowsay](https://github.com/VaasuDevanS/cowsay-python).

## Installation

Clone the project and install it with `pip`:

```bash
git clone https://github.com/trappitsch/qtcowsay.git
cd qtcowsay
pip install .
```

## Usage

```bash
qtcowsay
```

This will open a GUI window wrapping around `cowsay`.

## Create an executable with [`PyApp`](https://ofek.dev/pyapp/latest/)

To create an app with `PyApp`
and include the package locally,
clone the directory and build the project.

Make sure `cargo` is installed (as described in `PyApp`'s documentation).
Then follow the 
[instructions](https://ofek.dev/pyapp/latest/how-to/)
to get the latest `PyApp` source.

Copy the `whl` distribution file into the `pytest-latest` folder.
Then set the following environment variables:

| Variable                | Description                       |
|-------------------------|-----------------------------------|
| `PYAPP_PROJECT_NAME`    | "qtcowsay"                        |
| `PYAPP_PROJECT_VERSION` | "0.0.2"                           |
| `PYAPP_PROJECT_PATH`    | "qtcowsay-0.0.2-py3-none-any.whl" |
| `PYAPP_EXEC_SPEC`       | "qtcowsay:run"                    |

Then run `cargo run --release` to build the executable.

**Note**:
If you are using `rye` for building,
you can use the `pyapp_package.py` script
in the `dev` folder to automatically package the project.
The executable will be placed in the same `dev` folder.

## License

`qtcowsay` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
