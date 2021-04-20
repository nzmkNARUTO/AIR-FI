#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#define __USE_GNU
#include <pthread.h>
#include <sched.h>
#include "alg1.h"
int cpus;

pthread_barrier_t barrier;
void *fun(void *param){
    int cpu=*(int*)param;
    // printf("cpu%d\n",cpu);
    cpu_set_t mask;
    CPU_ZERO(&mask);
    CPU_SET(cpu,&mask);
    if (pthread_setaffinity_np(pthread_self(),sizeof(mask),&mask)<0)
    {
        printf("fun bind error\n");
        return;
    }

    int a[1024*256];
    int b[1024*256];
    for(int i=0;i<1024*256;i++){
        a[i]=1;
        b[i]=0;
    }
	int i = 0;
	clock_t start;

    pthread_barrier_wait(&barrier);
    start = clock();
    while (clock()<start+cpus*CLOCKS_PER_SEC/2)
    {
        i++;
        memcpy(a, b, sizeof(a));
        memcpy(b, a, sizeof(b));
        // if(i%100==0)
        //     printf("cpu:%d,%d\n",cpu,i);
    }
}

int main(int argc, char** argv){
    cpus=sysconf(_SC_NPROCESSORS_ONLN);
    printf("cpu count %d\n",cpus);
    int *cpu=(int*)malloc(cpus*sizeof(int));
    for(int i=0;i<cpus;i++){
        cpu[i]=i;
    }
    char payload[4];
    printf("input:");
    scanf("%s",payload);
    char *p=packet(payload);
    char currentChar;
    for(int i=0;i<6;i++){
        currentChar=p[i];
        for(int j=0;j<8;j++){
            if(currentChar&0x80){
                pthread_t thread;
                pthread_barrier_init(&barrier,NULL,cpus+1);
                for(int i=0;i<cpus;i++){
                    if (pthread_create(&thread, NULL, fun, cpu+i) != 0)
                    {
                        printf("create thread %d error\n",i);
                    }
                }
                printf("1");
                pthread_barrier_wait(&barrier);
                pthread_join(thread,NULL);
            }else{
                printf("0");
                usleep(1000000/2);
            }
            currentChar=currentChar<<1;
        }
        printf(" %c\n",p[i]);
    }
}