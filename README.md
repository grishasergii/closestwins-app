## Development

To build mock api server
```
cd tests/mock_api_server/
docker build --tag mock-api-server .
```

To run mock-api-server. Add `--rm` to remove the container after it is stopped.
```
docker run -d -p 5001:5000 --name mock-api-server mock-api-server
```

To start mock-api-server container
```
docker start mock-api-server
```