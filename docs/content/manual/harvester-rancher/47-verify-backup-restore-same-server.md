---
title: 47-Verify Backup and restore on same server
---

- Pre-requisites: Setup a backup-target
  - Could be NFS or another variation
- Pre-requisites: Have an instance of Rancher running
  - Also have installed Rancher Backup from the Apps/Marketplace

- Navigate to Rancher Backups, Backup:
  - Create a backup of RKE1 or RKE2

- Navigate to Rancher Backups, Restore:
  - Restore the backup that was generated

- Restoration should be successful
