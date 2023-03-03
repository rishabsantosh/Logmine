from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import csv
from logmine_pkg.run import run

import ibm_boto3
from ibm_botocore.client import Config, ClientError

UPLOAD_FOLDER = "./"

# The below statement creates a WSGI application, it's required because it's a standard to communicate between web server and the web application
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/") # Decorator
def welcome():
    return render_template("index.html")

@app.route("/uploadLog", methods = ["GET", "POST"])
def uploadLogFile():

    COS_API_KEY_ID = os.getenv("API_KEY")
    COS_SERVICE_ENDPOINT = os.getenv("SERVICE_ENDPOINT")
    COS_RESOURCE_INSTANCE_ID = os.getenv("RESOURCE_INSTANCE_ID")
    COS_BUCKET_NAME = os.getenv("BUCKET_NAME")

    cos = ibm_boto3.client("s3",
        ibm_api_key_id = COS_API_KEY_ID,
        ibm_service_instance_id = COS_RESOURCE_INSTANCE_ID,
        config = Config(signature_version = "oauth"),
        endpoint_url = COS_SERVICE_ENDPOINT
    )

    if request.method == "POST":
        f = request.files['file']
        fileName = secure_filename(f.filename)
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], fileName))

        # # set 5 MB chunks
        # part_size = 1024 * 1024 * 5
        
        # # set threadhold to 15 MB
        # file_threshold = 1024 * 1024 * 15

        # # set the transfer threshold and chunk size
        # transfer_config = ibm_boto3.s3.transfer.TransferConfig(
        #     multipart_threshold = file_threshold,
        #     multipart_chunksize = part_size
        # )

        # # the upload_fileobj method will automatically execute a multi-part upload
        # # in 5 MB chunks for all files over 15 MB
        # with open("./temp.log", "rb")

        filePath = "./" + fileName

        cos.upload_file(fileName, COS_BUCKET_NAME, fileName)

        print(filePath)

        return render_template("index.html", fileUploadStatus = "File Uploaded Successfully")


@app.route("/cluster", methods = ["GET"]) # Default value also is 'GET'
def logs():
    if request.method == 'GET':

        COS_API_KEY_ID = os.getenv("API_KEY")
        COS_SERVICE_ENDPOINT = os.getenv("SERVICE_ENDPOINT")
        COS_RESOURCE_INSTANCE_ID = os.getenv("RESOURCE_INSTANCE_ID")
        COS_BUCKET_NAME = os.getenv("BUCKET_NAME")

        cos = ibm_boto3.client("s3",
            ibm_api_key_id = COS_API_KEY_ID,
            ibm_service_instance_id = COS_RESOURCE_INSTANCE_ID,
            config = Config(signature_version = "oauth"),
            endpoint_url = COS_SERVICE_ENDPOINT
        )

        cos.download_file(COS_BUCKET_NAME, "Apache_2k.log", "./Apache_2k.log")

        os.system("./logmine ./Apache_2k.log -m0.5 > cout.txt")
        txt_file = open("cout.txt")
        lines = txt_file.readlines()
        # out = ""

        # for line in lines:
        #     out = out + line + '\n'
            # Try <br>, search how to add next line from python to html



        
        cnt = []
        typ = []

        for line in lines:
            cline = line.split(" ")
            cline = [i for i in cline if i != '']
            clog = cline[2:]
            cnt.append(cline[0])
            typ.append(" ".join(clog)[:-1])

        # print(cnt)
        # print(typ)

        with open("./templates/dataVis.csv", "w", newline = '') as file:
            writer = csv.writer(file)

            writer.writerow(["Count", "Message"])

            for i in range(0, len(cnt)):
                writer.writerow([cnt[i], typ[i]])



        txt_file.close()

        # return render_template("index.html", dataToRender = out)
        return render_template("index.html")


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=8080)
