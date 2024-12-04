# flake8: noqa: E501,E202,E261,E231
import openstack
import json
import pytest
import requests
import os
import yaml
import polling2


@pytest.fixture(scope="session")
def openstack_env(request):
    cloud_yaml_url = request.config.getoption('--openstack-clouds-yaml-file-location')
    response = requests.get(cloud_yaml_url, allow_redirects=True)
    if response.status_code == 200:
        content = response.content.decode("utf-8")
        content = yaml.safe_load(content)
        os.environ['OS_AUTH_URL'] = content['clouds']['openstack']['auth']['auth_url']
        os.environ['OS_IDENTITY_API'] = str(content['clouds']['openstack']['identity_api_version'])
        os.environ['OS_PROJECT_NAME'] = content['clouds']['openstack']['auth']['project_name']
        os.environ['OS_USER_DOMAIN_NAME'] = content['clouds']['openstack']['auth']['user_domain_name']
        os.environ['OS_PROJECT_DOMAIN_ID'] = str.lower( content['clouds']['openstack']['auth']['user_domain_name'] )
        os.environ['OS_USERNAME'] = content['clouds']['openstack']['auth']['username']
        os.environ['OS_REGION_NAME'] = content['clouds']['openstack']['region_name']
        os.environ['OS_INTERFACE'] = content['clouds']['openstack']['interface']
        os.environ['OS_PROJECT_ID'] = str(content['clouds']['openstack']['auth']['project_id'])
        os.environ['OS_PASSWORD'] = request.config.getoption('--openstack-admin-password')
        return content
    else:
        return ReferenceError('could not get yaml for openstack connection')

@pytest.fixture(scope="session")
def openstack_harvester(request, api_client):
    data = {
        "id": "harvester-system/vm-import-controller",
        "type": "harvesterhci.io.addon",
        "spec": {
            "chart": "harvester-vm-import-controller",
            "enabled": True,
            "repo": "http://harvester-cluster-repo.cattle-system.svc/charts",
            "valuesContent": "{\"resources\":{\"requests\":{\"cpu\":\"1\",\"memory\":\"2Gi\"},\"limits\":{\"cpu\":\"4\",\"memory\":\"8Gi\"}},\"pvcClaim\":{\"enabled\":true,\"size\":\"200Gi\",\"storageClassName\":\"harvester-longhorn\"}}"# noqa: E501,E202,E261
        },
        "status": {}
    }
    addon_code, addon_data = api_client.addons.update('harvester-system/vm-import-controller', data)
    if addon_code != 200:
        return ReferenceError('cant update vm-import-controller addon')
    polling2.poll(
        lambda: (api_client.addons.get('harvester-system/vm-import-controller')[1])['status']['status'] == 'AddonDeploySuccessful',
        10,
        timeout=300, poll_forever=False
    )
    cloud_yaml_url = request.config.getoption('--openstack-clouds-yaml-file-location')
    response = requests.get(cloud_yaml_url, allow_redirects=True)
    if response.status_code == 200:
        content = response.content.decode("utf-8")
        content = yaml.safe_load(content)
        stringData = {
            "username": content['clouds']['openstack']['auth']['username'],
            "password": request.config.getoption('--openstack-admin-password'),
            "project_name": content['clouds']['openstack']['auth']['project_name'],
            "domain_name": str.lower( content['clouds']['openstack']['auth']['user_domain_name'] )
        }
        secret_mgr = api_client.secrets
        code, data = secret_mgr.create("openstack-secret", "default", stringData)
        if code == 201:
            openstack_source_mgr = api_client.openstacksource
            credentials = {
                "name": "openstack-secret",
                "namespace": "default"
            }
            source_code, source_data = openstack_source_mgr.create("openstack-devstack", "default",
                                                                   content['clouds']['openstack']['auth']['auth_url'],
                                                                   content['clouds']['openstack']['region_name'],
                                                                   credentials)
            if source_code == 201:
                polling2.poll(
                    lambda: (openstack_source_mgr.get("openstack-devstack", "default")[1])['status']['status'] == 'clusterReady',
                    10,
                    timeout=180, poll_forever=False
                )
                yield data, source_data
                code, _data = openstack_source_mgr.delete("openstack-devstack", "default")
                if code != 200:
                    return ReferenceError('could not delete openstack-source')
                code, _data = secret_mgr.delete("openstack-secret", "default")
                if code != 200:
                    return ReferenceError('could not delete openstack-secret')
                data = {
                    "id": "harvester-system/vm-import-controller",
                    "type": "harvesterhci.io.addon",
                    "spec": {
                        "chart": "harvester-vm-import-controller",
                        "enabled": False,
                        "repo": "http://harvester-cluster-repo.cattle-system.svc/charts",
                        "valuesContent": "{\"resources\":{\"requests\":{\"cpu\":\"1\",\"memory\":\"2Gi\"},\"limits\":{\"cpu\":\"4\",\"memory\":\"8Gi\"}},\"pvcClaim\":{\"enabled\":false,\"size\":\"200Gi\",\"storageClassName\":\"harvester-longhorn\"}}"# noqa: E501,E202,E261
                    },
                    "status": {}
                }
                addon_code, addon_data = api_client.addons.update('harvester-system/vm-import-controller', data)
                if addon_code != 200:
                    return ReferenceError('cant update vm-import-controller addon')
            else:
                return ReferenceError('could not build openstack-source')
        else:
            return ReferenceError('could not build secret')
    else:
        return ReferenceError('could not get yaml for openstack connection')
