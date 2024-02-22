# aws-server-side-encryption

**s3-encryption-bucket.yaml**
  this template basically just create aws s3 bucket with configured metadata

 **sns-for-s3-encryption.yaml**
    the template create a subscription and its topic that will be forwarding messages according to how it is configured. is important to note that the sns can only 
    be triggered by Lambda function when certain conditions are breached


**s3-encryption-lambda.yaml**
  this template is the core of the solution project. this is where the core of the project is configured and every resource properly linked to the right resource to 
  make sure that everything works fine. especially when it comes to matters of IAM roles and permissions and access. from parameters, roles, permissions, schedule 
  and events and the specific function are all created or linked in this template.

  it is also important to note that permission boundary policy is already created in the accounts. if you want to use the templates, your own account might not need 
  it or have it, so you can remove the line or just use comments so that CloudFormation won't demand it.


 **s3-encryption.py**
    1. this is the actuall Lambda function code in Python. to explain the code in short:
    2. firstly i declare python client libraries that are needed for the code to run properly.
    3. lambda_handler function is straight forward, it just triggers other functions that need to execute
    4. get_s3_list function basically just gets all buckets available in the account, filter using the name of the bucket and add the buckets in an array list.
    5. bukectEncryption function it uses the list from above mentioned function, to check on every bucket if there's server-side-encrytion, otherwise add the 
        buckets into anoter array list
    6 send_sns_encrypt function gets triggered only if there are buckets with no encryption as specified above to the configured sns topic

    7. exclusion but important. the enforcing of the encryption step is commented but if you want to enforce encryption, the comment part can be removed and it 
       works just fine.
 
