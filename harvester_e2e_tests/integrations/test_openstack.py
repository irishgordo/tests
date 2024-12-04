# Copyright (c) 2024 SUSE LLC
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.   See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, contact SUSE LLC.
#
# To contact SUSE about this file by physical or electronic mail,
# you may find current contact information at www.suse.com

import openstack.block_storage
import pytest
import openstack
import polling2
from pytest_cases import parametrize_with_cases, case
from keystoneauth1.adapter import Adapter
from openstack.block_storage.v3._proxy import Proxy as BlockStorageService


openstack.enable_logging(debug=True)

pytest_plugins = [
    'harvester_e2e_tests.fixtures.api_client',
    "harvester_e2e_tests.fixtures.openstack",
]

# ds1G / ID: d2


class CasesOpenStackBootModes:
    """_summary_

    Yields:
        _type_: _description_
    """
    @case(tags="openstack-vm-boot")
    def case_openstack_vm_bios(self, request, openstack_env):
        image_uri = request.config.getoption('--openstack-ubuntu-image-url')
        desired_vol_timeout = request.config.getoption('--openstack-op-vol-timeout')
        desired_inst_timeout = request.config.getoption('--openstack-op-inst-timeout')
        desired_inst_step_time = request.config.getoption('--openstack-op-inst-step-time')
        desired_img_timeout = request.config.getoption('--openstack-op-img-timeout')
        desired_img_step_time = request.config.getoption('--openstack-op-img-step-time')
        default_flavor_name = request.config.getoption('--openstack-default-flavor-name')
        default_network_name = request.config.getoption('--openstack-default-network-name')
        image_attrs = {
            'name': 'test-vm-bios',
            'disk_format': 'qcow2',
            'container_format': 'bare',
            'visibility': 'public'
        }
        opnstk = openstack.connect()
        image = opnstk.image.create_image(**image_attrs, wait=True)
        opnstk.image.import_image(image, method="web-download", uri=image_uri)
        polling2.poll(
            lambda: (opnstk.get_image_by_id(image.id)).status == 'active',
            desired_img_step_time,
            timeout=desired_img_timeout, poll_forever=False
        )
        root_disk = opnstk.create_volume('10', wait=True, timeout=desired_vol_timeout,
                                         image=image.id, bootable=True)
        # Note: to maxamize space clean up temp volume service created prior
        # GET call to block-storage for http://IP/volume/v3/d9c2992f465c409c83c32ed69fa959fd/volumes/detail?name=image-accdf01d-c919-47e4-ac8e-2a4f58768807
        # used request id req-eb5d7d7f-3fa2-44de-b098-7dbdf3b076a3Volume image-accdf01d-c919-47e4-ac8e-2a4f58768807 does not exist
        # We'll see an issue trying to delete the volume with simply opnstk.delete_volume(), since it doesn't allow multiple project search
        # We need to use the cinder object that is proxy to the block_storage
        # then on the instance found, since it is not in the "demo" project for the temp volume image, it's in the "service" project
        # we'll call "delete" on that instance to remove it remotely
        print(f'cleaning up image temp volume...image-{image.id}')
        image_temp_vol = 'image-' + image.id
        cinder: BlockStorageService = opnstk.block_storage
        temp_vol_found = cinder.find_volume(image_temp_vol, all_projects=True)
        adapter = Adapter(opnstk.session, service_type="block-storage")
        temp_vol_found.delete(adapter)
        # Note: we're not useing wait=True as that mechanism is dependent on
        # floating_ips, and since the networking for floating_ips
        # is not working with our OpenStack instance due to limitations on both
        # an understanding of how to properly implement at OpenStack creation
        # with DevStack & juggling a "set" space for CIDR, we can not use
        # wait=True
        vm = opnstk.create_server('test-vm-bios', boot_volume=root_disk.id,
                                  flavor=default_flavor_name,
                                  wait=False, network=default_network_name, terminate_volume=True,
                                  reuse_ips=False)
        polling2.poll(
            lambda: (opnstk.get_server(vm.id)).status == 'ACTIVE',
            desired_inst_step_time,
            timeout=desired_inst_timeout, poll_forever=False
        )
        yield image, vm, root_disk
        # print(f'cleaning up vm...{vm.id}')
        # opnstk.delete_server(vm.id, wait=True)
        # print(f'cleaning up image...{image.id}')
        # opnstk.delete_image(image.id, wait=True)
        pass

    @case(tags="openstack-vm-boot")
    def case_openstack_vm_efi_no_secure_boot(self, request, openstack_env):
        #openstack image set -property hw_firmware_type=uefi
        # --property os_secure_boot=required --property hw_machine_type=q35 IMAGE-ID
        # --os-auth-url http://172.19.109.182/identity --os-identity-api-version 3
        # --os-project-name admin --os-project-domain-name default --os-username admin --os-password testtesttest
        pass

    @case(tags="openstack-vm-boot")
    def case_openstack_vm_efi_with_secure_boot(self, request, openstack_env):
        #openstack image set -property hw_firmware_type=uefi --property hw_machine_type=q35
        # IMAGE-ID --os-auth-url http://172.19.109.182/identity --os-identity-api-version 3
        # --os-project-name admin --os-project-domain-name default --os-username admin --os-password testtesttest
        pass


@pytest.mark.p1
class TestOpenstackVMImport:
    @parametrize_with_cases("openstack_vm_boot", cases=CasesOpenStackBootModes, has_tag='openstack-vm-boot')
    def test_vm_import_multi_boot(self, api_client, request, openstack_env,
                                  openstack_vm_boot, openstack_harvester):
        opnstk_img, opnstk_server, opnstk_root_disk = openstack_vm_boot
        openstack_secret, openstack_source = openstack_harvester
        print(opnstk_img)
        print(opnstk_server)
        print(opnstk_root_disk)
        pass