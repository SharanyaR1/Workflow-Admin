from flask import Flask, request,send_file
from flask_cors import CORS
import os,docker
import json
from pathlib import Path
from glob import glob
import subprocess


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

client=docker.from_env()

#Function to update dependency.json file
def update_dependencies(config_file,tar,cwd):
    print("in dep func")
    with open(config_file, 'r') as f:
        config_data = json.load(f)
    # IMAGE PATH
    pth =os.path.join(cwd,tar,"images/")
    pth = os.path.normpath(pth)  # Normalize the path
    # CHART PATH
    htp=os.path.join(cwd,tar,"charts/")
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
    
    
    #/home/anisha7/Videos/latest/Nokia_DSA/dimensioningbackend/config/dimensioning-services.services-req.json
    with open('/home/anisha7/Videos/latest/Nokia_DSA/dimensioningbackend/config/dimensioning-services.services-req.json', 'r+') as f:
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
                    with open(tar+'/images/'+image_name, 'rb') as g:
                        output = client.images.load(g.read())
                        print(output[0].tags[0])
                    
                    os.system("docker tag "+output[0].tags[0]+" dsanokia/"+mainService+":latest")
                    
                    os.system("docker push dsanokia/"+mainService+":latest")

                    os.system("helm push "+tar+'/charts/'+chart_name+" oci://registry-1.docker.io/dsanokia/")
                    
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


#Function to update bundles in in bundleUpload.py file


#Function to update the sertar_filevices.json file
def update_services(config_file,tar,cwd):
    print("In service function")
    with open(config_file, 'r') as f:
        config_data = json.load(f)

    # IMAGE PATH
    pth =os.path.join(cwd,tar,"images/")
    pth = os.path.normpath(pth)  # Normalize the path
    # CHART PATH
    htp=os.path.join(cwd,tar,"charts/")
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

    #/home/anisha7/Videos/latest/Nokia_DSA/dimensioningbackend/config/dimensioning-services.services-dependency.json
    with open('/home/anisha7/Videos/latest/Nokia_DSA/dimensioningbackend/config/dimensioning-services.services-dependency.json', 'r+') as f:
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
                    with open(tar+'/images/'+image_name, 'rb') as g:
                        output = client.images.load(g.read())
                        print(output[0].tags[0])
                    
                    os.system("docker tag "+output[0].tags[0]+" dsanokia/"+serviceName+":latest")
                    
                    os.system("docker push dsanokia/"+serviceName+":latest")

                    os.system("helm push "+tar+'/charts/'+chart_name+" oci://registry-1.docker.io/dsanokia/")
                    

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
    if 'tar' not in request.files:
        return "No tar file part", 400
    tar=request.files['tar']
    if file.filename == '' or tar.filename == '':
        return 'No selected file'
    cwd=os.getcwd()

    # Save the file to the uploads directory
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    print("The file path is: ",file_path)

    tar_path = os.path.join('uploads', tar.filename) #hc
    tar.save(tar_path)
    print("The tar path is: ",tar_path)

    os.system("tar -xvf uploads/"+tar.filename) #Untar
    tar_name=Path(tar_path).stem

    # Call the update_services function
    update_services(file_path,tar_name,cwd)

    # Call the update_dependencies function
    update_dependencies(file_path,tar_name,cwd)

    return 'File uploaded successfully and services updated.'

@app.route('/download',methods=['POST'])
def download():
    cwd=os.getcwd()
    path = os.path.join(cwd,'standard-format.json')
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True,port=5005)
