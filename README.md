# Fuzdir
Web path fuzzer

## Installing
Run the following command to install with pip:
```bash
$ pip3 install fuzdir 
```
Run the following commands to manually install:
```bash
$ git clone https://github.com/n3v4/fuzdir.git fuzdir
$ cd fuzdir
$ pip3 install -r requirements.txt
```

## Usage
You can start the process of fuzzing files and directories with the following command:
```bash
$ fuzdir.py -u <url> -w <wordlist>
```
Help message:
```bash
usage: fuzdir [-h] -u URL -w PATH [-e EXTENSIONS] [-E PATH] [-t THREADS]
              [--timeout TIMEOUT] [--retry RETRY] [--throttling SECONDS]
              [--proxy URL] [--user-agent USER AGENT] [-c COOKIE] [-H HEADER]
              [--allow-redirect] [-v]
              [--plain-report PATH | --json-report PATH] [-x CONDITIONS]

optional arguments:
  -h, --help            show this help message and exit

necessary arguments:
  -u URL, --url URL     target URL
  -w PATH, --wordlist PATH
                        path to word list

extensions settings:
  -e EXTENSIONS, --extensions EXTENSIONS
                        extension list separated by comma
  -E PATH, --extensions-file PATH
                        path to file with extensions

connection settings:
  -t THREADS, --threads THREADS
                        the maximum number of threads that can be used to requests, by default 10 threads
  --timeout TIMEOUT     connection timeout, by default 5s.
  --retry RETRY         number of attempts to connect to the server, by default 3 times
  --throttling SECONDS  delay time in seconds (float) between requests sending
  --proxy URL           HTTP or SOCKS5 proxy
                        usage format:
                          [http|socks5]://user:pass@host:port

request settings:
  --user-agent USER AGENT
                        custom user agent, by default setting random user agent
  -c COOKIE, --cookie COOKIE
  -H HEADER, --header HEADER
                        pass custom header(s)
  --allow-redirect      allow follow up to redirection

logging settings:
  -v, --verbose         verbose logging

reports settings:
  --plain-report PATH   a plain text reporting about the found status code, content length and path
  --json-report PATH    a reporting in JSON about the found status code, content length and path

filter:
  -x CONDITIONS         conditions for responses matching
                        available conditions:
                          code		filter by status code
                          length	filter by content length
                          grep		filter by regex in response headers or / and body
                        usage format:
                          [ignore]:<condition>:[<area>]=<args>
                        examples:
                          code=200,500		    match responses with 200 or 500 status code
                          ignore:code=404	    match responses exclude with 404 status code
                          length=0-1337,7331	match responses with content length between 0 and 1337 or equals 7331
                          grep='regex'		    match responses with 'regex' in headers or body
                          grep:body='regex'	    match responses with 'regex' in body
```

### Extensions
Extensions can be specified as `.ext` or `ext`, or as a formatted string `%.ext`. For example, if wordlist contains only
 `index`, and the extensions `php`, `.html`, `%.txt`, the following path will be sent to the server:
```
/index
/index.php
/index.html
/index.txt
```

### Throttling
Throttling allows you to adjust the frequency of sending packets to the server. To do this, you can explicitly pass the
 number of seconds that must elapse before sending the next packet to the server. For example, if the argument
 `--throttling 2.5` is passed to fuzdir, then 1 packet will be sent to the server every 2.5 seconds.

By default, when throttling isn't set, fuzdir adjusts the throttling value during fuzzing, tracking the response time
 from the server.

Throttling can be completely disabled through `--throttling 0`. 

### Custom header(s)
You can pass one or more custom headers with `-H` or `--header`. For example, if you pass `-H Platform:web` and
 `-H "Token: reWfBt1fnbgjEhA6wfs+Uw=="` the following HTTP-request will be sent to the server:
```
GET /path HTTP/1.1
Host: www.example.com
...
Platform: web
Token: reWfBt1fnbgjEhA6wfs+Uw==
...
```

### Conditions
Conditions is a system for filtering HTTP responses during fuzzing. 

Usage format `[ignore]:<condition>:[<area>]=<args>`
- `ignore` condition inverting,
- `condition` condition name,
- `area` search area (only grep supported),
- `args` condition arguments.

Currently it supports the following conditions:

| Condition | Area  | Args | Examples |
| --------- | :---: | ---- | -------- |
| code      | no    | list of status codes (or ranges) separated by comma | `-x code=200,500-503` match responses with 200, 500, 501, 502, or 503 status code |
| length    | no    | list of lengths (or ranges) separated by comma | `-x length=0-1337,7331` match responses with content length between 0 and 1337 or equals 7331 |
| grep      | headers, body | regex | `-x grep=token` match responses which contains 'token' in headers or body <br/>`-x grep:body=token` match responses which contains 'token' in body |
