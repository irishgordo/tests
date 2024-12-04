packer {
  required_plugins {
    vagrant = {
      version = "1.1.0"
      source  = "github.com/hashicorp/qemu"
    }
  }
}

source "qemu" "ubuntu" {
  format           = "qcow2"
  disk_image       = true
  disk_size        = "10G"
  headless         = true
  iso_url           = "https://cloud-images.ubuntu.com/noble/20250108/noble-server-cloudimg-amd64.img"
  iso_checksum      = "md5:b7207f981bd15e807a828068c797688e"
  qemuargs         = [["-m", "12G"], ["-smp", "8"], ["-cdrom", "cidata.iso"], ["-serial", "mon:stdio"]]
  ssh_password     = "packer"
  ssh_username     = "user"
  vm_name          = "build.qcow2"
  output_directory = "output"
  accelerator = "kvm"
  efi_boot          = false
  disk_compression = true
  net_device        = "virtio-net"
  shutdown_command = "sudo cloud-init clean --logs --machine-id && echo 'packer' | sudo -S shutdown -P now"
}

build {
  name = "image build"
  sources = ["source.qemu.ubuntu"]

  provisioner "shell" {
      inline = [
          "echo 'Waiting for cloud-init to complete...'",
          "cloud-init status --wait > /dev/null",
          "echo 'Completed cloud-init!'",
      ]
  }

}
