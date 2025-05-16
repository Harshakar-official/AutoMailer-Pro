import smtplib
import time
import os
from email.message import EmailMessage

def show_help():
    print("\n--- Gmail App Password Help ---")
    print("To send emails using this script, you'll need a Gmail App Password.")
    print("Steps:")
    print("1. Go to: https://myaccount.google.com/security")
    print("2. Turn ON 2-Step Verification if not already.")
    print("3. Under 'Signing in to Google', click 'App passwords'.")
    print("4. Choose 'Mail' for the app, and 'Other' or your device name.")
    print("5. Google will generate a 16-character App Password. Use that in this script.\n")

def read_file(filepath):
    if not os.path.exists(filepath):
        print(f"❌ Error: File not found at {filepath}")
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def send_emails(sender_email, sender_password, body_path, email_list_path, attachment_path,
                salutation, subject_line, email_per_second):
    
    body_content = read_file(body_path)
    if body_content is None:
        return

    email_list_content = read_file(email_list_path)
    if email_list_content is None:
        return

    recipients = []
    for line in email_list_content.splitlines():
        parts = [p.strip() for p in line.split(',')]
        if len(parts) == 0:
            continue
        email = parts[0]
        name = parts[1] if len(parts) > 1 else ''
        recipients.append((email, name))

    if not recipients:
        print("❌ No valid recipient entries found.")
        return

    attachment_data = None
    attachment_name = ''
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as f:
            attachment_data = f.read()
            attachment_name = os.path.basename(attachment_path)

    print(f"\n📤 Sending emails to {len(recipients)} recipients...\n")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)

            for i, (email, name) in enumerate(recipients):
                msg = EmailMessage()

                # Handle salutation intelligently
                if name:
                    prefix = salutation.split()[0] if salutation else "Hello"
                    greeting = f"{prefix} {name},"
                else:
                    greeting = f"{salutation},"

                personalized_body = f"{greeting}\n\n{body_content}"
                msg.set_content(personalized_body)
                msg['Subject'] = subject_line
                msg['From'] = sender_email
                msg['To'] = email

                if attachment_data:
                    msg.add_attachment(attachment_data, maintype='application', subtype='octet-stream', filename=attachment_name)

                smtp.send_message(msg)
                print(f"✅ Sent to {email} ({i+1}/{len(recipients)})")
                time.sleep(1 / email_per_second)

        print("\n🎉 All emails sent successfully!")

    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication error. Please check your email or app password.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

def main():
    print("=== Email Automation Script ===\n")

    # Step 1: Login credentials
    while True:
        sender_email = input("Enter your Gmail address (or type 'help' for password help): ").strip()
        if sender_email.lower() == 'help':
            show_help()
            continue
        sender_password = input("Enter your Gmail app password: ").strip()
        if sender_email and sender_password:
            break
        print("❌ Email and password cannot be empty.")

    # Step 2: File paths
    body_path = input("Enter full path to body text file (e.g., /path/to/body.txt): ").strip()
    email_list_path = input("Enter full path to email list file (e.g., /path/to/emails.txt): ").strip()
    attachment_path = input("Enter full path to attachment (optional, leave empty if none): ").strip()

    # Step 3: Email customization
    salutation = input("Enter custom salutation (e.g., Hi, Hello Sir): ").strip()
    subject_line = input("Enter email subject line: ").strip()

    # Step 4: Email rate
    while True:
        try:
            email_per_second = float(input("How many emails per second? (e.g., 1, 0.5): "))
            if email_per_second <= 0:
                raise ValueError
            break
        except ValueError:
            print("❌ Please enter a number greater than 0.")

    # Step 5: Confirm and send
    print("\n📝 Summary:")
    print(f"From: {sender_email}")
    print(f"Body file: {body_path}")
    print(f"Emails list: {email_list_path}")
    print(f"Attachment: {'None' if not attachment_path else attachment_path}")
    print(f"Subject: {subject_line}")
    print(f"Salutation: {salutation}")
    print(f"Rate: {email_per_second} emails/sec")

    confirm = input("\nStart sending emails? (yes/no): ").strip().lower()
    if confirm == 'yes':
        send_emails(sender_email, sender_password, body_path, email_list_path,
                    attachment_path, salutation, subject_line, email_per_second)
    else:
        print("❌ Cancelled.")

if __name__ == "__main__":
    main()
