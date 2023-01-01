
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

const char *path = "output/output_c";

int main() {
  uint32_t mysize = sizeof(mystruct);
  mystruct *myobject=malloc(mysize);

  // fill struct
  myobject->a = '\x96';
  myobject->b = '\xFF';
  myobject->c = '\xB0';
  myobject->d = '\x1A';
  myobject->e = '\x23'; // -> #
  myobject->i = -1;
  myobject->ui = 2;
  strcpy(myobject->str, "abc");

  // write
  FILE * writefile = fopen(path, "wb");
  if (writefile != NULL) {
    fwrite(myobject, mysize, 1, writefile);
    fclose(writefile);
  }
  free(myobject);

  // read
  mystruct *myobject2 = malloc(mysize);
  FILE * readfile = fopen(path, "rb");
  if (readfile != NULL) {
    fread(myobject2, mysize, 1, readfile);
    fclose(readfile);
  }

  assert(
    myobject2->a == '\x96'
    && "a must be \x96"
  );
  assert(
    myobject2->b == '\xFF'
    && "b must be \xFF"
  );
  assert(
    myobject2->c == '\xB0'
    && "c must be \xB0"
  );
  assert(
    myobject2->d == '\x1A'
    && "d must be \x1A"
  );
  assert(
    myobject2->e == '\x23'
    && "e must be \xB0"
  );
  assert(
    myobject2->i == -1
    && "i must be -1"
  );
  assert(
    myobject2->ui == 2
    && "ui must be 2"
  );
  assert(
    strcmp(myobject2->str, "abc") == 0
    && "str must be abc"
  );

  free(myobject2);

  return 0;
}