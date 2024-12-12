import boto3
s3 = boto3.resource('s3')
# Get list of objects for indexing
images = [('image1.jpeg','Ravi Ashwin'),
          ('image2.jpg','Sachin Tendulkar'),
          ('image3.jpg','Rohit Sharma'),
          ('image4.jpg','Bhvaneshwar Kumar'),
          ('image5.jpg','Rahul David'),
          ('image6.jpg','Smriti mandhana'),
          ('image7.jpg','P V Sindhu')
          ]
# Iterate through list to upload objects to S3
for image in images:
    file = open(image[0],'rb')
    object = s3.Object('umkc-images','index/'+ image[0])
    ret = object.put(Body=file,
                    Metadata={'FullName': image[1]})