#include <unistd.h>
#include <stdio.h>

/**
 * infinite_while - an infinity loop
 * Return: always 0
*/
int infinite_while(void)
{
	while (1)
	{
		sleep(1);
	}
	return (0);
}
/**
 * main - creats an 5 zombies process
 * Return: always 0
*/
int main(void)
{
	int pid, i = 0;

	while (i < 5)
	{
		pid = fork();
		if (pid > 0)
		{
			printf("Zombie process created, PID: %d\n", pid);
			sleep(1);
			i++;
		}
		else
			return (0);
	}
	infinite_while();
	return (0);
}
