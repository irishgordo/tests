from .base import BaseManager

# https://10.115.8.170/k8s/clusters/
# local
# /apis/migration.harvesterhci.io/v1beta1/namespaces/default/openstacksources
# ?fieldManager=kubectl-create&fieldValidation=Strict
# https://10.115.8.170/k8s/clusters/local
# /apis/migration.harvesterhci.io/v1beta1/namespaces/default/openstacksources/devstack
class OpenStackSourceManager(BaseManager):
    PATH_fmt = "apis/migration.harvesterhci.io/v1beta1/namespaces/{ns}/openstacksources/{name}"
    CREATE_fmt = "apis/migration.harvesterhci.io/v1beta1/namespaces/{ns}/openstacksources"
    API_VERSION = "migration.harvesterhci.io/v1beta1"

    def create_data(self, name, ns, endpoint, region, credentials):
        data = {
            "apiVersion": f"{self.API_VERSION}",
            "kind": "OpenstackSource",
            "metadata": {
                "name": f"{name}",
                "namespace": f"{ns}"
            },
            "spec": {
                "endpoint": f"{endpoint}",
                "region": f"{region}",
                "credentials": credentials
            }
        }
        return self._inject_data(data)

    def get(self, name, ns, *, raw=False):
        path = self.PATH_fmt.format(name=name, ns=ns)
        return self._get(path, raw=raw)

    def create(self, name, ns, endpoint, region, credentials, *, raw=False):
        data = self.create_data(name, ns, endpoint, region, credentials)
        path = self.CREATE_fmt.format(ns=ns)

        return self._create(path, json=data, raw=raw)

    def update(self, name, ns, *args, **kwargs):
        raise NotImplementedError("Update OpenStackSource Not Implemented")

    def replace(self, name, ns, *args, **kwargs):
        raise NotImplementedError("Replace OpenStackSource Not Implemented")

    def delete(self, name, ns, *, raw=False):
        path = self.PATH_fmt.format(name=name, ns=ns)
        return self._delete(path, raw=raw)