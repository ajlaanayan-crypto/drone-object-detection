import 
pip install openai-whisper


model = whisper.load_model("base")

def transcribe(file="input.wav"):
    result = model.transcribe(file)
    return result["text"].lower()