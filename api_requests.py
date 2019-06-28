import socket

import ujson


def get_auth(url, credentials):
    # connect to socket
    url = url + "/auth"
    _, _, host, path = url.split("/", 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)

    # prepare data
    data_string = ujson.dumps(credentials)
    content_len = len(data_string)
    message = bytes(
        "POST /%s HTTP/1.1\r\nHost: %s\r\nContent-Type: application/json\r\nContent-Length: %s\r\n\r\n%s"
        % (path, host, content_len, data_string),
        "utf8",
    )

    # send post request
    s.send(message)
    try:
        # get back the full message
        message = str()
        while True:
            data = str(s.recv(1024), "utf8")
            message += data.strip("\n")
            # stop at the end of the response json
            if data[-1] == "}":
                # TODO what if it gets back a bad response?
                break
        if data:
            # parse the response (a little janky)
            messages = message.split()
            status_code = int(messages[1])
            token = messages[-1][:-1].strip('"')  # remove final '}' and '"'

            if status_code == 200:
                return "Bearer " + token
            # TODO action based on other response codes
    except:
        print("failed to post data")
    finally:
        s.close()


def post_data(url, token, data):
    # connect to socket
    url = url + "/sensor_data"
    _, _, host, path = url.split("/", 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)

    # prepare data
    data_string = ujson.dumps(data)
    content_len = len(data_string)
    message = bytes(
        "POST /%s HTTP/1.1\r\nHost: %s\r\nAuthorization: %s\r\nContent-Type: application/json\r\nContent-Length: %s\r\n\r\n%s"
        % (path, host, token, content_len, data_string),
        "utf8",
    )

    # send post request
    s.send(message)
    try:
        # get back the full message
        message = str()
        while True:
            data = str(s.recv(1024), "utf8")
            message += data

            if "errors" in data:
                raise ValueError
            if data[-1] == "}":
                break

        if data:
            # parse the response (a little janky)
            messages = message.split()
            status_code = int(messages[1])

            if status_code != 201:
                print("error")
                # TODO do something useful
    except:
        print("failed to post data")
    finally:
        s.close()
