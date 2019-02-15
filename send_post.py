import socket

import ujson


def http_post(url, data):
    # connect to socket
    _, _, host, path = url.split("/", 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)

    # prepare data
    data_string = ujson.dumps(data)
    content_len = len(data_string)
    message = bytes(
        "POST /%s HTTP/1.1\r\nHost: %s\r\nContent-Type: application/json\r\nContent-Length: %s\r\n\r\n%s"
        % (path, host, content_len, data_string),
        "utf8",
    )

    # send post request
    s.send(message)
    try:
        data = s.recv(100)
        # TODO action based on response code
        if data:
            print(str(data, "utf8"), end="")
        else:
            print("no data")
    except:
        print("failed to post data")
    finally:
        s.close()
