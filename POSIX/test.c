#include <stdio.h>
#include <string.h>
#define __USE_GNU
#include <pthread.h>
pthread_barrier_t barrier;
void *fun1(){
	int a[1024*1024]={1};
	pthread_barrier_wait(&barrier);
}
void *fun2(){
	int b[1024*1024]={1};
	pthread_barrier_wait(&barrier);
}
int main(){
	int a[5];
	for(int i=0;i<5;i++){
		a[i]=1;
	}
	for(int i=0;i<5;i++){
		printf("%d ",a[i]);
	}
	printf("\n");
	int b[5]={0};
	memcpy(b,a,sizeof(a));
	for(int i=0;i<5;i++){
		printf("%d ",b[i]);
	}
	printf("\n%d\n",sizeof(a));
}