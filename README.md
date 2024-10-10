# Quick and reliable ✉️➡️

E-neiler makes it easy to quickly send high amounts of emails with tabled data through SMTP, file attachments included. It works on your custom server, gmail, outlook and any other service that allows SMTP. We support a variety of file types for both the body templates and the data tables.

## Requirements 📋

- Python 3.12.0+

## Usage 🚀

- Download the app from [here](https://github.com/NEIAAC/e-neiler/releases/latest), under the `assets` section, click the `.exe` file.

- Load template.

- Load table.

- Start the process.

- Edit the `template.txt` file in the `data` folder to contain the appropriate email content or even change it to a `.html` file.

- Edit the `table.csv` file in the `data` folder, or add your own, with the appropriate recipient emails, placeholder replacements and file attatchment paths, depending on what is needed.

## Development 🛠️

- Clone the repository:

  ```shell
  git clone https://github.com/NEIAAC/e-neiler.git
  ```

- Install the dependencies:

  ```shell
  pip install .
  ```

- Start the app:

  ```shell
  pyside6-project run
  ```

### Notes 🗒️

- When adding resources to the app always use the `resources` folder and add each file to the `index.qrc` file too. The `run` command will then use this `.qrc` file to generate the `rc_index.py` file, which exposes the resources to be used inside app like this:

  ```python
  QIcon(QPixmap(":/icons/logo.png"))
  ```
