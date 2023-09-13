# Testing eidos

## Running Postman Collections with Newman

This project includes a set of Postman collections that can be executed for automated testing.

### Prerequisites
- Installing [Newman](https://github.com/postmanlabs/newman)

### Running the tests
```bash
newman run tests/eidos-api-testing.postman_collection.json -e tests/development.postman_environment.json
```
