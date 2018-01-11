bad_lines = [
	"USBPcap pseudoheader",
	"IRP ID:",
	"URB bus id",
    "Device address:",
    "Packet Data Length:",
    "Control transfer stage:",
    "URB setup",
    "Language Id",
    "wLength",
	"[Response in:",
	"[Request in:",
	"[Destination:",
	"IRP USBD_STATUS:",
]

f = open("dyna_less.txt","r")

lines = f.readlines()
f.close()


f = open("my_dyna.txt","w")
#Then, write your lines back, except the line you want to delete. You might want to change the "\n" to #whatever line ending your file uses.

for line in lines:
  #print line
  if not any(bad_line in line for bad_line in bad_lines):
    f.write(line)
#At the end, close the file again.

f.close()