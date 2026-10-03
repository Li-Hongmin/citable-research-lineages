/* SPDX-License-Identifier: Apache-2.0 */
/* Independent complete-X identity check. Formal basis tests only; no RW data. */
#include "field_arithmetic.h"
int main(void){
  const unsigned U4=8+64+512+4096,kap=4*(1u<<15),M=(Q-1)/(U-1);
  fe K[U];unsigned nk=0;for(fe x=0;x<Q;x++)if(powf_(x,U)==x)K[nk++]=x;
  require(nk==U,"K size");fe a=K[2];require(a&&a!=1,"nontrivial separator label");
  fe kvals[3]={0,1,73951};
  for(unsigned kidx=0;kidx<3;kidx++){
    fe k=kvals[kidx],sum[7]={0},off[7]={0};
    for(fe x=0;x<Q;x++){
      fe s=L(0,x),ell=L(a,x),v=powf_(x,U-1),v4=powf_(v,4);
      fe low=powf_(1^mul(k,v4),U4),base0=powf_(s,4*M);
      fe base2=mul(powf_(ell,2),powf_(s,4*M-2));
      fe baseK=mul(powf_(ell,kap),powf_(s,4*M-kap));
      fe baseT=mul(powf_(ell,kap+2),powf_(s,4*M-kap-2));
      fe bases[7]={base0,base2,baseK,baseT,mul(base0,powf_(v,kap)),mul(base2,powf_(v,kap)),mul(baseT,powf_(v,kap))};
      int isoff=powf_(x,U)!=x;
      for(unsigned j=0;j<7;j++){fe term=mul(low,bases[j]);sum[j]^=term;if(isoff)off[j]^=term;}
    }
    fe want=powf_(1^k,U4);
    for(unsigned j=0;j<7;j++){require(sum[j]==want,"full X basis sum");require(off[j]==(want^(j==0?1:0)),"off-grid basis sum");}
    printf("PASS k=%u label=%u: seven full-X basis sums=%u; off-grid correction only first basis\n",k,a,want);
  }
  puts("Formal linear identity only; no actual-source reachability or coefficient independence is certified.");return 0;
}
