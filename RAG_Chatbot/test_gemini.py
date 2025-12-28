
import os
from google.genai import Client

print("STARTING TEST")

api_key = "AIzaSyCHvMRb1YGBUx9rL-RAL1pM3inw-kb7YZE"
print("API KEY FOUND:", bool(api_key))

client = Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Say hello in one word"
)

print("RAW RESPONSE:", response)
print("TEXT RESPONSE:", response.text)

print("TEST COMPLETED")
