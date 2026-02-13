import pandas as pd
import smtplib
from email.message import EmailMessage

# ----------------------------
# 1. Read Excel File
# ----------------------------
file_path = "Emp and Training Details.xlsx"
df = pd.read_excel(file_path)
newfile=pd.read_excel("Please confirm your availability for the Team Event on 20th and 21st March(Sheet1).xlsx")

not_voted = newfile["Name"]


for name in not_voted:
    print(name)
# ----------------------------
# 2. Filter employees who haven't completed training
# ----------------------------
not_completed = df[
    df["Business Conduct Educational Process"]
    .fillna("")
    .str.lower()
    .str.strip() != "completed"
]

if not_completed.empty:
    print("All employees have completed the training.")
    exit()

# Get names list
names_list = "\n".join(not_completed["Employee Name"].astype(str).tolist())

print("Employees pending training:")
for name in not_completed["Employee Name"]:
    print(name)

# ----------------------------
# 3. Prepare Email
# ----------------------------
sender_email = "rehansource3@gmail.com"
sender_password = "csbybervypiryuyg"  # Use App Password
receiver_email = "dangneha59@gmail.com"

subject = "Employees Pending Training Completion"

body = f"""
Hello,

The following employees have not completed the Business Conduct Educational Process training:

{names_list}

Please take necessary action.

Regards,
Training Team
"""

msg = EmailMessage()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject
msg.set_content(body)

# ----------------------------
# 4. Send Email
# ----------------------------
try:
    smtp_server = "smtp.gmail.com"
    port = 587

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

    print("Email sent successfully!")

except Exception as e:
    print("Error sending email:", e)
