#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

int main(int argc, char** argv) {
    // ha nincs semmi argument az nem jo
    if(argc == 1) {
        return 1;
    }

    // elso argument az a command ami a block outputot
    // adja (megjelenites)
    const char* output_command = *(argv + 1);

    // ebben a csodaszep environment variableben van a megnyomott
    // egergomb kodja (1 = left, 2 = right, 3 = middle, stb)
    // ezeket a kodokat a dwm configban lehet definialni
    // amiket irtam azok a defaultok amik a patchben vannak
    const char* button_variable_raw = getenv("BLOCK_BUTTON");

    if(button_variable_raw != NULL) {
        int button_id = atoi(button_variable_raw);
        
        // szepen leelenorizzuk van-e ehhez a gombhoz tartozo
        // command
        if(button_id >= 1 && button_id < argc - 1) {
            const char* click_command = *(argv + button_id + 1);

            // szepen csinalunk egy uj processt mert nem akarjuk
            // hogy a megnyitott gui programra varakozzon az
            // egesz block (nem updatelene)
            if(fork() == 0) {
                // output annyira nem erdekel most feltetlen
                int null_output = open("/dev/null", O_WRONLY | O_CREAT, 0666);
                dup2(null_output, fileno(stdout));
                dup2(null_output, fileno(stderr));

                // irany surany
                system(click_command);

                close(null_output);   
                return 0;
            }
        }
    }

    // jo kis output
    return system(output_command);
}