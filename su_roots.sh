#!/system/bin/sh

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

if [[ ! -e /sbin/magisk ]]; then 
    echo "This script only works in magisk enviroment."
    exit
fi

suroots_fp="/sbin/.suroots"
system_mirror="/sbin/.magisk/mirror/system/ "
mkdir "$suroots_fp"

# Handle LineageOS SU


init_losu() {
   chmntdir="$suroots_fp/losu"

    mkdir "$suroots_fp/losu"
    mkdir "$suroots_fp/losu/dev"
    mkdir "$suroots_fp/losu/sys"

    mkdir "$suroots_fp/losu/proc"
    mkdir "$suroots_fp/losu/etc"
   
   echo "Mounting bindpoints";

   mount -o bind /dev "$chmntdir/dev"
   mount -t devpts -o rw,gid=5,mode=620 devpts "$chmntdir/dev/pts"
    mount -t sysfs sys "$chmntdir/sys"
  
    mount -o rw "/data/adb/system.ext4"   "$suroots_fp/losu/system"
    mount -o bind "/etc" "$suroots_fp/losu/etc"
    
    losu_loc="$suroots_fp/losu/system/xbin/su"
    touch "$losu_loc"
    mount -o bind "$(pwd)/data/los16/system/xbin/su" "$losu_loc"

  chmod 0755 "$losu_loc"
}



subcommand="$1"
super_su="$2"

sub_help() {
    echo "Create a fake root to test su binaries."
}

sub_mount() {
    init_losu
}

sub_chroot() {
/sbin/.magisk/busybox/unshare -fpm /sbin/.magisk/busybox/chroot  "$suroots_fp/losu/" 
}

sub_umount() {
    umount $(grep     "$suroots_fp/losu"  /proc/mounts | cut -f2 -d " " | sort -r)
 
}
case $subcommand in
    "" | "-h" | "--help")
        sub_help
        ;;
    *)
        shift
        sub_${subcommand} $@
        ;;
esac