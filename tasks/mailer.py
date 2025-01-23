import http.client

def mail(subject,body,recipient):
    conn = http.client.HTTPSConnection("privy.pythonanywhere.com")

    payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"subject\"\r\n\r\n{subject}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"body\"\r\n\r\n{body}\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"recipient\"\r\n\r\n{recipient}\r\n-----011000010111000001101001--\r\n"

    headers = {
        'Content-Type': "multipart/form-data; boundary=---011000010111000001101001",
        'User-Agent': "insomnia/10.3.0"
        }

    conn.request("POST", "/mail/", payload, headers)

    res = conn.getresponse()
    data = res.read()

# print(data.decode("utf-8"))