# SerialExperimentsLAN

A tool for hosting and connecting to web APIs on local networks. It uses
periodic UDP datagrams to announce the existence of a service to all listeners.
Datagrams are broadcast to port `1337`, and consist of just the string
`sel-announce <port_number>`, where the port number is the port on the
announcing computer that has the service in question.

## Transmitter API

By announcing a transmitter's existence, the web API promises to have at least
one endpoint: `/transmitter_info`. This endpoint should serve a JSON object with
properties `name` and `description`, which provide some user-friendly info
about the transmitter's services.

## Usage

Services running using the Serial Experiments LAN protocol are fairly simple.
To announce the existence of a service, simply import `transmitter.py` and
call `transmitter.run_transmitter(<port_number>, <timeout>)`. The port number
should be the port on the transmitter's host machine that the transmitter is
available on. The delay is the time between announcements, with the minimum
being 10 seconds.

To listen for services, import `scanner.py` and run `scanner.run_scanner(<callback>)`, where the callback is a function that takes
a service address (a pair of an IP address and port number, as strings), and
performs some action. The callback is called every time a transmission is
received.
