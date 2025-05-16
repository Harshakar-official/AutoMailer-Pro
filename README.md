# AutoMailer Pro

AutoMailer Pro is a lightweight Python email automation tool that lets you send bulk personalized emails using your Gmail account. Perfect for career outreach, networking, or campaigns, it supports secure login, custom message templates, and attachments — all from your terminal.

## Features
- Gmail App Password integration
- Personalized greetings with name fallback
- Attachments (PDFs, resumes, etc.)
- Adjustable sending speed
- Email list parsing in `email,name` format

## Usage
Just run the script and follow the prompts!

```bash
python3 sender.py
```
You Need to have Gmail account to use this script. And this is done for security purpose that you can not use it illegally.

Generate Gmail App Passwords: https://myaccount.google.com/apppasswords


## Example Output for Salutation and Email.txt Format

If salutation is set to = Hii Sir

and your email list is like this :
####################################
1:roganag890@deusa7.com, Rahul
2: john@example.com
####################################

Receiver will get mail like:

1: Hii Rahul,
2: Hii Sir,
