
import boto3

client = boto3.client('s3')
sts = boto3.client('sts')
sns = boto3.client('sns')
AccountID = sts.get_caller_identity()

def lambda_handler(event, context):#the main function
    
    print(event)
    s3_list =[]
       
    s3_list = get_s3_list(client)
    BucketEncryption(client, s3_list)


# a function to get all s3 buckets in an account
def get_s3_list(client):
    s3_array=[]
    extra_args ={}
   
    list_buckets = client.list_buckets()
    for bucket in list_buckets['Buckets']:
            
        s3_array.append(bucket['Name'])
            
      
    
    return s3_array



#get all buckets without serverside encryption
def BucketEncryption(client, s3_array):
    no_encryption = []
    for buckets in s3_array:
        try:
            s3_encryption = client.get_bucket_encryption(Bucket=buckets, ExpectedBucketOwner=AccountID['Account'])
            if not s3_encryption.get('ServerSideEncryptionConfiguration'):
                no_encryption.append(buckets)
        except Exception as e:
            print("failed to get encryption_buckets because of this error :", e)
            
    print("BUCKETS WITHOUT SERVERSIDE ENCRYPTION ENABLED :", no_encryption)  
    
    if len(no_encryption) >0:
        message = f"S3 Buckets with no server side encryption enabled below... \n \n"
        message += "\n".join(no_encryption)
        subject = f"S3 BUCKETS WITH NO ENCRYPTION IN THE ACCOUNT :{AccountID['Account']}"
        SNSResult = send_sns_encrypt(message, subject)
        if SNSResult:
            
            print("Notification Function Successfully triggered and send buckets with no encryption")
            return SNSResult




# sending a notification for buckets that do not have encryption
def send_sns_encrypt(message, subject):
    
    try:
        
        topic_arn = f"arn:aws:sns:af-south-1:{AccountID['Account']}:SNS_Notification_for_S3Encryption"
        result = sns.publish(TopicArn=topic_arn, Message=message, Subject=subject)
        if result['ResponseMetadata']['HTTPStatusCode']==200:
                
            print(result)
            print("Bucket Encryption Notification Send Successfully..!!!")
            return True
         
            
            
    except Exception as e:
        
        print("Error occured while publish while publish notification and error is :", e)
        return True






   