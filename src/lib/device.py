import os, re, stat
from subprocess import Popen, PIPE

"""
device.py - Device management for ASMDisks
Copyright (c) 2023 - Bart Sjerps <bart@dirty-cache.com>
License: GPLv3+
"""

class Device():
    def __init__(self, dev):
        if not os.path.exists(dev):
            raise ValueError('device %s does not exist' % dev)
        st = os.stat(dev)
        if not stat.S_ISBLK(st.st_mode):
            raise ValueError('%s is not a block device' % dev)
        self.dev = os.path.realpath(dev)
        self.major = st.st_rdev // 256
        self.minor = st.st_rdev % 256

    def execute(self, cmd):
        env = { 'PATH': '/usr/bin:/usr/sbin'}
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, env=env, encoding='utf-8')
        out, _ = proc.communicate()
        return out

    def __repr__(self):
        return f"{self.dev} {self.driver} {self.major}-{self.minor}"

    @property
    def driver(self):
        """Get the driver type for a device"""
        with open('/proc/devices') as f:
            data = f.read()
            r = re.match(r'.*Block devices:\s(.*)', data, re.S)
            if not r:
                raise ValueError("/proc/devices not processed")
            devices = r.group(1)
            for m, driver in re.findall('^\s*(\d+)\s+(.*)', devices, re.M):
                if int(m) == self.major:
                    return driver

    @property
    def serial(self):
        env = {}
        # Regular SCSI disks
        if self.driver == 'sd':
            out = self.execute(f'/lib/udev/scsi_id -ug {self.dev}'.split())
            return out.strip()

        # KVM VirtIO disks - not supported
        elif self.driver == 'virtblk':
            pass
        
        # Device mapper (LVM logical volumes, etc)
        elif self.driver == 'device-mapper':
            out = self.execute(f'dmsetup info -c --noheadings -o name {self.dev}'.split())
            return out.strip()
        
        # NVMe devices
        elif self.driver == 'blkext':
            wwidpath = os.path.join('/sys/block/', os.path.basename(self.dev), 'wwid')
            with open(wwidpath) as f:
                return f.read().rstrip()
        
        # Dell PowerFlex
        elif self.driver == 'scini':
            out = self.execute(f'/bin/emc/scaleio/drv_cfg --query_block_device_id --block_device {self.dev}')
            return out.strip()
        
        # Dell PowerPath
        elif self.driver == 'power2':
            out = self.execute(f'/sbin/powermt display dev={self.shortname}')
            r = re.search(r'^Pseudo name=(.*)', out, re.M)
            if r:
                return r.group(1)

    @property
    def shortname(self):
        return os.path.basename(self.dev)

    @property
    def scsi(self):
        if self.driver == 'sd':
            dirs = os.listdir(f'/sys/block/{self.shortname}/device/bsg')
            return f'[{dirs[0]}]'
        else:
            return '-'

    @property
    def size(self):
        out = self.execute(f'lsblk -ndo size {self.dev}'.split())
        return out.strip()

    @property
    def symlink(self):
        """Get first UDEV symlink for a device, excluded are /dev/disk/... and /dev/mapper/..."""
        path = f'/block/{self.shortname}'
        out = self.execute(f'udevadm info --root --query=symlink --path={path}'.split())
        for link in out.split():
            if not link.startswith('/dev/'):
                continue
            if link.startswith('/dev/disk') or link.startswith('/dev/mapper'):
                continue
            return link
        return '-'
    
    @property
    def contents(self):
        if self.isblank:
            return 'blank'
        udevinfo = self.execute(f'blkid -p -o udev {self.dev}'.split())
        for line in udevinfo.splitlines():
            k, v = line.split('=')
            if k == 'ID_PART_TABLE_TYPE':
                if v in ['dos','gpt','swap']:
                    return v
            elif k == 'ID_FS_TYPE':
                if v == 'oracleasm':
                    return 'asm'
                elif v == 'LVM2_member':
                    return 'lvm'
                elif v == 'linux_raid_member':
                    return 'raid'
                elif v in ['xfs', 'ext3', 'ext4']:
                    return v
        return 'unknown'

    @property
    def isblank(self):
        buf = bytearray(1024)
        try:
            with open(self.dev,'rb') as disk:
                data = disk.read(1024)
                if data == buf:
                    return True
                else:
                    return False
        except ValueError:
            pass

    @staticmethod
    def getdisks():
        proc = Popen(['lsblk', '-ndo', 'kname'], env={}, stdout=PIPE, stderr=PIPE, stdin=PIPE, encoding='utf-8')
        out, _ = proc.communicate()
        return sorted(out.strip().splitlines())

    @staticmethod
    def rescan():
        for dirname in os.listdir('/sys/class/scsi_host/'):
            if not os.path.isfile('/sys/class/scsi_host/' + dirname + '/scan'):
                continue
            with open('/sys/class/scsi_host/' + dirname + '/scan','a') as f:
                f.write('- - -\n')

    def xpartition(self):
        """Returns the partition number, 0 if full disk"""
        return self.minor % 16

    def xtype(self):
        """Get the disk type for a device"""
        return run('lsblk -dno type %s' % self.dev)