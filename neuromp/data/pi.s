	.globl _num_passos
	.data
	.align 3
_num_passos:
	.quad	10000000000
	.comm	_passo,8,3
	.cstring
lC4:
	.ascii "O valor de PI \303\251: %f\12\0"
	.text
	.globl _main
_main:
LFB1:
	pushq	%rbp
LCFI0:
	movq	%rsp, %rbp
LCFI1:
	subq	$48, %rsp
	movl	%edi, -36(%rbp)
	movq	%rsi, -48(%rbp)
	pxor	%xmm0, %xmm0
	movsd	%xmm0, -16(%rbp)
	movq	_num_passos(%rip), %rax
	cvtsi2sdq	%rax, %xmm0
	movsd	lC1(%rip), %xmm1
	divsd	%xmm0, %xmm1
	movapd	%xmm1, %xmm0
	movq	_passo@GOTPCREL(%rip), %rax
	movsd	%xmm0, (%rax)
	movq	$0, -8(%rbp)
	jmp	L2
L3:
	cvtsi2sdq	-8(%rbp), %xmm0
	movsd	lC2(%rip), %xmm1
	addsd	%xmm1, %xmm0
	movq	_passo@GOTPCREL(%rip), %rax
	movsd	(%rax), %xmm1
	mulsd	%xmm1, %xmm0
	movsd	%xmm0, -32(%rbp)
	movsd	-32(%rbp), %xmm0
	mulsd	-32(%rbp), %xmm0
	movsd	lC1(%rip), %xmm1
	addsd	%xmm1, %xmm0
	movsd	lC3(%rip), %xmm1
	divsd	%xmm0, %xmm1
	movapd	%xmm1, %xmm0
	movsd	-16(%rbp), %xmm1
	addsd	%xmm1, %xmm0
	movsd	%xmm0, -16(%rbp)
	addq	$1, -8(%rbp)
L2:
	movq	_num_passos(%rip), %rax
	cmpq	%rax, -8(%rbp)
	jl	L3
	movq	_passo@GOTPCREL(%rip), %rax
	movsd	(%rax), %xmm0
	movsd	-16(%rbp), %xmm1
	mulsd	%xmm1, %xmm0
	movsd	%xmm0, -24(%rbp)
	movq	-24(%rbp), %rax
	movq	%rax, %xmm0
	leaq	lC4(%rip), %rdi
	movl	$1, %eax
	call	_printf
	movl	$0, %eax
	leave
LCFI2:
	ret
LFE1:
	.literal8
	.align 3
lC1:
	.long	0
	.long	1072693248
	.align 3
lC2:
	.long	0
	.long	1071644672
	.align 3
lC3:
	.long	0
	.long	1074790400
	.section __TEXT,__eh_frame,coalesced,no_toc+strip_static_syms+live_support
EH_frame1:
	.set L$set$0,LECIE1-LSCIE1
	.long L$set$0
LSCIE1:
	.long	0
	.byte	0x1
	.ascii "zR\0"
	.byte	0x1
	.byte	0x78
	.byte	0x10
	.byte	0x1
	.byte	0x10
	.byte	0xc
	.byte	0x7
	.byte	0x8
	.byte	0x90
	.byte	0x1
	.align 3
LECIE1:
LSFDE1:
	.set L$set$1,LEFDE1-LASFDE1
	.long L$set$1
LASFDE1:
	.long	LASFDE1-EH_frame1
	.quad	LFB1-.
	.set L$set$2,LFE1-LFB1
	.quad L$set$2
	.byte	0
	.byte	0x4
	.set L$set$3,LCFI0-LFB1
	.long L$set$3
	.byte	0xe
	.byte	0x10
	.byte	0x86
	.byte	0x2
	.byte	0x4
	.set L$set$4,LCFI1-LCFI0
	.long L$set$4
	.byte	0xd
	.byte	0x6
	.byte	0x4
	.set L$set$5,LCFI2-LCFI1
	.long L$set$5
	.byte	0xc
	.byte	0x7
	.byte	0x8
	.align 3
LEFDE1:
	.subsections_via_symbols
