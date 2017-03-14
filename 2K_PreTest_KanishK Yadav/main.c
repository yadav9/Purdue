/*
 * Programmer: Kanishk Yadav
 * Project: 2K Pre-Test
 * File Desc: The program outputs the minimum time required before a message sent
 * from the capitol (city #1) throughout the empire, i.e. the time it is received
 * in the last city to get the message.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

typedef enum { false, true } bool;
int **allocateMapMemory(int size);
void readFromFileAndFillAdjMatrix(FILE *fMap, int **map, int numOfCities);
int minDistance(int dist[], bool sptSet[], int numOfCities);
void findMinTimeToDeliverAllMsgs(int **map, int src, int numOfCities);
void freeMapMemory(int **map, int size);

int main(int argc, char **argv)
{
    //Check number of arguments
    if(argc != 2)
    {
        fprintf(stderr, "Function call must be of type: ./2kpretest input_map.txt\n");
        return 0;
    }

    //Open input file
    FILE *fMap;
    fMap = fopen(argv[1], "r");
    if(fMap == NULL)
    {
        fprintf(stderr, "Map file (%s) could not be opened\n", argv[1]);
        return 0;
    }

    //read number of cities
    int numOfCities = -1;
    fscanf(fMap,"%d",&numOfCities);
    if(numOfCities == -1)
    {
        fprintf(stderr, "Error. Cannot read (%s) header properly.\n", argv[1]);
        fclose(fMap);
        return 0;
    }

    int **map = allocateMapMemory(numOfCities);
    if(map == NULL)
    {
        fclose(fMap);
        return 0;
    }
    readFromFileAndFillAdjMatrix(fMap, map, numOfCities);
    findMinTimeToDeliverAllMsgs(map, 0, numOfCities);
    freeMapMemory(map, numOfCities);
    fclose(fMap);
    return 1;
}

/*
 * @description : Allocates memory for the Adjacency Matrix of the graph
 * @return : retuns a 2d array block of memory of int
 * @argument : takes in size of 2d square array
 */

int **allocateMapMemory(int size)
{
    int **map;
    int i;
    map = calloc(size, sizeof(int*));
    if(map == NULL)
    {
        fprintf(stderr, "Memory Allocation failed\n");
        return NULL;
    }

    for(i = 0; i < size; ++i)
    {
        map[i] = calloc(size, sizeof(int));

        if(map[i] == NULL)
        {
            fprintf(stderr, "Memory Allocation failed\n");
            return NULL;
        }
    }
    return map;
}


/*
* @description : reads from input file and fills up the Adj. Matrix
* @return : void
* @argument : takes in file pointer, 2d map array and number of cities
*/

void readFromFileAndFillAdjMatrix(FILE *fMap, int **map, int numOfCities)
{
    int row = 0;
    int col = 0;
    char line[256];

    while(fgets(line, sizeof(line), fMap))
    {
        char *tempLine = strtok(line," ");
        col = 0;
        while(tempLine != NULL)
        {
            if(*tempLine == 'x')
            {
                map[row][col] = 0;
            }
            else
            {
                map[row][col] = atol(tempLine);
            }
            col++;
            tempLine = strtok(NULL," ");
        }
        row++;
    }

    for(row = 0; row < numOfCities; ++row)
    {
        for(col = row + 1; col < numOfCities; ++col)
        {
            map[row][col] = map[col][row];
        }
    }
    return;
}


/*
* @description : find the min distance
* @return : retuns the index of min distance
* @argument : takes in dist array, aptSet array and number of cities
*/

int minDistance(int dist[], bool sptSet[], int numOfCities)
{
    int min = INT_MAX;
    int minIndex;
    int i;
    for(i = 0; i < numOfCities; ++i)
    {
        if (sptSet[i] == false && dist[i] <= min)
        {
            min = dist[i];
            minIndex = i;
        }
    }

    return minIndex;
}


/*
* @description : finds minimum time to deliver all messages using Dijkstra
*                algorithm
* @return : void
* @argument : takes in the Adj. matrix, src city (Capitol city) and num of cities
*/

void findMinTimeToDeliverAllMsgs(int **map, int src, int numOfCities)
{
    int dist[numOfCities];
    bool sptSet[numOfCities];
    int maxDist = INT_MIN;
    int i;
    for(i = 0; i < numOfCities; ++i)
    {
        dist[i] = INT_MAX;
        sptSet[i] = false;
    }

    // Distance of source vertex from itself is always 0
    dist[src] = 0;

    for(i = 0; i < (numOfCities - 1); ++i)
    {
        int tempMinDistance = minDistance(dist, sptSet, numOfCities);
        sptSet[tempMinDistance] = true;
        int j;
        for(j = 0; j < numOfCities; ++j)
        {
            if (!sptSet[j] && map[tempMinDistance][j] && dist[tempMinDistance] != INT_MAX
                && dist[tempMinDistance] + map[tempMinDistance][j] < dist[j])
            {
                dist[j] = dist[tempMinDistance] + map[tempMinDistance][j];
            }
        }
    }

    for(i = 0; i < numOfCities; ++i)
    {
        if(dist[i]  > maxDist)
        {
            maxDist = dist[i];
        }

    }

    printf("The minimum time required before message is sent out from the capitol throughtout the empire is : %d\n", maxDist);
    return;
}


/*
* @description : frees the memory for the 2d Adj. matrix
* @return : void
* @argument : takes in size of 2d square array and pointer to 2d array 
*/

void freeMapMemory(int **map, int size)
{
    int i;
    for(i = 0; i < size; ++i)
    {
        free(map[i]);
    }
    free(map);
    return;
}
