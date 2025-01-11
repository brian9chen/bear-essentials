import csv
import openai
import requests
import os

# implements openai api to generate images based on product descriptions.  

openai.api_key = ""  # commented out for privacy 
CSV_FILE_PATH = 'Products.csv'  
save_to = os.path.dirname(__file__)  # Save the images 

def generate_image_from_description(name, description, img_name):
    try:
        response = openai.Image.create(
            prompt=f"{name}: {description}",
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']

        # Download  image
        img_data = requests.get(image_url).content
        img_path = os.path.join(save_to, img_name)  # Save in the same folder as images.py

        # Save  image to folder
        with open(img_path, 'wb') as file:
            file.write(img_data)

        print(f"Image for {name} saved as {img_name}")
        return img_name
    except Exception as e:
        print(f"Error generating image for {name}: {e}")
        return None

# process the CSV and generate images
def process_products():
    with open(CSV_FILE_PATH, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Iterate through each row of the CSV
        for row in reader:
            product_name = row.get('product_name', '').strip()  
            product_description = row.get('description', '').strip()
            img_name = row.get('img_name', '').strip()

            # Check for missing or NULL values
            if not product_name or not product_description or not img_name or img_name.lower() == 'null':
                print(f"Skipping row with missing data: {row}")
                continue  

            print(f"Generating image for: {product_name}, Description: {product_description}, Image: {img_name}")
            
            # Generate 
            generate_image_from_description(product_name, product_description, img_name)

if __name__ == "__main__":
    process_products()
