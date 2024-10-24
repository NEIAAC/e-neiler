import os
import smtplib
import mimetypes
from typing import Dict
from string import Template
from email.message import EmailMessage
from math import isnan

import pandas as pd
import html2text
from PySide6.QtCore import QThread, Signal

from utils.logger import logger


class EmailerThread(QThread):
    outputSignal = Signal(str, str)

    def __init__(
        self,
        smtpHost: str,
        smtpPort: str,
        smtpUsername: str,
        smtpPassword: str,
        subject: str,
        cc: str,
        bcc: str,
        templatePath: str,
        tablePath: str,
        attachmentDir: str,
    ):
        super().__init__()
        self.smtpHost = smtpHost
        self.smtpPort = smtpPort
        self.smtpUsername = smtpUsername
        self.smtpPassword = smtpPassword
        self.subject = subject
        self.cc = cc
        self.bcc = bcc
        self.templatePath = templatePath
        self.tablePath = tablePath
        self.attachmentDir = attachmentDir

    def output(self, text: str, level: str = "INFO"):
        logger.log(level, text)
        self.outputSignal.emit(text, level)

    def readTemplate(self) -> Template:
        with open(self.templatePath, "r", encoding="utf-8") as templateFile:
            content = templateFile.read()
        return Template(content)

    def readTable(self) -> tuple[list[Dict[str, str]], list[str]]:
        if self.tablePath.endswith(".csv"):
            table = pd.read_csv(self.tablePath, index_col=False)
        elif self.tablePath.endswith(".xlsx"):
            table = pd.read_excel(self.tablePath, index_col=False)
        else:
            self.output("Table data file type extension not supported", "ERROR")
            raise ValueError("Unsupported file format")

        records = table.to_dict("records")
        headers = list(table.columns)

        # Convert NaN, which is parsed in empty cells, to empty string
        for record in records:
            for key in record:
                if type(record[key]) is float and isnan(record[key]):
                    record[key] = ""

        return records, headers

    def readAttachment(self, filePath: str) -> tuple[bytes, str, str]:
        mimeType, _ = mimetypes.guess_type(filePath)

        if mimeType is None:
            mimeType = "application/octet-stream"
        mainType, subType = mimeType.split("/")

        with open(filePath, "rb") as file:
            content = file.read()

        return content, mainType, subType

    def run(self):
        inputs = self.__dict__.copy()
        inputs.pop("smtpPassword")
        logger.info(f"Starting emailer thread with input parameters: {inputs}")
        with logger.catch():
            if not os.path.isdir(self.attachmentDir):
                self.output(
                    f"Attachment directory {self.attachmentDir} not found or is not a directory",
                    "ERROR",
                )
                return

            try:
                body = self.readTemplate()
            except Exception as e:
                self.output(f"Failed to load body: {e}", "ERROR")
                return
            logger.info(f"Body loaded: {body}")
            logger.info(f"Body read: {body}")

            try:
                rows, cols = self.readTable()
            except Exception as e:
                self.output(f"Failed to load table: {e}", "ERROR")
                return
            logger.info(
                f"Table loaded, found {len(rows)} {len(rows) == 1 and 'row' or 'rows'}"
            )
            logger.info(f"Table columns read: {cols}")
            logger.info(f"Table rows read: {rows}")

            if not rows or not cols:
                self.output("Given table is empty", "ERROR")
                return

            variableInputs = {
                "Subject": self.subject,
                "CC": self.cc,
                "BCC": self.bcc,
                "Body": self.attachmentDir,
            }
            # Validate that all variable inputs are present in the table headers
            for key, value in variableInputs.items():
                try:
                    Template(value).substitute(rows[0])
                except KeyError as e:
                    self.output(
                        f"{key} variable not found in table headers: {e}",
                        "ERROR",
                    )
                    return
                except TypeError as e:
                    self.output(
                        f"{key} variable found more than once in table headers: {e}",
                        "ERROR",
                    )
                    return

            server = smtplib.SMTP(host=self.smtpHost, port=self.smtpPort)

            try:
                server.starttls()
                server.login(self.smtpUsername, self.smtpPassword)
                self.output(
                    f"Logged in as {self.smtpUsername} on {self.smtpHost}:{self.smtpPort}"
                )
            except Exception as e:
                self.output(f"Failed to login: {e}", "ERROR")
                return

            total: int = 0
            successful: int = 0
            for row in rows:
                total += 1

                message = EmailMessage()

                if not row[cols[0]] or "@" not in row[cols[0]]:
                    self.output(
                        f"[{total}] Email address column is empty or the value is invalid on this row",
                        "ERROR",
                    )
                    continue

                # Configure email headers
                message["To"] = row[cols[0]].strip()
                message["From"] = self.smtpUsername
                message["Subject"] = Template(self.subject).substitute(row)
                message["Cc"] = Template(self.cc).substitute(row)
                message["Bcc"] = Template(self.bcc).substitute(row)

                # Add body to email
                content = body.substitute(row)
                if self.templatePath.endswith(".html"):
                    message.set_content(html2text.html2text(content))
                    message.add_alternative(content, subtype="html")
                else:
                    message.set_content(content)

                # Add attachments to email
                filePaths: list[str] = []
                if row[cols[1]]:
                    attachmentNames = row[cols[1]].split(",")
                    for attachmentName in attachmentNames:
                        fullPath = os.path.join(
                            self.attachmentDir, attachmentName
                        )
                        filePaths.append(fullPath)
                try:
                    for filePath in filePaths:
                        file, mainType, subType = self.readAttachment(filePath)
                        message.add_attachment(
                            file,
                            maintype=mainType,
                            subtype=subType,
                            filename=os.path.basename(filePath),
                        )
                except Exception as e:
                    self.output(
                        f"[{total}] Failed to attach file in email to {row[cols[0]]}: {e}",
                        "ERROR",
                    )
                    continue

                # Send email
                try:
                    server.send_message(message)
                    successful += 1
                    self.output(
                        f"[{total}] Sent email to {row[cols[0]]} with {len(filePaths)} {len(filePaths) == 1 and 'attachment' or 'attachments'}"
                    )
                except Exception as e:
                    self.output(
                        f"[{total}] Failed to send email to {row[cols[0]]}: {e}",
                        "ERROR",
                    )

            server.quit()

            self.output(f"Successfully sent {successful} out of {total} emails")
