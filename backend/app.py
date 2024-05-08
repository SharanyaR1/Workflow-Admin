from flask import Flask, request,send_file
from flask_cors import CORS
import os
import json
from pathlib import Path
from glob import glob
import subprocess
import docker

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

client=docker.from_env()
#Function to update dependency.json file
def update_dependencies(config_file,tar,cwd):
    print("in dep func")
    with open(config_file, 'r') as f:
        config_data = json.load(f)
    # IMAGE PATH
    pth =os.path.join(cwd,tar,"image/")
    pth = os.path.normpath(pth)  # Normalize the path
    # CHART PATH
    htp=os.path.join(cwd,tar,"chart/")
    htp = os.path.normpath(htp)  # Normalize the path
    print("Image path:",pth)
    imagetar=glob(os.path.join(pth, "*.tar"))
    print("Files found in image path:", imagetar)
    if not imagetar:
        print("No .tar files found in:", pth)
        return
    image_name = os.path.basename(imagetar[0])
    print("Image name:", image_name)
    charttar=glob(os.path.join(htp, "*.tgz"))
    if not charttar:
        print("No .tgz files found in:", htp)
        return
    chart_name = os.path.basename(charttar[0])
    print("Chart name:", chart_name)
    
    

    with open('config/dependency.json', 'r+') as f:
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
                    # out=os.system("docker load --input tar/image/"+imagetar)
                    
                    # process = subprocess.run("docker load "+cwd+tar+"/image/"+image_name,capture_output=True,text=True  )
                    # process = subprocess.run("docker load --input boss/image/ss7lb.tar",capture_output=True,text=True  )
                    # print(process)
                    with open(tar+'/image/'+image_name, 'rb') as g:
                        output = client.images.load(g.read())
                        print(output[0].tags[0])
                    
                    os.system("docker tag "+output[0].tags[0]+" abbashozefa/"+mainService+":latest")
                    
                    os.system("docker push abbashozefa/"+mainService+":latest")

                    os.system("helm push "+tar+'/chart/'+chart_name+" oci://registry-1.docker.io/abbashozefa/")
                    
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
def update_bundles(config_file,tar):
    with open(config_file, 'r') as f:
        config_data = json.load(f)

    with open('config/bundle.json', 'r+') as f:
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



#Function to update the sertar_filevices.json file
def update_services(config_file,tar):
    with open(config_file, 'r') as f:
        config_data = json.load(f)

    with open('config/services.json', 'r+') as f:
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
    print(request.files)
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if 'tar' not in request.files:
        return "No tar file part", 400
    tar=request.files['tar']
    if file.filename == '' or tar.filename == '':
        return 'No selected file'
    cwd=os.getcwd()
    # Save the file to the uploads directory
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    tar_path = os.path.join('uploads', tar.filename)
    tar.save(tar_path)
    #os.system("tar -xvf " + tar_path + " -C backend/uploads/") 
    os.system("tar -xvf uploads/"+tar.filename)
    # print(tar.filename)
    tar_name=Path(tar_path).stem
    #tar_name=os.path.join('uploads', tar_name)
    print(tar_name)
    # Call the update_services function
    update_services(file_path,tar_name)

    # Call the update_dependencies function
    update_dependencies(file_path,tar_name,cwd)

    # Call the update_bundles function
    update_bundles(file_path,tar_name)

    return 'File uploaded successfully and services updated.'

@app.route('/download',methods=['POST'])
def download():
    cwd=os.getcwd()
    path = os.path.join(cwd,'standard-format.json')
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
