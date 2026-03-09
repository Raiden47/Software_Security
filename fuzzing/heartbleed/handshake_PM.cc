// Copyright 2016 Google Inc. All Rights Reserved.
// Licensed under the Apache License, Version 2.0 (the "License");
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <assert.h>
#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <unistd.h>
#include <limits.h>

__AFL_FUZZ_INIT();

#ifndef CERT_PATH
# define CERT_PATH
#endif

// To ensure checks are not optimized out it is recommended to disable
// code optimization for the fuzzer harness main() 
#pragma clang optimize off
#pragma GCC optimize("O0")

SSL_CTX *Init() {
  SSL_library_init();
  SSL_load_error_strings();
  ERR_load_BIO_strings();
  OpenSSL_add_all_algorithms();
  SSL_CTX *sctx;
  assert (sctx = SSL_CTX_new(TLSv1_method()));
  /* These two file were created with this command:
      openssl req -x509 -newkey rsa:512 -keyout server.key \
     -out server.pem -days 9999 -nodes -subj /CN=a/
  */
  assert(SSL_CTX_use_certificate_file(sctx, "server.pem",
                                      SSL_FILETYPE_PEM));
  assert(SSL_CTX_use_PrivateKey_file(sctx, "server.key",
                                     SSL_FILETYPE_PEM));
  return sctx;
}

int main() {
  static SSL_CTX *sctx = Init();
  
  #ifndef __AFL_HAVE_MANUAL_CONTROL
  // AFL Persisten mode
  __AFL_INIT();
  #endif //__AFL_HAVE_MANUAL_CONTROL
  
  unsigned char *data = __AFL_FUZZ_TESTCASE_BUF;
  
  while (__AFL_LOOP(UINT_MAX)){
  	SSL *server = SSL_new(sctx);
  	BIO *sinbio = BIO_new(BIO_s_mem());
  	BIO *soutbio = BIO_new(BIO_s_mem());
  	SSL_set_bio(server, sinbio, soutbio);
  	SSL_set_accept_state(server);

  	/* TODO: To spoof one end of the handshake, we need to write data to sinbio
  	 * here */
  
  	int size = __AFL_FUZZ_TESTCASE_LEN;
  	
  	read(STDIN_FILENO, data, size);
  
 	BIO_write(sinbio, data, size);
  	SSL_do_handshake(server);
  	SSL_free(server);
  }
  return 0;
}
