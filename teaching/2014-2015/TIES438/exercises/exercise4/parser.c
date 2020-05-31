#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct atomStruct atomStruct;
struct atomStruct{
    double x,y,z;
    double vx,vy,vz;
};

typedef struct molecule molecule;
struct molecule {
     atomStruct atoms[16];
     int outcome;    
};

/**
 * parse parses 'amount' molecules encoded in the file with name 'filename' into the molecule array.
 */
void parse(molecule res[], int amount, char *filename){
    
    FILE *fp;
    int i, moleculeNumber;
    
    int lineBufferSize = 100;
    char* lineBuffer = malloc(sizeof(char) * lineBufferSize);
    
    if ((fp = fopen(filename, "r")) == NULL) {
        fprintf(stderr, "Could not open file: %s\n", filename);
        exit(EXIT_FAILURE);
    }
    for (moleculeNumber = 0; moleculeNumber < amount; moleculeNumber++){
        //header
        if (fgets(lineBuffer, lineBufferSize, fp) == NULL){
            fprintf(stderr, "Could not read next line\n");
            exit(EXIT_FAILURE);
        }
        int * outcome = &(res[moleculeNumber].outcome);
        sscanf(lineBuffer,"Outcome: %i", outcome);
        //skip line
        if (fgets(lineBuffer, lineBufferSize, fp) == NULL){
            fprintf(stderr, "Could not read next line\n");
            exit(EXIT_FAILURE);
        }
        //read 16 atoms
        for (i = 0; i < 16; i++) {
            if (fgets(lineBuffer, lineBufferSize, fp) == NULL){
                fprintf(stderr, "Could not read next line\n");
                exit(EXIT_FAILURE);
            }
            atomStruct * a = &(res[moleculeNumber].atoms[i]);
            //    1SB2     NZ    1  -0.020   0.016  -0.029  0.5938 -0.1478 -0.3879    
            //skip first 22 characters!
            sscanf(lineBuffer  + (22 * sizeof(char)),"%lf %lf %lf %lf %lf %lf", &a->x,&a->y,&a->z,&a->vx,&a->vy,&a->vz);
            
        }
        //skip line
        if (fgets(lineBuffer, lineBufferSize, fp) == NULL){
            fprintf(stderr, "Could not read next line\n");
            exit(EXIT_FAILURE);
        }

    }

    free(lineBuffer);

    fclose(fp);
}

void printMolecule(molecule *m){
    int i;
    printf("Result : %d\n", m->outcome);
    for (i = 0; i < 16; i++){
        atomStruct * atom = &(m->atoms[i]);
        printf("%lf %lf %lf %lf %lf %lf\n", atom->x,atom->y,atom->z,atom->vx,atom->vy,atom->vz);
    }
}

int main(int argc, char **argv)
{
    int i;    
//    char input_file[] = "diabatic.txt";
 //   int amount = 296;
    
    char input_file[] = "ffsh.dat";
    int amount = 509;
    
    molecule molecules[amount];
    

    parse(molecules, amount, input_file);

    //printf("%d\n", molecules[0].outcome);
    for (i = 0; i < amount; i++){
        printMolecule (&(molecules[i]));
    }

    //The following could be used to get the data as double arrays of size 96
    //Classified as black magic, this happens to work in C on common architectures. http://www.catb.org/esr/structure-packing/
    //Might or might not work in C++, be careful
    double *asDoubleArray = (double *) (molecules[1].atoms);

    for(i = 0; i < 16*6; i++){
        printf("%lf ", asDoubleArray[i]);
    }

    return 0;
}
