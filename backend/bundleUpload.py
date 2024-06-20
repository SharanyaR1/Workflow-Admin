from flask import Flask, request,send_file
from flask_cors import CORS
import os
import json
from pathlib import Path
from glob import glob

app=Flask(__name__)
CORS(app)   # This will enable CORS for all routes


# Function to update the bundles.json file
def update_bundles(config_file):
    with open(config_file, 'r') as f:
        config_data = json.load(f)

    with open('/home/anisha7/Videos/latest/Nokia_DSA/dimensioningbackend/config/servicesBundle.json', 'r+') as f:
        bundles_data = json.load(f)

        for item in config_data:
            if 'bundles' in item:
                bundle_name = item.get('bundles')
                services = item.get('services')
                optional_service = item.get('optionalService')

                existing_bundle = next((bundle for bundle in bundles_data if bundle.get('bundles') == bundle_name), None)
                print(existing_bundle)
                if existing_bundle is None:
                    # Add new bundle if not present
                    bundles_data.append(item)
                else:
                    # Check if services match
                    existing_services = [bundle['services'] for bundle in bundles_data if bundle.get('bundles') == bundle_name]
                    existing_optservices = [bundle['optionalService'] for bundle in bundles_data if bundle.get('bundles') == bundle_name]
                    print(existing_services)
                    if services not in existing_services[0]:
                        # If services don't match, add a new item
                        # bundles_data.append(item)
                        existing_bundle['services'].append(services)
                    if optional_service not in existing_optservices[0]:
                        # If services match, update optionalService
                        # existing_update=[bundle['services'] for bundle in bundles_data if bundle.get('bundles') == bundle_name]
                        existing_bundle['optionalService'].append(optional_service)
                       

        # Move pointer to the beginning of the file
        f.seek(0)
        # Write updated bundles data back to bundles.json
        json.dump(bundles_data, f, indent=4)
        # Truncate the file to remove any remaining content
        f.truncate()


@app.route('/')
def main():
    return "Hello, welcome to the file bundle upload page!"



#Function to upload the bundle config file 
@app.route('/upload', methods=['POST'])
def upload_file():
     
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
     
    if file.filename == '':
        return 'No selected file'
    cwd=os.getcwd()

    # Save the file to the uploads directory
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    print("The file path is: ",file_path)

    # Call the update_bundles function
    update_bundles(file_path)

    return 'File uploaded successfully and services updated.'

@app.route('/download',methods=['POST'])
def download():
    cwd=os.getcwd()
    path = os.path.join(cwd,'standard-bundle.json')
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(port=5006,debug=True)