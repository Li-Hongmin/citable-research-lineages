/* SPDX-License-Identifier: Apache-2.0; extracted authorized finite arithmetic only. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

/* Lightweight exhaustive one-coordinate check only: F=GF(2^18), u=8.
   Polynomial x^18+x^7+1 is independently checked in the companion command.
   No actual RW word, source table, solver or project file is read. */
typedef uint32_t fe;
#define Q (1u<<18)
#define U 8u
#define MOD ((1u<<18)|(1u<<7)|1u)
static fe mul(fe a,fe b){fe r=0;while(b){if(b&1)r^=a;b>>=1;a<<=1;if(a&Q)a^=MOD;}return r;}
static fe powf_(fe a,uint32_t e){fe r=1;while(e){if(e&1)r=mul(r,a);a=mul(a,a);e>>=1;}return r;}
static fe L(fe b,fe x){return 1^powf_(x^b,U-1);}
static void require(int ok,const char *why){if(!ok){fprintf(stderr,"FAIL %s\n",why);exit(1);}}
