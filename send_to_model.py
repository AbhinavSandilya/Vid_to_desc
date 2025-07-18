# from google.cloud import aiplatform
# import os

# # --- STEP 1: Initialize Vertex AI ---
# aiplatform.init(project="your-gcp-project-id", location="us-central1")

# # --- STEP 2: Load Transcribed Text ---
# with open("transcription.txt", "r") as f:
#     input_text = f.read()

# # --- STEP 3: Call Fine-Tuned Model ---
# model = aiplatform.TextGenerationModel(
#     model_name="7827021956393205760",  # Your fine-tuned model ID
#     tuning_job=None  # Set to None for already tuned model
# )

# response = model.predict(input_text)

# # --- STEP 4: Save Output to TXT File ---
# with open("output.txt", "w", encoding="utf-8") as f:
#     f.write(response.text)

# print("✅ Model response saved to output.txt")


# send_to_model.py


# from google.cloud import aiplatform
# import os

# def call_vertex_model():
#     # --- STEP 1: Initialize Vertex AI ---
#     aiplatform.init(project="your-gcp-project-id", location="us-central1")

#     # --- STEP 2: Load Transcribed Text ---
#     with open("transcription.txt", "r") as f:
#         input_text = f.read()

#     # --- STEP 3: Call Fine-Tuned Model ---
#     model = aiplatform.TextGenerationModel(
#         model_name="7827021956393205760",
#         tuning_job=None
#     )

#     response = model.predict(input_text)

#     # --- STEP 4: Save Output to TXT File ---
#     with open("output.txt", "w", encoding="utf-8") as f:
#         f.write(response.text)

#     print("✅ Model response saved to output.txt")
#     return response.text


from vertexai.preview.language_models import TextGenerationModel
from vertexai import init

# Step 1: Initialize Vertex AI
init(project="local-bliss-465905-r3", location="us-central1")  # update with your project

# Step 2: Load the model
model = TextGenerationModel.from_pretrained("text-bison@001")  # Update model ID if needed

# Step 3: Read transcription
with open("transcription.txt", "r", encoding="utf-8") as f:
    input_text = f.read()

# Step 4: Generate response
response = model.predict(input_text)

# Step 5: Save response
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(response.text)

print("✅ Model response saved to output.txt")

