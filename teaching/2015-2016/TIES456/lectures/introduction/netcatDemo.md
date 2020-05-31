Netcat demo
============
A short demot to show what http is all about on the lower level

netcat
------
* terminal 1
    $ nc -l 8080
* terminal 2
    $ nc localhost 8080
* show communication

netcat http
-----------
start webrick (server for Jekyll - personal website)
$ nc localhost 4000
    GET /~miselico/ HTTP/1.1
    Host: localhost

Now from other server: http://api.openweathermap.org/data/2.5/weather?q=Jyv%C3%A4skyl%C3%A4
$nc api.openweathermap.org 80
    GET /data/2.5/weather?q=Jyv%C3%A4skyl%C3%A4
    Host: api.openweathermap.org
    
