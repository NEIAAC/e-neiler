from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from qfluentwidgets import (
    BodyLabel,
    SingleDirectionScrollArea,
)


class HelpPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Guide")

        self.helpText = BodyLabel(
            """
<h1>Guide</h1>

<h2>Overview</h2>
<p>
    This application helps you send personalized mass emails using data from a spreadsheet. Perfect for newsletters,
    announcements, or any situation where you need to send customized emails to multiple recipients.
</p>

<h2>SMTP Configuration</h2>

<h3>SMTP Host</h3>
<ul>
    <li>Enter your email provider's SMTP server address</li>
    <li>Example: <code>smtp.gmail.com</code> for Gmail</li>
    <li>For other providers, check their SMTP settings documentation</li>
</ul>

<h3>SMTP Port</h3>
<ul>
    <li>Enter your email provider's SMTP port</li>
    <li>Common ports:</li>
    <ul>
        <li>587 (TLS)</li>
        <li>465 (SSL)</li>
    </ul>
    <li>Check your email provider's documentation for the correct port</li>
</ul>

<h3>SMTP Username</h3>
<ul>
    <li>Enter your email address</li>
    <li>For Gmail users: Use your complete email address</li>
    <li>For business emails: Check with your IT department</li>
</ul>

<h3>SMTP Password</h3>
<ul>
    <li>Enter your email password or app-specific password</li>
    <li>For Gmail: Use an App Password (regular password won't work with 2FA)</li>
    <li>Keep this secure - the app saves this locally</li>
</ul>

<h2>Email Settings</h2>

<h3>Subject</h3>
<ul>
    <li>Enter your email subject line</li>
    <li>You can use template variables: <code>{{variable_name}}</code></li>
    <li>Variables will be replaced with data from your spreadsheet</li>
</ul>

<h3>CC Recipients</h3>
<ul>
    <li>Optional: Add CC recipients</li>
    <li>Separate multiple emails with commas</li>
    <li>Example: <code>person1@example.com, person2@example.com</code></li>
</ul>

<h3>BCC Recipients</h3>
<ul>
    <li>Optional: Add BCC recipients</li>
    <li>Separate multiple emails with commas</li>
    <li>Recipients won't see other BCC addresses</li>
</ul>

<h2>Files Setup</h2>

<h3>Template File</h3>
<ul>
    <li>Create an HTML file for your email template</li>
    <li>Use <code>{{variable_name}}</code> for dynamic content</li>
    <li>Variables must match your spreadsheet column names</li>
    <li>Example: <code>Dear {{name}}, Your balance is {{amount}}</code></li>
</ul>

<h3>Table File</h3>
<ul>
    <li>Supported formats: CSV, Excel (.xlsx)</li>
    <li>Must include an 'email' column for recipients</li>
    <li>Other columns can be used as template variables</li>
    <li>First row should be column headers</li>
</ul>

<h3>Attachments Directory</h3>
<ul>
    <li>Optional: Select a folder containing attachments</li>
    <li>Files must be named to match your data</li>
    <li>Example: If spreadsheet has 'attachment' column with 'doc1.pdf', that file must exist in the folder</li>
</ul>

<h2>Running the App</h2>
<ol>
    <li>Click the Play button to start sending emails</li>
    <li>Monitor progress in the log window</li>
    <li>Green text indicates success</li>
    <li>Red text indicates errors</li>
    <li>Use the trash can icon to clear logs</li>
    <li>The app will notify you when complete</li>
</ol>

<h2>Tips</h2>
<ul>
    <li>Test with a controlled small group first</li>
    <li>Double-check all settings before sending</li>
    <li>Keep template files simple and well-formatted</li>
    <li>Ensure all attachments exist before starting</li>
    <li>Watch for error messages in the run logs</li>
</ul>

<h2>Troubleshooting</h2>
<ul>
    <li><strong>Authentication failed:</strong> Check username and password</li>
    <li><strong>Connection refused:</strong> Verify SMTP host and port</li>
    <li><strong>Template error:</strong> Check variable names match spreadsheet</li>
    <li><strong>File not found:</strong> Verify all paths and filenames</li>
    <li><strong>Invalid email:</strong> Check email format in spreadsheet</li>
</ul>
           """,
        )
        self.helpText.setWordWrap(True)

        self.contentWidget = QWidget()
        self.contentLayout = QVBoxLayout(self.contentWidget)
        self.contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.contentLayout.setContentsMargins(40, 40, 50, 40)
        self.contentLayout.setSpacing(40)
        self.contentLayout.addWidget(self.helpText)

        self.scrollArea = SingleDirectionScrollArea(
            orient=Qt.Orientation.Vertical
        )
        self.scrollArea.setWidget(self.contentWidget)
        self.scrollArea.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding
        )
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.enableTransparentBackground()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.scrollArea)

        self.setLayout(self.mainLayout)
