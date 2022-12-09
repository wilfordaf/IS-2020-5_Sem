"select disk 1
convert dynamic
select disk 2
convert dynamic
select disk 3
convert dynamic
select disk 4
convert dynamic
create volume raid disk=1,2,3,4
format fs=ntfs quick label=Raid5_Volume
assign letter=V" | DISKPART
pause