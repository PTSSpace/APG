
#include <assert.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <errno.h>

typedef struct {
  char a;
  char b;
  char c;
  char d;
  char e;
  int32_t i;
  uint32_t ui;
  char str[3];
} mystruct;

const char *path = "output/output_py";

int main() {
  uint32_t mysize = sizeof(mystruct);

  // read file writen with py
  mystruct *myobject = malloc(mysize);
  FILE * readfilepy = fopen(path, "rb");
  if (readfilepy != NULL) {
    fread(myobject, mysize, 1, readfilepy);
    fclose(readfilepy);
  }

  printf("%c %c %c %c %c %i %u %s\n",
  myobject->a,
  myobject->b,
  myobject->c,
  myobject->d,
  myobject->e,
  myobject->i,
  myobject->ui,
  myobject->str
  );

  assert(
    myobject->a == '\x96'
    && "a must be \x96"
  );
  assert(
    myobject->b == '\xFF'
    && "b must be \xFF"
  );
  assert(
    myobject->c == '\xB0'
    && "c must be \xB0"
  );
  assert(
    myobject->d == '\x1A'
    && "d must be \x1A"
  );
  assert(
    myobject->e == '\x23'
    && "e must be \xB0"
  );
  assert(
    myobject->i == -1
    && "i must be -1"
  );
  assert(
    myobject->ui == 2
    && "ui must be 2"
  );
  assert(
    strcmp(myobject->str, "abc") == 0
    && "str must be abc"
  );

  free(myobject);

  return 0;
}