from flask import Flask, request
import os
import json

app = Flask(__name__)


#Function to update dependency.json file
def update_dependencies(config_file):
    with open(config_file, 'r') as f:
        config_data = json.load(f)

    with open('backend/config/dependency.json', 'r+') as f:
        dependency_data = json.load(f)

        for item in config_data:
            if 'serviceLibrary' in item and 'dependency' in item:
                serviceLibrary = item.get('serviceLibrary')
                dependency = item.get('dependency')
                mainService = dependency.get('mainService')

                # Check if the mainService already exists
                existing_dependency_index = next((i for i, dep in enumerate(dependency_data) if dep.get('serviceLibrary') == serviceLibrary and dep['dependency'].get('mainService') == mainService), None)

                if existing_dependency_index is not None:
                    # Overwrite existing dependency
                    dependency_data[existing_dependency_index]['dependency'] = dependency
                else:
                    # Add new dependency
                    dependency_data.append({
                        "serviceLibrary": serviceLibrary,
                        "dependency": dependency
                    })

        # Move pointer to the beginning of the file
        f.seek(0)
        # Write updated dependency data back to dependency.json
        json.dump(dependency_data, f, indent=4)
        # Truncate the file to remove any remaining content
        f.truncate()



 



# Function to update the bundles.json file
def update_bundles(config_file):
    with open(config_file, 'r') as f:
        config_data = json.load(f)

    with open('backend/config/bundle.json', 'r+') as f:
        bundles_data = json.load(f)

        for item in config_data:
            if 'bundles' in item:
                bundle_name = item.get('bundles')
                services = item.get('services')
                optional_service = item.get('optionalService')

                existing_bundle = next((bundle for bundle in bundles_data if bundle.get('bundles') == bundle_name), None)

                if existing_bundle is None:
                    # Add new bundle if not present
                    bundles_data.append(item)
                else:
                    # Check if services match
                    existing_services = existing_bundle.get('services', [])
                    if existing_services != services:
                        # If services don't match, add a new item
                        bundles_data.append(item)
                    else:
                        # If services match, update optionalService
                        existing_bundle['optionalService'] = optional_service
                       

        # Move pointer to the beginning of the file
        f.seek(0)
        # Write updated bundles data back to bundles.json
        json.dump(bundles_data, f, indent=4)
        # Truncate the file to remove any remaining content
        f.truncate()



#Function to update the services.json file
def update_services(config_file):
    with open(config_file, 'r') as f:
        config_data = json.load(f)

    with open('backend/config/services.json', 'r+') as f:
        services_data = json.load(f)

        for item in config_data:
            if 'serviceLibrary' in item and 'serviceName' in item:
                serviceLibrary = item.get('serviceLibrary')
                serviceName = item.get('serviceName')
                for service in services_data:
                    if service.get('serviceLibrary') == serviceLibrary and service.get('serviceName') == serviceName:
                        # Update existing service
                        service['vCPU'] = item.get('vCPU')
                        service['RAM'] = item.get('RAM')
                        service['TPS'] = item.get('TPS')
                        break
                else:
                    # Add new service
                    services_data.append(item)

        # Move pointer to the beginning of the file
        f.seek(0)
        # Write updated services data back to services.json
        json.dump(services_data, f, indent=4)
        # Truncate the file to remove any remaining content
        f.truncate()

@app.route('/')
def main():
    return "Hello, welcome to the file upload page!"



#Function to upload the config file from the admin
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    # Save the file to the uploads directory
    file_path = os.path.join('backend','uploads', file.filename)
    file.save(file_path)

    # Call the update_services function
    update_services(file_path)

    # Call the update_dependencies function
    update_dependencies(file_path)

    # Call the update_bundles function
    update_bundles(file_path)

    return 'File uploaded successfully and services updated.'

if __name__ == '__main__':
    app.run(debug=True)
