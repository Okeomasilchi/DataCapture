CC = gcc
CFLAGS = -Wall -Werror -Wextra -pedantic

setenviron: env.c
	$(CC) $(CFLAGS) env.c -o setenviron
	sudo mv setenviron /usr/bin/

clean:
	rm -f setenviron *.o
