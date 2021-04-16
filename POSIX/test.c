#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>


/*
        两个线程分别对a进行+1,最后由主线程输出其值.
*/
int a=0;

pthread_mutex_t numlock; //互斥量
pthread_barrier_t b; //屏障

void* handle(void *data)
{
        pthread_mutex_lock(&numlock);
        a++;
        pthread_mutex_unlock(&numlock);
        pthread_barrier_wait(&b);
        return 0;
}


int main()
{
        pthread_t t1,t2;
        pthread_barrier_init(&b,NULL,3); //初始化屏障
        pthread_mutex_init(&numlock,NULL);
        pthread_create(&t1,NULL,handle,NULL);
        pthread_create(&t2,NULL,handle,NULL);
        pthread_barrier_wait(&b);
        printf("a=:%d\n",a);
        exit(0);
}