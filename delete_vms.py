#!/usr/bin/env python3
from ec2Manager import EC2Manager

ec2_manager = EC2Manager()

print("Do you want to terminate all VMs with the ids:", ec2_manager.get_current_vm_details(), "(y/n)?")

while True:
    choice = input()

    if choice.lower() == "y":
        ec2_manager.terminate_instances_by_id()
        print("Termination triggered successfully!")
        break
    elif choice.lower() == "n":
        print("Termination not triggered.")
        break
    else:
        print("Invalid option, reenter.")
