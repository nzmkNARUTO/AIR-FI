#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#define __USE_GNU
#include <pthread.h>
#include <sched.h>
#include "algorithm1/alg1.h"

pthread_barrier_t barrier;
void *fun(void *param){
    int cpu=*(int*)param;
    printf("cpu%d\n",cpu);
    cpu_set_t mask;
    CPU_ZERO(&mask);
    CPU_SET(cpu,&mask);
    if (pthread_setaffinity_np(pthread_self(),sizeof(mask),&mask)<0)
    {
        printf("fun bind error\n");
        return;
    }

    int a[1024*256]={1};
    int b[1024*256]={1};
	int i = 0;
	clock_t start;

    pthread_barrier_wait(&barrier);
    start = clock();
    while (clock()<start+1*CLOCKS_PER_SEC)
    {
        i++;
    	memcpy(a, b, 1024 * 256);
    	//memset(b, 0, 1024 * 1024);
    	memcpy(b, a, 1024 * 256);
        printf("%d\n",i);
    }
}

int main(int argc, char** argv){
    int cpus=sysconf(_SC_NPROCESSORS_ONLN);
    printf("cpu count %d\n",cpus);
    int *cpu=(int*)malloc(cpus*sizeof(int));
    for(int i=0;i<cpus;i++){
        cpu[i]=i;
    }
    while(1){
        pthread_t thread;
        pthread_barrier_init(&barrier,NULL,cpus+1);
        for(int i=0;i<cpus;i++){
            if (pthread_create(&thread, NULL, fun, cpu+i) != 0)
            {
                printf("create thread %d error\n",i);
            }
        }
        printf("main\n");
        pthread_barrier_wait(&barrier);
        pthread_join(thread,NULL);
        sleep(1);
    }
}