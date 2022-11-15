import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
message=Mail(from_email='sec19cs080@sairamtap.edu.in',to_emails='karthikeyan01230123@gmail.com',
	subject='Registration mail',plain_text_content='Hi, hello welcome',html_content='<strong>Registration successfull!!!</strong>')
try:
	sg=SendGridAPIClient(os.environ['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'])
	response=sg.send(message)
	print(response.status_code)
	print(response.body)
	print(response.headers)
except Exception as e:
	print(e.message)