import os
import zipfile
from io import BytesIO
import google.generativeai as genai

# Set up GenerativeModel
api_key = "enter you gemini-api-key here"
os.environ['GOOGLE_API_KEY'] = api_key
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

# Function to parse the custom formatted response and extract features
def parse_features(response_text):
    features = {}
    current_feature = None
    current_content = []

    lines = response_text.splitlines()
    for line in lines:
        if line.startswith("**") or line.strip().isdigit():
            if current_feature:
                features[current_feature] = "\n".join(current_content).strip()
                current_content = []
            current_feature = line.strip("**").strip()
        else:
            current_content.append(line)

    if current_feature:
        features[current_feature] = "\n".join(current_content).strip()

    return features

# Read the uploaded file
file_path = 'C:/Users/ayush/PycharmProjects/pythonProject1/generated_output.txt'
with open(file_path, 'r') as file:
    content = file.read()

# Parse the features
features = parse_features(content)

# Function to generate additional information using the model
def generate_additional_info(feature_name, feature_content):
    prompt = f"Provide detailed information about the following feature: {feature_name}\n\n{feature_content}\n\nAdditional Information:"
    response = model.generate_content(prompt)
    return response.text.strip()

# Create a zip file containing all the generated files
zip_buffer = BytesIO()
with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for i, (feature_name, feature_content) in enumerate(features.items(), 1):
        # Generate additional information
        additional_info = generate_additional_info(feature_name, feature_content)

        # Save the original feature content
        original_file_name = f'feature_{i}_original.txt'
        zipf.writestr(original_file_name, f"{feature_name}\n\n{feature_content}")
        print(f"Added original file to zip: {original_file_name}")

        # Save the additional information
        additional_file_name = f'feature_{i}_additional.txt'
        zipf.writestr(additional_file_name, f"{feature_name} - Additional Information\n\n{additional_info}")
        print(f"Added additional file to zip: {additional_file_name}")

# Save the zip file in the current working directory
zip_file_path = os.path.join(os.getcwd(), 'generated_files.zip')
with open(zip_file_path, 'wb') as f:
    f.write(zip_buffer.getvalue())

print(f"Successfully created zip file: {zip_file_path}")

# Display success message
print(f"Successfully generated {len(features)} pairs of files and zipped them into: {zip_file_path}")
