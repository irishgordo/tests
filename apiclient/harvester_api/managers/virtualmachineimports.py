from .base import BaseManager

# https://10.115.8.170/k8s/clusters/local
# /apis/migration.harvesterhci.io/v1beta1/namespaces/default/virtualmachineimports
# ?fieldManager=kubectl-create&fieldValidation=Strict
class VirtualMachineImportsManager(BaseManager):
    PATH_fmt = "apis/migration.harvesterhci.io/v1beta1/namespaces/{ns}/virtualmachineimports/{name}"
    CREATE_fmt = "apis/migration.harvesterhci.io/v1beta1/namespaces/{ns}/virtualmachineimports"
    API_VERSION = "migration.harvesterhci.io/v1beta1"

    def create_data(self, name, ns, vm_to_import_name, network_mappings, sc_name, sc_namespace, sc_kind):
        net_list = []
        for network_mapping in network_mappings:
            new_net = {
                "sourceNetwork": network_mapping['sourceNetwork'],
                "destinationNetwork": network_mapping['destinationNetwork']
            }
            net_list.append(new_net)
        data = {
            "apiVersion": f"{self.API_VERSION}",
            "kind": "VirtualMachineImport",
            "metadata": {
                "name": f"{name}",
                "namespace": f"{ns}"
            },
            "spec": {
                "virtualMachineName": f"{vm_to_import_name}",
                "networkMapping": net_list,
                "sourceCluster": {
                    "name": f"{sc_name}",
                    "namespace": f"{sc_namespace}",
                    "kind": f"{sc_kind}",
                    "apiVersion": f"{self.API_VERSION}"
                }
            }
        }

        return self._inject_data(data)

    def get(self, name, ns, *, raw=False):
        path = self.PATH_fmt.format(name=name, ns=ns)
        return self._get(path, raw=raw)

    def create(self, name, ns, vm_to_import_name, network_mappings, sc_name, sc_namespace, sc_kind, *, raw=False):
        data = self.create_data(name, ns, vm_to_import_name, network_mappings, sc_name, sc_namespace, sc_kind,)
        path = self.CREATE_fmt.format(ns=ns)

        return self._create(path, json=data, raw=raw)

    def update(self, name, ns, *args, **kwargs):
        raise NotImplementedError("Update VirtualMachineImport Not Implemented")

    def replace(self, name, ns, *args, **kwargs):
        raise NotImplementedError("Replace VirtualMachineImport Not Implemented")

    def delete(self, name, ns, *, raw=False):
        path = self.PATH_fmt.format(name=name, ns=ns)
        return self._delete(path, raw=raw)