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
$ python3 setup.py install
```

## Usage
You can start the process of fuzzing files and directories with the following command:
```bash
$ fuzdir.py -u <url> -W <wordlist>
```
Help message:
```bash
usage: fuzdir [-h] -u URL (-w WORDS | -W PATH) [-e EXTENSIONS] [-E PATH]
              [-m METHOD] [-t THREADS] [--timeout TIMEOUT] [--retry RETRY]
              [--retry-status-list STATUS_LIST] [--ignore-retry-fail]
              [--throttling [SECONDS]] [--proxy URL] [--user-agent USER AGENT]
              [-c COOKIE] [-H HEADER] [--allow-redirect] [-v]
              [--report CONFIG] [-x CONDITIONS]

optional arguments:
  -h, --help            show this help message and exit

necessary arguments:
  -u URL, --url URL     target URL
  -w WORDS, --wordlist WORDS
                        a comma-separated list of words
  -W PATH, --wordlist-path PATH
                        path to word list

extensions settings:
  -e EXTENSIONS, --extensions EXTENSIONS
                        extension list separated by comma
  -E PATH, --extensions-file PATH
                        path to file with extensions

connection settings:
  -m METHOD, --method METHOD
                        HTTP method to use^ by default is GET
  -t THREADS, --threads THREADS
                        the maximum number of threads that can be used to requests, by default 10 threads
  --timeout TIMEOUT     connection timeout, by default 5s.
  --retry RETRY         number of attempts to connect to the server, by default 3 times
  --retry-status-list STATUS_LIST
                        a comma-separated list of HTTP status codes for which should be retry on, by default 504, 502, 503
  --ignore-retry-fail   ignore failed attempts to connect to server and continue fuzzing
  --throttling [SECONDS]
                        delay time in seconds (float) between requests sending, if the throttling value is not specified, it will automatically adjust during fuzzing
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
  --report CONFIG       reports on responses
                        available types:
                          plain         a plain text reporting
                          json          a reporting in JSON
                        usage format:
                          <type>[:components]=<path>
                        available components:
                          json:
                            body        a response body
                            length      a response content length
                            headers     a response headers
                            code        a response status code
                        examples:
                          plain=/tmp/report.txt                 a plain text reporting about the found status code, content length and path
                          json=/tmp/report.json                 a reporting in JSON about the found status code, content length and path
                          json:code,body=/tmp/report.json       a reporting in JSON about the found status code, body and path

filter:
  -x CONDITIONS         conditions for responses matching
                        available conditions:
                          code          filter by status code
                          length        filter by content length
                          grep          filter by regex in response headers or / and body
                        usage format:
                          [ignore:]<condition>[:<area>]=<args>[;]
                        examples:
                          code=200,500                  match responses with 200 or 500 status code
                          ignore:code=404               match responses exclude with 404 status code
                          length=0-1337,7331            match responses with content length between 0 and 1337 or equals 7331
                          grep='regex'                  match responses with 'regex' in headers or body
                          grep:body='regex'             match responses with 'regex' in body
                          code=200;length=0-1337        match responses with 200 status code and content length between 0 and 1337

examples:
  fuzdir -u https://example.com -W wordlist.txt
  fuzdir -u https://example.com -w index,robots -e html,txt
  fuzdir -u https://example.com -W wordlist.txt -e html,js,php -x code=200
  fuzdir -u https://example.com -W wordlist.txt -x code=200;ignore:grep:headers='Auth'
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

When throttling value isn't specified, fuzdir adjusts the throttling value during fuzzing, tracking the response time
 from the server.

By default, throttling completely disabled, similar `--throttling 0`. 

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

### Retry settings
You can specify a list of HTTP status codes with `--retry-status-list`, for which fuzdir should resend the request to
 the server, the default value is 502, 503, 504.

The number of attempts can be adjusted using `--retry` from 0 to 5 inclusive, by default 3 attempts.

By default, if all attempts were fail, fuzzing will be interrupted and the program will exit. To avoid this, you can use
 `--ignore-retry-fail`.

### Report
You can write a fuzzing results to file with `--report` key.

Usage format `<type>[:components]=<path>`
- `type` report type,
- `components` список компонент, которые должны быть включены в отчет,
- `path` путь до файла.

Currently it supports the following components:
- `body` a response body,
- `length` a response content length,
- `headers` a response headers,
- `code` a response status code.

Currently it supports the following report types:

| Type | Default Components | Supported Components | Examples |
| ---- | :----------------: | :------------------: | -------- |
| plain | code, length | no | `--report plain=/tmp/report.txt` a plain text reporting about the found status code, content length and path |
| json | code, length | body, length, headers, code | `--report json=/tmp/report.txt` a reporting in JSON about the found status code, content length and path<br/>`--report json:code,body=/tmp/report.json` a reporting in JSON about the found status code, body and path |

### Conditions
Conditions is a system for filtering HTTP responses during fuzzing. 

Usage format `[ignore]:<condition>:[<area>]=<args>[;]`
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

You can use multiple conditions, separating them with a semicolon, for example: `-x code=200;length=0-1337`