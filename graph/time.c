#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <time.h>

struct timespec start, end;
int main() {
  clock_gettime(CLOCK_MONOTONIC_RAW, &start);
  // do stuff
  int max = INT_MAX;
  for (int32_t i = 0; i < max; i++) {
    asm volatile("" : : "r"(i));
  }
  clock_gettime(CLOCK_MONOTONIC_RAW, &end);
  uint64_t delta_us = (end.tv_sec - start.tv_sec) * 1000000 +
                      (end.tv_nsec - start.tv_nsec) / 1000;
  printf("Time taken: %llu\n", delta_us);
}
