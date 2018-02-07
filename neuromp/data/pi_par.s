	.globl _num_passos
	.data
	.align 3
_num_passos:
	.quad	10000000000
	.comm	_passo,8,3
	.cstring
lC2:
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
	movsd	%xmm0, -8(%rbp)
	movq	_num_passos(%rip), %rax
	cvtsi2sdq	%rax, %xmm0
	movsd	lC1(%rip), %xmm1
	divsd	%xmm0, %xmm1
	movapd	%xmm1, %xmm0
	movq	_passo@GOTPCREL(%rip), %rax
	movsd	%xmm0, (%rax)
	movsd	-8(%rbp), %xmm0
	movsd	%xmm0, -24(%rbp)
	leaq	-24(%rbp), %rax
	movl	$0, %ecx
	movl	$0, %edx
	movq	%rax, %rsi
	leaq	_main._omp_fn.0(%rip), %rdi
	call	_GOMP_parallel
	movsd	-24(%rbp), %xmm0
	movsd	%xmm0, -8(%rbp)
	movq	_passo@GOTPCREL(%rip), %rax
	movsd	(%rax), %xmm0
	movsd	-8(%rbp), %xmm1
	mulsd	%xmm1, %xmm0
	movsd	%xmm0, -16(%rbp)
	movq	-16(%rbp), %rax
	movq	%rax, %xmm0
	leaq	lC2(%rip), %rdi
	movl	$1, %eax
	call	_printf
	movl	$0, %eax
	leave
LCFI2:
	ret
LFE1:
_main._omp_fn.0:
LFB2:
	pushq	%rbp
LCFI3:
	movq	%rsp, %rbp
LCFI4:
	pushq	%r12
	pushq	%rbx
	subq	$48, %rsp
LCFI5:
	movq	%rdi, -56(%rbp)
	pxor	%xmm0, %xmm0
	movsd	%xmm0, -24(%rbp)
	movq	_num_passos(%rip), %rbx
	call	_omp_get_num_threads
	movslq	%eax, %r12
	call	_omp_get_thread_num
	movslq	%eax, %rsi
	movq	%rbx, %rax
	cqto
	idivq	%r12
	movq	%rax, %rcx
	movq	%rbx, %rax
	cqto
	idivq	%r12
	movq	%rdx, %rax
	cmpq	%rax, %rsi
	jl	L4
L8:
	imulq	%rcx, %rsi
	movq	%rsi, %rdx
	addq	%rdx, %rax
	leaq	(%rax,%rcx), %rdx
	cmpq	%rdx, %rax
	jge	L5
	movq	%rax, -32(%rbp)
L6:
	cvtsi2sdq	-32(%rbp), %xmm0
	movsd	lC3(%rip), %xmm1
	addsd	%xmm1, %xmm0
	movq	_passo@GOTPCREL(%rip), %rax
	movsd	(%rax), %xmm1
	mulsd	%xmm1, %xmm0
	movsd	%xmm0, -40(%rbp)
	movsd	-40(%rbp), %xmm0
	mulsd	-40(%rbp), %xmm0
	movsd	lC1(%rip), %xmm1
	addsd	%xmm1, %xmm0
	movsd	lC4(%rip), %xmm1
	divsd	%xmm0, %xmm1
	movapd	%xmm1, %xmm0
	movsd	-24(%rbp), %xmm1
	addsd	%xmm1, %xmm0
	movsd	%xmm0, -24(%rbp)
	addq	$1, -32(%rbp)
	cmpq	%rdx, -32(%rbp)
	jl	L6
L5:
	movq	-56(%rbp), %rax
	movq	%rax, %rcx
	movq	(%rcx), %rdx
L7:
	movq	%rdx, %xmm0
	addsd	-24(%rbp), %xmm0
	movq	%xmm0, %rsi
	movq	%rdx, %rax
	lock cmpxchgq	%rsi, (%rcx)
	movq	%rdx, %rsi
	movq	%rax, %rdx
	cmpq	%rsi, %rax
	jne	L7
	jmp	L9
L4:
	movl	$0, %eax
	addq	$1, %rcx
	jmp	L8
L9:
	addq	$48, %rsp
	popq	%rbx
	popq	%r12
	popq	%rbp
LCFI6:
	ret
LFE2:
	.literal8
	.align 3
lC1:
	.long	0
	.long	1072693248
	.align 3
lC3:
	.long	0
	.long	1071644672
	.align 3
lC4:
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
LSFDE3:
	.set L$set$6,LEFDE3-LASFDE3
	.long L$set$6
LASFDE3:
	.long	LASFDE3-EH_frame1
	.quad	LFB2-.
	.set L$set$7,LFE2-LFB2
	.quad L$set$7
	.byte	0
	.byte	0x4
	.set L$set$8,LCFI3-LFB2
	.long L$set$8
	.byte	0xe
	.byte	0x10
	.byte	0x86
	.byte	0x2
	.byte	0x4
	.set L$set$9,LCFI4-LCFI3
	.long L$set$9
	.byte	0xd
	.byte	0x6
	.byte	0x4
	.set L$set$10,LCFI5-LCFI4
	.long L$set$10
	.byte	0x8c
	.byte	0x3
	.byte	0x83
	.byte	0x4
	.byte	0x4
	.set L$set$11,LCFI6-LCFI5
	.long L$set$11
	.byte	0xc
	.byte	0x7
	.byte	0x8
	.align 3
LEFDE3:
	.subsections_via_symbols
