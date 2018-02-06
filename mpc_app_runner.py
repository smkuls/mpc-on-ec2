#!/usr/bin/env python3
from ec2Manager import EC2Manager
import time
import os
import threading


def viff_app_runner_helper(ec2Manager, instance_ids, instance_ips, viff_app):

    port_numbers = [9000+i for i in range(1, ec2Manager.config.VM_COUNT + 1)]
    n = ec2Manager.config.VM_COUNT
    # kill_previous_processes = "killall python"
    for player_number, instance_id in zip(range(1, n + 1), instance_ids):
        viff_config_command = ("python ~/viff/apps/generate-config-files.py " +
                "-n " + str(n) + " -t 1")
        for port_number, instance_ip in zip(port_numbers, instance_ips):
            viff_config_command += " " + instance_ip+":"+str(port_number)

        viff_app_command = ("python ~/viff/apps/" + viff_app +" --no-ssl " +
                "--statistics --deferred-debug player-" + str(player_number) +
                ".ini > output 2>&1 &")

        print(viff_config_command)
        print(viff_app_command)
        # ec2Manager.execute_command_on_instance(instance_id,
            # [kill_previous_processes, viff_config_command, viff_app_command])
        ec2Manager.execute_command_on_instance(instance_id,
                [viff_config_command, viff_app_command])

def spdz_app_runner_helper(ec2Manager, instance_ids, instance_ips, app_name):
    root_instance_ip = instance_ips[0]
    root_instance_id = instance_ids[0]
    total_instances = len(instance_ids)
    
    script_command = 'cd ~/spdz-2; sh Scripts/setup-online.sh ' + str(total_instances) + " 128 40"

    ec2Manager.execute_command_on_instance(root_instance_id, [script_command])
    scp_command = ("rm -rf .downloaded/; mkdir .downloaded; scp -q -o StrictHostKeyChecking=no  -r -i " +
            ec2Manager.config.KEY_FILE_PATH + " ec2-user@" + root_instance_ip + ":~/spdz-2/Player-Data" +
            " .downloaded")
    # print (scp_command)
    os.system(scp_command)


    root_machine_commands = [('cd ~/spdz-2; python compile.py ' + app_name +
            '; ./Server.x ' + str(total_instances) + ' 5000 &'
            + ' ./Player-Online.x -pn 5000 -h ' + root_instance_ip
            + ' 0 ' + app_name)]
    print(root_machine_commands)

    root_machine_thread = threading.Thread(target=ec2Manager.execute_command_on_instance,
            args = [root_instance_id, root_machine_commands, False, True])
    root_machine_thread.start()

    client_machine_threads = []

    for i in range(len(instance_ids[1:])):
        os.system("scp -q -o StrictHostKeyChecking=no -i " + ec2Manager.config.KEY_FILE_PATH + " -r .downloaded/Player-Data ec2-user@" +
                instance_ips[i+1]+":~/spdz-2")
        other_machine_commands = [('cd ~/spdz-2; python compile.py ' +
                app_name + '; cd ~/spdz-2; ./Player-Online.x -pn 5000 -h ' +
                root_instance_ip + ' ' + str(1+i) + ' ' + app_name)]
        print (other_machine_commands)

        client_thread = threading.Thread(target=ec2Manager.execute_command_on_instance, args=[instance_ids[i+1],
                other_machine_commands, False, True])

        client_thread.start()

        client_machine_threads.append(client_thread)

    for client_thread in client_machine_threads:
        client_thread.join()
    root_machine_thread.join()


def display_output(ec2Manager, instance_ids):
    for instance_id in instance_ids:
        ec2Manager.execute_command_on_instance(instance_id, ["cat ~/output"],
                True)


def run_viff_app(ec2Manager):
    instance_ids, instance_ips = ec2Manager.create_instances()
    viff_app_runner_helper(ec2Manager, instance_ids, instance_ips,
            ec2Manager.config.MPC_APP_NAME)
    time.sleep(ec2Manager.config.SLEEP_TIMEOUT_IN_SECONDS)
    display_output(ec2Manager, instance_ids)


def run_spdz_app(ec2Manager):
    instance_ids, instance_ips = ec2Manager.create_instances()
    # print(instance_ips)
    # print(instance_ids)
    spdz_app_runner_helper(ec2Manager, instance_ids, instance_ips,
                           ec2Manager.config.MPC_APP_NAME)
    time.sleep(ec2Manager.config.SLEEP_TIMEOUT_IN_SECONDS)


ec2Manager = EC2Manager()
if ec2Manager.config.MPC_FRAMEWORK == "viff":
    run_viff_app(ec2Manager)
elif ec2Manager.config.MPC_FRAMEWORK == "spdz":
    run_spdz_app(ec2Manager)
