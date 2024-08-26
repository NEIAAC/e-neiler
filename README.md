# Quick and reliable ✉️➡️

E-neiler makes it easy to quickly send high amounts of emails through SMTP, file attachments included. It works on your custom server, gmail, outlook and any other service that supports SMTP.

## Requirements 📋

- Python 3.0.0+

## Usage 🚀

- Clone the repository:

  ```shell
  git clone https://github.com/NEIAAC/landing-page.git
  ```

- Install the dependencies:

  ```shell
  pip install -r requirements.txt
  ```

- Create a `.env` file based on the provided `.env.example` file, with attention to the notes on each variable

- Edit the `template.txt` file in the `data` folder to contain the appropriate email content

- Edit the `details.csv` file in the `data` folder to contain the appropriate recipient emails, placeholder replacements and file attatchment paths, depending on what is needed

- Map placeholders and files to the values that will be read from the CSV in this section of the `main.py` file:

  ```python
  #-------------CONFIGURATION-------------#

  message["To"] = row[0]
  message["From"] = "NEIAAC"
  message["Subject"] = "Your NEIAAC Python workshop certificate!"

  # CC and BCC are optional
  message["Cc"] = prepare_copy([""])
  message ["Bcc"] = prepare_copy(["sample@example.com", "fake@example.com"])

  # Replace template placeholders with values from the CSV
  body = message_template.substitute(
      NAME=row[1]
  )

  # Repeat appends to this list for multiple files or comment/remove them if no files are needed
  file_paths: list[str] = []
  file_paths.append(row[2])

  #---------------------------------------#
  ```

- Run the script:

  ```shell
  python main.py
  ```
