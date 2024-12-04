from .base import BaseManager

# https://10.115.8.170/k8s/clusters/local/
# api/v1/namespaces/default/secrets?fieldManager=kubectl-create&fieldValidation=Strict
class SecretsManager(BaseManager):
    # PATH_fmt = ("apis/{{API_VERSION}}/namespaces/{}"
    #             "/supportbundles/{uid}")
    # DL_fmt = "/v1/harvester/supportbundles/{uid}/download"
    API_VERSION = "v1"
    PATH_fmt = ("/api/v1/namespaces/{namespace}/secrets/{name}")
    CREATE_fmt = ("/api/v1/namespaces/{namespace}/secrets")

    def create_data(self, name, namespace, string_data, ):
        data = {
            "apiVersion": f"{self.API_VERSION}",
            "kind": "Secret",
            "metadata": {
                "name": f"{name}",
                "namespace": f"{namespace}"
            },
            "stringData": string_data
        }

        return self._inject_data(data)

    def get(self, name, namespace, *, raw=False):
        path = self.PATH_fmt.format(name=name, namespace=namespace)
        return self._get(path, raw=raw)

    def create(self, name, namespace, string_data, *, raw=False):
        data = self.create_data(name, namespace, string_data)
        path = self.CREATE_fmt.format(namespace=namespace)

        return self._create(path, json=data, raw=raw)

    def update(self, *args, **kwargs):
        raise NotImplementedError("Update Secret Not Implemented")

    def replace(self, *args, **kwargs):
        raise NotImplementedError("Replace Secret Not Implemented")

    def delete(self, name, namespace, *, raw=False):
        path = self.PATH_fmt.format(name=name, namespace=namespace)
        return self._delete(path, raw=raw)
