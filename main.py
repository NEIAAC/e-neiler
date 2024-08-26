import os
import logging
import csv
import smtplib
import dotenv
import mimetypes
import html2text
from string import Template
from email.message import EmailMessage

def get_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        logging.critical(f"Environment variable for {var_name} is not set")
        exit(1)
    return value

def read_template(template_path: str) -> Template:
    with open(template_path, "r", encoding="utf-8") as template_file:
        content = template_file.read()
    return Template(content)

def read_csv(csv_path: str) -> list[list[str]]:
    with open(csv_path, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        # Skip the first row (contains headers)
        next(csv_reader)
        content = list(csv_reader)
        return content

def prepare_copy(emails: list[str]) -> list[str]:
    # Different clients may use different delimiters, change ", " to other delimiters if needed
    return ", ".join(emails)

def strip_html(content: str) -> str:
    content = html2text.html2text(content)
    return content

def read_attachment(file_path: str) -> tuple[bytes, str, str]:
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type is None:
        mime_type = "application/octet-stream"
    main_type, sub_type = mime_type.split("/")

    with open(file_path, "rb") as file:
        content = file.read()

    return content, main_type, sub_type


def main():
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=logging.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler("e-neiler.log"),
            logging.StreamHandler(),
        ],
    )

    logging.info("Process started")

    # Load environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    smtp_host = get_env("SMTP_HOST")
    smtp_port = get_env("SMTP_PORT")
    smtp_username = get_env("SMTP_USERNAME")
    smtp_password = get_env("SMTP_PASSWORD")
    template_path = get_env("TEMPLATE_PATH")
    csv_path = get_env("CSV_PATH")

    logging.info("Environment variables loaded")
    logging.info(f"Logging in as {smtp_username} on {smtp_host}:{smtp_port}")

    server = smtplib.SMTP(host=smtp_host, port=smtp_port)

    try:
        server.starttls()
        server.login(smtp_username, smtp_password)
        logging.info("Successfully logged in")
    except Exception as e:
        logging.error(f"Failed to login: {e}")
        exit(1)

    try:
        template = read_template(template_path)
        logging.info("Template loaded")
    except Exception as e:
        logging.error(f"Failed to load template: {e}")
        exit(1)

    try:
        csv = read_csv(csv_path)
        logging.info(f"CSV loaded, found {len(csv)} {len(csv) == 1 and 'row' or 'rows'}")
    except Exception as e:
        logging.error(f"Failed to load CSV: {e}")
        exit(1)

    total: int = 0
    successful: int = 0
    for row in csv:
        total += 1

        logging.info(f"[{total}]")

        message = EmailMessage()

        #----------------------------CONFIGURATION----------------------------#

        message["To"] = row[0]

        # Most clients will ignore this and set it as the sender address automatically
        message["From"] = "NEIAAC"

        message["Subject"] = "Your NEIAAC example workshop certificate!"

        # CC and BCC are optional
        message["Cc"] = prepare_copy([""])
        message ["Bcc"] = prepare_copy(["sample@example.com", "fake@example.com"])

        # Replace template placeholders with values from the CSV
        body = template.substitute(
            NAME=row[1]
        )

        # Repeat appends to this list for multiple files or comment/remove them if no files are needed
        file_paths: list[str] = []
        file_paths.append(row[2])

        #---------------------------------------------------------------------#

        # Add alternative plain text version when using html, for backwards compatibility
        if (template_path.endswith(".html")):
            message.set_content(strip_html(body))
            message.add_alternative(body, subtype="html")
        else:
            message.set_content(body)

        # Skipped if file list is empty
        try:
            for file_path in file_paths:
                file, main_type, sub_type = read_attachment(file_path)
                message.add_attachment(file, maintype=main_type, subtype=sub_type, filename=os.path.basename(file_path))
        except Exception as e:
            logging.error(f"Failed to attach file in email to {row[0]}: {e}")
            continue

        try:
            server.send_message(message)
            successful += 1
            logging.info(f"Email sent to {row[0]} successfully")
        except Exception as e:
            logging.error(f"Failed to send email to {row[0]}: {e}")

    logging.info(f"Successfully sent {successful} out of {total} emails")

    logging.info("Logging out")
    server.quit()

    logging.info("Process finished")

if __name__ == "__main__":
    main()
