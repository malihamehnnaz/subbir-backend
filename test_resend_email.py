import resend

# Set your Resend API key
resend.api_key = "re_xxxxxxxxx"  # Replace with your actual API key

# Define email parameters
params = resend.Emails.SendParams(
    from_="Acme <onboarding@resend.dev>",  # Replace with a verified domain email
    to=["delivered@resend.dev"],
    subject="hello world",
    html="<p>it works!</p>"
)

# Send the email
try:
    email = resend.Emails.send(params)
    print("Email sent successfully:", email)
except Exception as e:
    print("Failed to send email:", e)