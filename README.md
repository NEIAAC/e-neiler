# Quick and reliable ✉️➡️

E-neiler makes it easy to quickly send high amounts of emails with tabled data through SMTP, file attachments included. It works can connect to your custom mail server, gmail, outlook and any other service that allows SMTP. We support a variety of file types for both the body templates and the data tables.

## Usage 🚀

- The app is automatically built by a pipeline with every release, so we provide **direct download links** for most operating systems.

- ### Windows 🪟

  - Use this [link](https://github.com/NEIAAC/e-neiler/releases/latest/download/Windows.zip) to start the download.

  - Run the `main.exe` file inside the extracted folder, you can create a shortcut with any name you like for this file.

- ### Linux 🐧

  - Use this [link](https://github.com/NEIAAC/e-neiler/releases/latest/download/Linux.zip) to start the download.

  - Run the `main.bin` file inside the extracted folder. Note that compilation is targeted at Ubuntu (Wayland), other distributions may need additional actions to run the app.

- ### MacOS 🍎

  - Use this [link](https://github.com/NEIAAC/e-neiler/releases/latest/download/MacOS.zip) to start the download.

  - Run the bundle installer extracted from the `.zip` file.

- Depending on your operating system, you _may_ get a **security warning** due to the app not being signed. You can **safely ignore it** as our builds are automated from the open sourced codebase.

- Detailed usage instructions can be found in the [wiki](https://github.com/NEIAAC/e-neiler/wiki) page.

- See the [example](./example/) directory for demo files.

## Development 🛠️

- ### Requirements 📋

  - Python 3.12.0+

- ### Setup ⚙️

  - Clone the repository and open a terminal **inside** it.

  - Install the dependencies:

    ```shell
    # It is it recommend that a virtual environment is set before doing this!

    pip install .
    ```

  - Start the app:

    ```shell
    python src/main.py
    ```

- ### Tooling 🧰

  - Ruff is used as a linter and formatter:

    ```shell
    pip install .[check]
    ruff check --fix
    ruff format

    # To automatically lint and format on every commit install the pre-commit hooks:
    pre-commit install

    # Note that when using pre-commit the git command will fail if any files are lint fixed or formatted.
    # You will have to add the changed files to the staged area and commit again to apply the changes.
    ```

  - PyTest and PyTest-Qt are used for testing:

    ```shell
    pip install .[test]
    pytest
    ```

  - Nuitka is used for cross-compiling to all supported platforms:

    ```shell
    pip install .[build]
    nuitka <options>
    ```

    See the build [workflow](./.github/workflows/build.yaml) for a list of options used for each platform.
