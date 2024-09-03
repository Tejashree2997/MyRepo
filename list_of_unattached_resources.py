#!/usr/bin/env python3


# Imports values
import cred_values
# To create a csv file
import subprocess
import json
import csv
import time

# Imports all the credential values from the module.
from cred_values import *
from datetime import datetime
# Provide Authentication support.
from azure.identity import ClientSecretCredential
# Provide operations for managing resources.
from azure.mgmt.resource import ResourceManagementClient
# Provide operations for managing computing resources.
from azure.mgmt.compute import ComputeManagementClient
# Provide operations for managing networking resources.
from azure.mgmt.network import NetworkManagementClient
# Provide operations for managing ACR resources.
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from azure.mgmt.containerregistry.v2019_05_01_preview import ContainerRegistryManagementClient

# Get a creadentials
credential = ClientSecretCredential(
	cred_values.TENANT_ID,
	cred_values.CLIENT,
	cred_values.KEY
)

# Creating an object of resource client.
Resource_client = ResourceManagementClient(credential, subscription_id)
# Creating an object of compute resources.
compute_client = ComputeManagementClient(credential, subscription_id)
# Creating an object of network resources.
Network_client = NetworkManagementClient(credential,subscription_id)
# Creating an object of ACR resources.
acr_client = ContainerRegistryManagementClient(credential, subscription_id)

# Function to get unattached Disk
def get_unattached_disk():
	
	csv_rows = []
	for disk in compute_client.disks.list():
		if(disk.managed_by is None):
			array = disk.id.split("/")
			resource_group = array[4]
			row = [resource_group,disk.name]
			csv_rows.append(row)
	filename = datetime.now().strftime('/home/Tejashri/Unattached-Resources/unattached_disk_%d%m%Y.csv')
	with open(filename,'w') as fp:
		writer=csv.writer(fp,delimiter=",")
		writer.writerow(["RG","DISK-NAME"])
		writer.writerows(csv_rows)
		fp.close()

# Function to get unattached NIC  
def get_unattached_nic():
	csv_rows = []
	for nic in Network_client.network_interfaces.list_all():
		array=nic.id.split("/")
		Resource_group=array[4]
		network_interface = Network_client.network_interfaces.list(Resource_group)
		Unattached=nic.virtual_machine
		if Unattached==None:
			row = [Resource_group,nic.name]
			csv_rows.append(row)
	filename = datetime.now().strftime('/home/Tejashri/Unattached-Resources/unattached_nic_%d%m%Y.csv')
	with open(filename,'w') as fp:
		writer=csv.writer(fp,delimiter=",")
		writer.writerow(["RG" , "NIC-NAME"])
		writer.writerows(csv_rows)
		fp.close()
      
# Function to get unattached NSG
def get_unattached_nsg():
	csv_rows = []
	for nsg in Network_client.network_security_groups.list_all():
		array=nsg.id.split("/")
		Resource_group=array[4]
		if(nsg.subnets is None) and (nsg.network_interfaces is None) :
			row = [Resource_group,nsg.name]
			csv_rows.append(row)
	filename = datetime.now().strftime('/home/Tejashri/Unattached-Resources/unattached_nsg_%d%m%Y.csv')
	with open(filename,'w') as fp:
		writer=csv.writer(fp,delimiter=",")
		writer.writerow(["RG","NSG-NAME"])
		writer.writerows(csv_rows)
		fp.close()

# Function to get unattached IP'S
def get_unattached_ips():
	csv_rows = []
	for ip in Network_client.public_ip_addresses.list_all():
		array=ip.id.split("/")
		Resource_group=array[4]
		if(ip.ip_address is None):
			row = [Resource_group,ip.name]
			csv_rows.append(row)
	filename = datetime.now().strftime('/home/Tejashri/Unattached-Resources/unattached_ip_%d%m%Y.csv')
	with open(filename,'w') as fp:
		writer=csv.writer(fp,delimiter=",")
		writer.writerow(["RG" , "IP-NAME"])
		writer.writerows(csv_rows)
		fp.close()

def get_unattached_snapshots():
    csv_rows = []
    for snapshot in compute_client.snapshots.list():
        if snapshot.managed_by is None:  # Check if the snapshot is not attached to any resource
            array = snapshot.id.split("/")
            resource_group = array[4]
            row = [resource_group, snapshot.name]
            csv_rows.append(row)
    filename = datetime.now().strftime('/home/Tejashri/Unattached-Resources/unattached_snapshots_%d%m%Y.csv')
    with open(filename, 'w') as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerow(["RG", "SNAPSHOT-NAME"])
        writer.writerows(csv_rows)
        fp.close()

def get_unattached_images():
    csv_rows = []
    for image in compute_client.images.list():
        if image.storage_profile.os_disk.managed_disk is None:  # Check if the image is not attached to any managed disk
            array = image.id.split("/")
            resource_group = array[4]
            row = [resource_group, image.name]
            csv_rows.append(row)
    filename = datetime.now().strftime('/home/Tejashri/Unattached-Resources/unattached_images_%d%m%Y.csv')
    with open(filename, 'w') as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerow(["RG", "IMAGE-NAME"])
        writer.writerows(csv_rows)
        fp.close()

def list_untagged_acr_images(registry_name):
    csv_rows = []

    # Get a list of repositories in the registry
    command_repos = f"az acr repository list -n relidacr --output json"
    repositories = json.loads(subprocess.check_output(command_repos, shell=True))

    for repository in repositories:
        # Get a list of manifests in the repository
        command_manifests = f"az acr repository show-manifests -n {registry_name} --repository {repository} --output json"
        manifests = json.loads(subprocess.check_output(command_manifests, shell=True))

        for manifest in manifests:
            if not manifest.get('tags'):  # Check if the manifest has no tags
                row = [registry_name, repository, manifest['digest']]
                csv_rows.append(row)

    filename = datetime.now().strftime('/home/Tejashri/Unattached-Resources/untagged_acr_images_%d%m%Y.csv')
    with open(filename, 'w') as fp:
        writer = csv.writer(fp, delimiter=",")
        writer.writerow(["Registry", "Repository", "Manifest Digest"])
        writer.writerows(csv_rows)
        fp.close()


#def list_untagged_acr_images():
   # csv_rows = []
   # for registry in acr_client.registries.list():
    #    resource_group = registry.id.split("/")[4]
     #   for repository in acr_client.registries.list_repository_names(resource_group, registry.name).repositories:
      #      for tag in acr_client.registries.list_tags(resource_group, registry.name, repository).tags:
       #         if tag.name == "<none>":
        #            row = [registry.name, repository]
         #           csv_rows.append(row)
    
    #filename = datetime.now().strftime('/home/Tejashri/Unattached-Resources/untagged_acr_images_%d%m%Y.csv')
    #with open(filename, 'w') as fp:
     #   writer = csv.writer(fp, delimiter=",")
      #  writer.writerow(["Registry", "Repository"])
       # writer.writerows(csv_rows)
        #fp.close()

get_unattached_disk()
get_unattached_nic()
get_unattached_nsg()
get_unattached_ips()
get_unattached_snapshots()
get_unattached_images()
list_untagged_acr_images('relidacr')








