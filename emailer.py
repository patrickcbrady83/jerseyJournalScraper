import smtplib
import os

def send_email_for_week(week):
	send_email_for_file('./'+week)

def send_email_for_file(file):
    week = os.path.basename(file)
    gmail_user = open('./deviceu','r').read().replace('\n','')
    gmail_pw = open('./devicepw','r').read().replace('\n','')

    sent_from = gmail_user
    to = [gmail_user]
    subject = "Weehawken Public Notices for Week of %s" % (week)
    body = run_filter(open(file).read())
    email_text = "\n".join(["From: "+sent_from, "To: " + ", ".join(to), "Subject: " + subject, "\n" + body])

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_pw)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print 'Email sent Successfully for', week
    except Exception as e:
        print 'Something went wrong:', e

def run_filter(listings):
    separator = "\n\n====================================\n\n"
    listingList = listings.split(separator.encode('utf-8').strip())
    filteredListings = list(filter(lambda x: not "SHERIFF'S SALE".lower() in x.lower(), listingList))
    return separator.join(filteredListings).encode('utf-8').strip()
