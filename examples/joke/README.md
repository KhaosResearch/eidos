Run with:

```bash
docker build -t eidos-joke .
docker run --rm -p 8090:80 eidos-joke
```

Example:

```bash
curl -X POST http://localhost:8090/api/v1/execution/joke
```