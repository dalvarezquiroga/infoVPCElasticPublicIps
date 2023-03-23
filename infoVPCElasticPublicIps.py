#!/usr/bin/python3
# -*- coding: utf-8 -*-
import boto3
import yaml

# Inicialize EC2 resource.
ec2 = boto3.resource("ec2")

# Empty DICT to save AllocationId to later remove it automatically.
unused_ips = {}

# Empty DICT to save PublicIP and region to later create a summary line by line.
unused_ips_summary = {}

# Empty LIST to count the number of IPs unused.
unused_ips_counts = []

# Price Elastic IP Addresses -->  "https://aws.amazon.com/ec2/pricing/on-demand/?nc1=h_ls"
elasticipaddress_not_associated_with_a_running_instance_per_hour = 3.6 # --> 0.005*24 = 0.12 * 30 days = 3.6

"""
  Function: infoVPCElasticPublicIps()
  Input:
    AWS_PROFILE=sso-nvoperations-pu python3 infoVPCElasticPublicIps.py
  Output:
    Print the unused Public IPs.
  Descr: This script finds and deletes all unused Elastic IPs in all AWS Regions.
"""

################
# Lambda Start #
################

def handler():
    for region in ec2.meta.client.describe_regions()["Regions"]:
        region_name = region["RegionName"]
        try:
            ec2conn = boto3.client("ec2", region_name=region_name)
            addresses = ec2conn.describe_addresses(Filters=[{"Name": "domain", "Values": ["vpc"]}])["Addresses"]
            for address in addresses:
                if ("AssociationId" not in address and address["AllocationId"] not in unused_ips):
                    unused_ips[address["AllocationId"]] = region_name
                    unused_ips_summary[address["PublicIp"]] = region_name
                    unused_ips_counts.append({address['PublicIp']})
                    #### WARNING!! IF YOU UNCOMMENT THE FOLLOWING LINES IT WILL REMOVE THE IPS AUTOMATICALLY ####
                    #ec2conn.release_address(AllocationId=address["AllocationId"])  
                    #print(f"Deleted unused Elastic IP {address['PublicIp']} in region {region_name}")
        except Exception as error:
            print(f"No access to region {region_name}: {error}")

    # Count number of IPs to be deleted.
    number_of_elements = len(unused_ips_counts)

    # Calculate the cost saving with the number of IPs.
    total_cost = elasticipaddress_not_associated_with_a_running_instance_per_hour * number_of_elements

    print("--------------------------------------------")
    print(yaml.dump(unused_ips_summary))
    print("--------------------------------------------")
    print(f"SHUR! You should delete manually {len(unused_ips_counts)} unused Elastic IPs across all regions, because you can save {total_cost}$ :")

handler()
