import os
import smtplib
import mimetypes
from typing import Dict
from string import Template
from email.message import EmailMessage
from math import isnan

import pandas as pd
import openpyxl
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
        origin: str,
        reply: str,
        cc: str,
        bcc: str,
        bodyPath: str,
        tablePath: str,
        attachmentPath: str,
    ):
        super().__init__()
        self.smtpHost = smtpHost
        self.smtpPort = smtpPort
        self.smtpUsername = smtpUsername
        self.smtpPassword = smtpPassword
        self.subject = subject
        self.origin = origin
        self.reply = reply
        self.cc = cc
        self.bcc = bcc
        self.bodyPath = bodyPath
        self.tablePath = tablePath
        self.attachmentPath = attachmentPath

    def output(self, text: str, level: str = "INFO"):
        logger.log(level, text)
        self.outputSignal.emit(text, level)

    def readBody(self) -> Template:
        with open(self.bodyPath, "r", encoding="utf-8") as bodyFile:
            content = bodyFile.read()
        return Template(content)

    def readTable(self) -> tuple[list[Dict[str, str]], list[str]]:
        if self.tablePath.endswith(".csv"):
            logger.info(
                f"Using pandas {pd.__version__} to read {self.tablePath}"
            )
            table = pd.read_csv(self.tablePath, index_col=False)
        elif self.tablePath.endswith(".xlsx"):
            logger.info(
                f"Using openpyxl {openpyxl.__version__} to read {self.tablePath}"
            )
            table = pd.read_excel(self.tablePath, index_col=False)
        else:
            raise ValueError("Unsupported file extension")

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
        self.output("...")
        with logger.catch():
            if not os.path.isdir(self.attachmentPath):
                self.output(
                    f"Attachment directory {self.attachmentPath} not found or is not a directory",
                    "ERROR",
                )
                return

            try:
                body = self.readBody()
            except Exception as e:
                self.output(f"Failed to load body: {e}", "ERROR")
                return
            logger.info(f"Body loaded: {body.template}")
            logger.info(f"Body read: {body.template}")

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
            if len(rows) < 1:
                self.output(
                    "Given table must have at least another row in addition to the headers!",
                    "ERROR",
                )
                return

            variableInputs = {
                "Subject": self.subject,
                "CC": self.cc,
                "BCC": self.bcc,
                "Body": self.attachmentPath,
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
                message["From"] = self.origin.strip()
                message["Subject"] = (
                    Template(self.subject).substitute(row).strip()
                )
                if self.reply:
                    message["Reply-To"] = (
                        Template(self.reply).substitute(row).strip()
                    )
                if self.cc:
                    message["Cc"] = Template(self.cc).substitute(row).strip()
                if self.bcc:
                    message["Bcc"] = Template(self.bcc).substitute(row).strip()

                # Add body to email
                content = body.substitute(row)
                if self.bodyPath.endswith(".html"):
                    message.set_content(html2text.html2text(content))
                    message.add_alternative(content, subtype="html")
                else:
                    message.set_content(content)

                # Add attachments to email
                filePaths: list[str] = []
                try:
                    if len(cols) > 1 and row[cols[1]]:
                        attachmentNames = row[cols[1]].split(",")
                        for attachmentName in attachmentNames:
                            fullPath = os.path.join(
                                self.attachmentPath, attachmentName
                            )
                            filePaths.append(fullPath)
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
