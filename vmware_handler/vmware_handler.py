#!/usr/bin/env python
# -*- coding: utf-8 -*
import atexit

from pyVim.connect import SmartConnect, Disconnect

import ssl
from pyVmomi import vim
import json


class VMwareHandler(object):
    """
    Operate VMware
    """

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        self.si = None
        self.init_connection()

    def init_connection(self):
        try:
            self.context.verify_mode = ssl.CERT_NONE
            self.si = SmartConnect(host=self.host,
                                   user=self.username,
                                   pwd=self.password,
                                   sslContext=self.context)
        except:
            raise Exception("Failed to connect to VMware")


class VM(VMwareHandler):
    """
    Operate Image
    """

    def __init__(self, host, username, password):
        super(VM, self).__init__(host, username, password)

    def hosts(self):
        """
        List all hosts
        :return: json
        """
        try:
            atexit.register(Disconnect, self.si)
            result = _get_all_objs(self.si.RetrieveContent(), [vim.HostSystem])
            if result is not None:
                hosts = []
                for host in result:
                    d = {'name': host.name, 'status': host.summary.runtime.powerState, 'port': host.summary.config.port}
                    hosts.append(d)
                return json.dumps(hosts)
            else:
                return None
        except:
            raise Exception("Failed to list hosts")

    def vms(self):
        """
        List all images
        :return: json
        """
        try:
            atexit.register(Disconnect, self.si)
            content = self.si.RetrieveContent()
            container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
            if container is not None:
                vms = []
                for vm in container.view:
                    ip = vm.summary.guest.ipAddress
                    if not ip:
                        ip = ''
                    if vm.config.template:
                        is_template = True
                    else:
                        is_template = False
                    d = {'name': vm.name, 'status': vm.summary.runtime.powerState, 'instanceId': vm.summary.config.uuid,
                         'memory': vm.summary.config.memorySizeMB, 'cpu': vm.summary.config.numCpu, 'privateIps': ip,
                         'managerIp': ip, 'isTemplate': is_template}
                    vms.append(d)
                return json.dumps(vms)
            else:
                return None
        except:
            raise Exception("Failed to list vm")

    def get_vm(self, uuid):
        """
        Get vm
        :param uuid:
        :return: json
        """
        try:
            atexit.register(Disconnect, self.si)
            vm = self.si.content.searchIndex.FindByUuid(None, uuid, True, False)
            if vm is not None:
                ip = vm.summary.guest.ipAddress
                if not ip:
                    ip = ''
                d = {'name': vm.name, 'status': vm.summary.runtime.powerState, 'instanceId': vm.summary.config.uuid,
                     'memory': vm.summary.config.memorySizeMB, 'cpu': vm.summary.config.numCpu, 'privateIps': ip,
                     'managerIp': ip}
                return json.dumps(d)
            else:
                return None
        except:
            raise Exception("Failed to get vm")

    def create(self, vm_name, uuid):
        """
        Create vm
        :param vm_name:
        :param datastore_name:
        :param uuid:
        :return:
        """

    def delete(self, uuid):
        """
        Delete vm
        :param uuid:
        :return: True | False
        """
        try:
            atexit.register(Disconnect, self.si)
            vm = self.si.content.searchIndex.FindByUuid(None, uuid, True, False)
            if vm is not None:
                result = vm.Destroy_Task()
            else:
                return False
            if result:
                return True
            else:
                return False
        except:
            raise Exception("Failed to delete vm")

    def startup(self, uuid):
        """
        Startup vm
        :param uuid:
        :return: True | False
        """
        try:
            atexit.register(Disconnect, self.si)
            vm = self.si.content.searchIndex.FindByUuid(None, uuid, True, False)
            if vm is not None:
                result = vm.PowerOnVM_Task()
            else:
                return False
            if result:
                return True
            else:
                return False
        except:
            raise Exception("Failed to PowerOnVM_Task vm")

    def shutdown(self, uuid):
        """
        Shutdown vm
        :param name:
        :return: True | False
        """
        try:
            atexit.register(Disconnect, self.si)
            vm = self.si.content.searchIndex.FindByUuid(None, uuid, True, False)
            if vm is not None:
                result = vm.PowerOffVM_Task()
            else:
                return False
            if result:
                return True
            else:
                return False
        except:
            raise Exception("Failed to shutdown vm")

    def reboot(self, uuid):
        """
        Reboot vm
        :param uuid:
        :return: True | False
        """
        try:
            atexit.register(Disconnect, self.si)
            vm = self.si.content.searchIndex.FindByUuid(None, uuid, True, False)
            if vm is not None:
                result = vm.ResetVM_Task()
            else:
                return False
            if result:
                return True
            else:
                return False
        except:
            raise Exception("Failed to reboot vm")

    def suspend(self, uuid):
        """
        Suspend vm
        :param uuid:
        :return: True | False
        """
        try:
            atexit.register(Disconnect, self.si)
            vm = self.si.content.searchIndex.FindByUuid(None, uuid, True, False)
            if vm is not None:
                result = vm.SuspendVM_Task()
            else:
                return False
            if result:
                return True
            else:
                return False
        except:
            raise Exception("Failed to suspend vm")

    def active(self, uuid):
        """
        Active vm
        :param uuid:
        :return: True | False
        """
        try:
            atexit.register(Disconnect, self.si)
            vm = self.si.content.searchIndex.FindByUuid(None, uuid, True, False)
            if vm is not None:
                result = vm.PowerOnVM_Task()
            else:
                return False
            if result:
                return True
            else:
                return False
        except:
            raise Exception("Failed to active vm")

    def create_snapshot(self, uuid, name, desc):
        """
        Create snapshot
        :param uuid:
        :param name:
        :param desc:
        :return:
        """
        try:
            atexit.register(Disconnect, self.si)
            vm = self.si.content.searchIndex.FindByUuid(None, uuid, True, False)
            if vm is not None:
                result = vm.CreateSnapshot_Task(name=name, description=desc, memory=True, quiesce=False)
            else:
                return False
            if result:
                return True
            else:
                return False
        except:
            raise Exception("Failed to create snapshot")

    def remove_snapshot(self, uuid, name):
        """
        Remove snapshot
        :param uuid:
        :param name:
        :return:
        """
        try:
            atexit.register(Disconnect, self.si)
            vm = self.si.content.searchIndex.FindByUuid(None, uuid, True, False)
            if vm is not None:
                snapshots = vm.snapshot.rootSnapshotList
                for snapshot in snapshots:
                    if name == snapshot.name:
                        snap_obj = snapshot.snapshot
                        result = snap_obj.RemoveSnapshot_Task(True)
            else:
                return False
            if result:
                return True
            else:
                return False
        except:
            raise Exception("Failed to remove snapshot")


if __name__ == '__main__':
    vm = VM('192.168.1.235', 'administrator@vsphere.local', 'Root123!')
    print vm.delete('564d0fb0-830f-3c86-e76b-342ead016e60')
