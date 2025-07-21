Run with:

```bash
docker build -t eidos-joke .
docker run --rm -p 8090:80 eidos-joke
```

Example:

```bash
curl -X POST http://localhost:8090/api/v1/execution/joke
```

To test an example of a LLM-powered agent, you can execute the example provided in `chat.py`.

```bash
pip install "streamlit>=1.44.0" "openai>=1.0.0"
export OPENAI_API_KEY=your_openai_api_key
streamlit run chat.py
```