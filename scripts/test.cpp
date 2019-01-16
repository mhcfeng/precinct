#include <stdio.h>
#include <time.h>
#include <iostream>
int main( int argc, char** argv ) {
  time_t start = time(0);
  int n=15576;
  for (int i=0; i<n; i++){
    for (int j=i; j<n; j++) {
      for(int k=j; k<n; k++) {
        i;
      }
    }
  }
  time_t end = time(0);
  double time = difftime(end,start);
  std::cout << time << std::endl;
}
