AWS EC2 Infrastructure Creation using Azure DevOps Pipeline

1. Introduction:
 This document provides a step-by-step guide for creating AWS EC2 infrastructure using Azure DevOps pipelines. The guide is organized into three sections, each with its own folder for creating and deleting AWS resources.

2. Prerequisites Before beginning, ensure the following prerequisites are met:
    1. Permission to access Azure DevOps Organization
    2. AWS credentials with appropriate permissions
    3. Azure DevOps Service Connection to AWS
    4. Azure DevOps Service Connection to Azure
    5. Installed Azure CLI

3. Folder Structure in Azure Repos (Master Branch)
/RELID-EC2-INSTANCE
/MTD-EC2-INSTANCE
/DELETE-RESOURCES
Each folder contains the necessary YAML scripts and pipeline configurations for managing AWS EC2 instances.

4. Variable-Group Structure We have four variable groups in the Azure DevOps Library, specifically for each folder mentioned above.
    1. RELID-INSTANCE-DETAILS: Contains the required information in the form of variables for creating RELID instances, such as:
        AWS Credentials: User AWS login credentials
        Name: Name of the instance
        Region: Region name in which the instance will be created
        AMI ID: OS image ID
        Instance-count: No. of instances required
        Instance Configuration: Instance type
        Disk Size: Default 30GB, can be changed as per requirement
        Ports: RELID ports to be opened
        Creation Date: Date of the instance creation
        Owner: Name of the person who requested the instance

    Note: AMI ID changes as per the region and OS.

    2. MTD-INSTANCE-DETAILS: Contains the required information for creating an MTD instance with multiple configuration details and MTD ports to be opened.
    
    3. MTD-SINGLE-INSTANCE-DETAILS: Contains the required information for single MTD instance creation.

    4. RESOURCE-DELETION-DETAILS: Contains all the information needed to delete the resource in the form of variables.

5. Pipeline Configuration
    1. relid-instance-creation: This folder contains the scripts and pipeline configuration for creating RELID instances. We have two separate pipelines for the creation of instances with the below YAML configurations. Pipelines are triggered as per requests raised by the QA team. For example, if QA raises a request for a RELID instance with a Load Balancer configured, then we will trigger the pipeline which will create a RELID EC2 instance with the Load Balancer configured and vice versa.
    Below are the resources that get created using the pipeline:
        EC2 Instance
        SSH key to access the instance
        Volume
        Security Group
        Load Balancer if requested
    There are two YAML configurations for creating EC2 resources as follows:
        RELID-EC2-INSTANCE-WITHOUT-LB.yaml: This YAML configuration creates only RELID EC2 instances.
        RELID-EC2-INSTANCE-WITH-LB.yaml: This YAML configuration creates RELID instances with LB configured.

    2. mtd-instance-creation: This folder contains the scripts and pipeline configuration for creating MTD instances. There are three YAML configurations for creating MTD instances with or without a Load Balancer. We have three separate pipelines for the creation of instances with the above YAML configurations. Pipelines are triggered as per request. For example, if QA raises a request for MTD instances with two different configurations (instance types) of EC2 instances, then we will trigger the pipeline which will create MTD EC2 instances with different configurations.
    There are two YAML configurations for creating EC2 resources as follows:
        MTD-EC2-INSTANCE-WITHOUT-LB.yaml: This YAML configuration creates multiple MTD instances with different configurations.
        MTD-EC2-INSTANCE-WITH-LB.yaml: This YAML configuration creates multiple MTD instances with LB configured.
        MTD-EC2-SINGLE-INSTANCE.yaml: This YAML configuration creates a single MTD instance.

    3. resource-deletion: This folder contains the scripts and pipeline configuration for deleting resources. This script will delete all resource instances, be it MTD or RELID. We just have to manually change the instance name to be deleted and the region of the resource in the RESOURCE-DELETION-DETAILS variable group.

6. Pipelines We have a total of 6 pipelines as follows:
    1. RELID-EC2-INSTANCE-WITHOUT-LB CREATION PIPELINE: This pipeline will create single or multiple RELID EC2 instances without LB.
    2. RELID-EC2-INSTANCE-WITH-LB CREATION PIPELINE: This pipeline will create single or multiple RELID EC2 instances with LB configured.
    3. MTD-EC2-INSTANCE-WITHOUT-LB CREATION PIPELINE: This pipeline will create multiple MTD EC2 instances without LB.
    4. MTD-EC2-INSTANCE-WITH-LB CREATION PIPELINE: This pipeline will create multiple MTD EC2 instances with LB configured.
    5. MTD-EC2-SINGLE-INSTANCE CREATION PIPELINE: This pipeline will create a single MTD EC2 instance.
    6. RESOURCE DELETION PIPELINE: This pipeline will delete single/multiple EC2 instances with all the associated resources.


7. Run Pipeline

    Note:  Before triggering the pipeline, ensure that the instance details related changes have been made in the respective variable group as per requirement.
    
    Note:  AWS credentials need to be changed as per the person who is triggering the pipeline.
    
    Navigate to Pipelines:
    1. Go to Pipelines in Azure DevOps.
    2. Manually trigger each pipeline:
    3. Select a pipeline (e.g., RELID-EC2-INSTANCE-WITHOUT-LB CREATION PIPELINE).
    4. Click "Run pipeline" to start the process.
    5. Repeat this for mtd-instance-creation and resource-deletion as per requirement.
    6. Verify the creation and deletion of AWS resources:
    7. Ensure that the pipelines run successfully and that the AWS resources are created and deleted as expected.

8. Conclusion
     By following the above steps, you can efficiently create and manage AWS EC2 infrastructure using Azure DevOps pipelines. Each folder (relid-instance-creation, mtd-instance-creation, and resource-deletion) has its own pipeline, ensuring modular and organized infrastructure management.