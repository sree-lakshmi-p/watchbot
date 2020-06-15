import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = '***********************************'
SECRET_KEY = '***********************************'



def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        upload=s3.upload_file(local_file, bucket, s3_file,ExtraArgs={'ACL':'public-read'})
        print("Upload Successful"+s3_file)
	location = s3.get_bucket_location(Bucket=bucket)['LocationConstraint']
	s3_file=s3_file.replace(":","%3A")
	s3_file=s3_file.replace(" ","+")
	url = "https://%s.s3.%s.amazonaws.com/%s" % (bucket,location,s3_file)
        return url
    #except FileNotFoundError:
    #    print("The file was not found")
    #    return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


#function call is as follows
#uploaded = upload_to_aws('/home/jarvis3000/Pictures/Wallpapers/1.jpg', 'projectasiet', 'pictures')
