# infoVPCElasticPublicIps


![Cost](/assets/aws-costs.jpp)

 We want reduce costs in our AWS account. Normally in DEVs accounts we have some IP Adress that users forget to delete and it doesn't remove automatically when you destroy an EC2 Instance (It depends).

This small script help you to identify them to take some action.

Your boss Finance will appreciate it ;-)

# Technologies we’ll use:

*  AWS API (EC2)
*  Python3.9


```bash
https://linuxhostsupport.com/blog/how-to-install-python-3-9-on-ubuntu-20-04/ (Google)
```

# Pre-requisites:
```bash
pip3 install boto3
pip3 install pyyaml
```

# Deploy:

You have 2 versions:

* infoVPCElasticPublicIps.py -------> To be executed in your local bash or any other bash with cli and login credentials.
* infoVPCElasticPublicIps_sns.py  --> Execution in a Lambda and integration with SNS AWS to send a report periodically (use Eventbridge service).

```
#### WARNING!! IF YOU UNCOMMENT THE FOLLOWING LINES IT WILL REMOVE THE IPS AUTOMATICALLY ####
#ec2conn.release_address(AllocationId=address["AllocationId"])  
#print(f"Example message --> Deleted unused Elastic IP {address['PublicIp']} in region {region_name}")
```

You can uncomment these lines if you allow the script to remove the IPs. 
Please be sure before running it.

```bash
AWS_PROFILE=XXX python3 infoVPCElasticPublicIps.py
```

![Deploy](/assets/deploy1.PNG)

# Testing

If everything is working well, we will see a output in your terminal:

```
52.208.38.33: eu-west-1
52.209.205.209: eu-west-1
52.210.133.90: eu-west-1
52.211.160.89: eu-west-1
52.212.148.88: eu-west-1
52.212.209.126: eu-west-1
```

# Licence

MIT

![Result](/assets/meme.gif)

# Information

More info -->

Original script https://github.com/dannysteenman/aws-toolbox/blob/main/ec2/delete_all_unused_elastic_ips.py from Danny Steenman.

https://www.kodyaz.com/aws/send-sns-notification-from-aws-lambda-function-using-python.aspx

https://mkdev.me/posts/how-to-send-sms-messages-with-aws-lambda-sns-and-python-3

David Álvarez Quiroga
