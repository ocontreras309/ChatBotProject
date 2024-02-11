from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

with open('finetunes_train.jsonl', 'rb') as file:
    training_file = client.files.create(file=file, purpose='fine-tune')
    
with open('finetunes_val.jsonl', 'rb') as file:
    validation_file = client.files.create(file=file, purpose='fine-tune')

response = client.fine_tuning.jobs.create(
    training_file=training_file.id,
    validation_file=validation_file.id,
    model='gpt-3.5-turbo',
    suffix='UMSS-assistant'
)
