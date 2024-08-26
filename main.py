import os
import logging
import csv
import smtplib
import dotenv
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def get_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        logging.critical(f"Environment variable for {var_name} is not set")
        exit(1)
    return value

def read_template(template_path: str) -> Template:
    with open(template_path, "r", encoding="utf-8") as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def read_csv(csv_path: str) -> list[list[str]]:
    with open(csv_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        # Skip the first row (contains headers)
        next(csv_reader)
        return list(csv_reader)

def prepare_copy(emails: list[str]) -> list[str]:
    # Different clients may use different delimiters, change ", " to other delimiters if needed
    return ", ".join(emails)

def prepare_file(file_path: str) -> MIMEApplication:
    with open(file_path, "rb") as file:
        attachment = MIMEApplication(file.read(), Name=os.path.basename(file_path))
        attachment["Content-Disposition"] = f"attachment; filename={os.path.basename(file_path)}"
        return attachment


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

    # Load environment variables (.env file is ignored if they already exist)
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
        message_template = read_template(template_path)
        logging.info("Template loaded")
    except Exception as e:
        logging.error(f"Failed to load template: {e}")
        exit(1)

    try:
        csv = read_csv(csv_path)
        logging.info("CSV loaded")
    except Exception as e:
        logging.error(f"Failed to load CSV: {e}")
        exit(1)

    logging.info("Sending emails")

    total: int = 0
    successful: int = 0
    for row in csv:
        total += 1
        message = MIMEMultipart()


        #----------------------------CONFIGURATION----------------------------#

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

        #---------------------------------------------------------------------#


        message.attach(MIMEText(body, "plain"))
        # Skipped if file list is empty
        for file_path in file_paths:
            try:
                file = prepare_file(file_path)
                message.attach(file)
            except Exception as e:
                logging.error(f"Failed to attach file {file_path} in email to {row[0]}, this email will be skipped: {e}")
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
