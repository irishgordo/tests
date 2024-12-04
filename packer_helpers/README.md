# Builds OpenStack Ready Image That Can Be Uploaded To FileServer

1. `packer init .`
2. `packer build ubuntu_custom_jammy_pre_req.pkr.hcl`
3. `PACKER_LOG=1 packer build ubuntu_custom_jammy_qemu.pkr.hcl`

# Note:
- must manually remove `output` dir prior to each run as well as cidata.iso, meta-data, user-data

# Deploy Note:
- deploy to file-server, example, for openstack image built w/ jammy w/ files pre-seeded + users
```
scp -v ./output/build.qcow2 opensuse@10.115.1.6:/iso/vm-import/openstack/jammy-openstack.qcow2
```

# Modification To File-Server/Artifact-Server Implemented:
- manually prepped out file-server:
```
sudo chown -R opensuse:users vm-import
```