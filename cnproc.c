#include <unistd.h>
#include <stdio.h>

int main() {
int num_processors = sysconf(_SC_NPROCESSORS_CONF);
printf("%d\n", num_processors);
}