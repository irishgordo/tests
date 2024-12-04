source "file" "user_data" {
  content = <<EOF
#cloud-config
final_message: "Packer Based Image finished in $UPTIME"
ssh_pwauth: True
users:
  - name: user
    plain_text_passwd: packer
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    lock_passwd: false
  - name: ubuntu
    plain_text_passwd: ubuntupw
    sudo: ALL=(ALL) NOPASSWD:ALL
    shell: /bin/bash
    lock_passwd: false
packages:
  - qemu-guest-agent
write_files:
  - path: /etc/rc.local
    owner: root:root
    content: |
      #!/bin/sh
      # add your commands
      # call your scripts here

      /usr/sbin/ip link set enp1s0 up
      /usr/sbin/dhclient -v enp1s0
      # last line must be exit 0
      exit 0
runcmd:
  - echo "hello" > /etc/hello.txt
  - chmod 777 /etc/hello.txt
  - md5sum /etc/hello.txt > /etc/md5sum-of-hello-txt-to-compare.txt
  - chmod 777 /etc/md5sum-of-hello-txt-to-compare.txt
  - systemctl enable qemu-guest-agent.service
  - systemctl enable rc-local.service
EOF
  target  = "user-data"
}

source "file" "meta_data" {
  content = <<EOF
{"instance-id":"packer-worker.tenant-local","local-hostname":"packer-worker"}
EOF
  target  = "meta-data"
}

build {
  sources = ["sources.file.user_data", "sources.file.meta_data"]

  provisioner "shell-local" {
    inline = ["genisoimage -output cidata.iso -input-charset utf-8 -volid cidata -joliet -r user-data meta-data"]
  }
}