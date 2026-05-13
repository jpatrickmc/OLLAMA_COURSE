# OLLAMA-COURSE

A Python project for learning and working with Ollama.

## Prerequisites

1. **Install Ollama**: Download and install Ollama from [https://ollama.ai](https://ollama.ai)
2. **Python 3.7+**: Make sure Python is installed on your system

## Setup Instructions

### 1. Activate the Virtual Environment

```bash
# Navigate to the project directory
cd /Users/patrickmcdaniel/Desktop/OLLAMA-COURSE

# Activate the virtual environment
source venv/bin/activate
```

### 2. Install Dependencies (if needed)

If you're setting up on a new machine or the dependencies aren't installed:

```bash
pip install -r requirements.txt
```

### 3. Start Ollama Service

In a separate terminal window, start the Ollama service:

```bash
ollama serve
```

### 4. Pull a Model

Before running the script, you need to pull a model. For example:

```bash
ollama pull llama2
```

Other popular models:

- `ollama pull mistral`
- `ollama pull codellama`
- `ollama pull llama3`

### 5. Run the Script

```bash
python main.py
```

## Project Structure

```
OLLAMA-COURSE/
├── venv/              # Virtual environment (not tracked in git)
├── main.py            # Main Python script with Ollama examples
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## Usage Examples

The `main.py` script includes three examples:

1. **Simple Chat Completion**: Basic question-answer interaction
2. **Streaming Response**: Real-time streaming of responses
3. **Text Generation**: Generate text from a prompt

## Deactivating the Virtual Environment

When you're done working:

```bash
deactivate
```

## Troubleshooting

- **Connection Error**: Make sure Ollama service is running (`ollama serve`)
- **Model Not Found**: Pull the model first (`ollama pull llama2`)
- **Import Error**: Activate the virtual environment and ensure dependencies are installed

## Next Steps

- Explore different models available in Ollama
- Modify the examples in `main.py` to suit your needs
- Check out the [Ollama Python library documentation](https://github.com/ollama/ollama-python)
