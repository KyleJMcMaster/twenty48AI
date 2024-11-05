#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <float.h>
#include <stdbool.h>
#include <unistd.h>
#include <math.h>



typedef struct{
    // each row is represented by a char, starting in top right corner
    // each char represents the power of the tile (2^tile_value), unless it is 0 in which case 00000000 = 0 != 2^0
    // score represents the current score in the game

    char tiles[16]; 
    int score; 
} Board;

typedef enum{
    UP = 2,
    DOWN = 3,
    LEFT = 1,
    RIGHT = 0,
    NONE = -1
}Move;

static Move moves[4] = {UP, DOWN, LEFT, RIGHT};

double get_rand() {return (double)rand() / (double) RAND_MAX;}


int apply_move(Board* board, Move move){
    //modifies referenced board by applying specified move
    //returns 1 if move is valid
    int valid_move = 0;
    switch(move){
        case UP:
            for(int col = 0; col < 4; col++){
                for(int t1 = col; t1 <= 8+col; t1 += 4){//stop at second last row
                    for(int t2 = t1 + 4; t2 <= 12+col; t2 += 4){
                        if(board->tiles[t2] != 0){
                            if(board->tiles[t2] == board->tiles[t1]){
                                //tiles match, combine
                                board->tiles[t1]++;
                                board->tiles[t2] = 0;
                                valid_move = 1;
                                board->score += (2 << (board->tiles[t1]-1));
                                break;
                            }
                            else if(board->tiles[t1] == 0){
                                //starting tile is 0, move tile to blank space and look for future combinations
                                board->tiles[t1] = board->tiles[t2];
                                board->tiles[t2] = 0;
                                valid_move = 1;
                            }
                            else{
                                //tiles do not match, do nothing
                                break;
                            }
                        }
                    }
                }
            }
            break;
        case DOWN:
            for(int col = 0; col < 4; col++){
                    for(int t1 = 12+col; t1 >= 4+col; t1 -= 4){//stop at second last row
                        for(int t2 = t1 - 4; t2 >= col; t2 -= 4){
                            if(board->tiles[t2] != 0){
                                if(board->tiles[t2] == board->tiles[t1]){
                                    //tiles match, combine
                                    board->tiles[t1]++;
                                    board->tiles[t2] = 0;
                                    valid_move = 1;
                                    board->score += (2 << (board->tiles[t1]-1));
                                    break;
                                }
                                else if(board->tiles[t1] == 0){
                                    //starting tile is 0, move tile to blank space and look for future combinations
                                    board->tiles[t1] = board->tiles[t2];
                                    board->tiles[t2] = 0;
                                    valid_move = 1;
                                }
                                else{
                                    //tiles do not match, do nothing
                                    break;
                                }
                            }
                        }
                    }
                }
            break;
        case LEFT:
            for(int row = 0; row <= 12; row += 4){
                    for(int t1 = row; t1 <= row + 2; t1++){//stop at second last col
                        for(int t2 = t1 + 1; t2 <= row + 3; t2++){
                            if(board->tiles[t2] != 0){
                                if(board->tiles[t2] == board->tiles[t1]){
                                    //tiles match, combine
                                    board->tiles[t1]++;
                                    board->tiles[t2] = 0;
                                    valid_move = 1;
                                    board->score += (2 << (board->tiles[t1]-1));
                                    break;
                                }
                                else if(board->tiles[t1] == 0){
                                    //starting tile is 0, move tile to blank space and look for future combinations
                                    board->tiles[t1] = board->tiles[t2];
                                    board->tiles[t2] = 0;
                                    valid_move = 1;
                                }
                                else{
                                    //tiles do not match, do nothing
                                    break;
                                }
                            }
                        }
                    }
                }
            break;
        case RIGHT:
            for(int row = 3; row <= 15; row += 4){
                    for(int t1 = row; t1 >= row -2; t1--){//stop at second last col
                        for(int t2 = t1 - 1; t2 >= row - 3; t2--){
                            if(board->tiles[t2] != 0){
                                if(board->tiles[t2] == board->tiles[t1]){
                                    //tiles match, combine
                                    board->tiles[t1]++;
                                    board->tiles[t2] = 0;
                                    valid_move = 1;
                                    board->score += (2 << (board->tiles[t1]-1));
                                    break;
                                }
                                else if(board->tiles[t1] == 0){
                                    //starting tile is 0, move tile to blank space and look for future combinations
                                    board->tiles[t1] = board->tiles[t2];
                                    board->tiles[t2] = 0;
                                    valid_move = 1;
                                }
                                else{
                                    //tiles do not match, do nothing
                                    break;
                                }
                            }
                        }
                    }
                }
            break;

    }
    return valid_move;
}

int check_valid_move(Board* board, Move move){
    //makes a copy of passed board and checks if move is valid on the board
    //returns 1 if move is valid
    int board_cp[16];
    for(int i = 0; i < 16; i ++){
        board_cp[i] = board->tiles[i];
    }

    switch(move){
        case UP:
            for(int col = 0; col < 4; col++){
                for(int t1 = col; t1 <= 8+col; t1 += 4){//stop at second last row
                    for(int t2 = t1 + 4; t2 <= 12+col; t2 += 4){
                        if(board_cp[t2] != 0){
                            if(board_cp[t2] == board_cp[t1]){
                                //tiles match, combine
                                board_cp[t1]++;
                                board_cp[t2] = 0;
                                return 1;
                            }
                            else if(board_cp[t1] == 0){
                                //starting tile is 0, move tile to blank space and look for future combinations
                                board_cp[t1] = board_cp[t2];
                                board_cp[t2] = 0;
                                return 1;
                            }
                            else{
                                //tiles do not match, do nothing
                                break;
                            }
                        }
                    }
                }
            }
            break;
        case DOWN:
            for(int col = 0; col < 4; col++){
                    for(int t1 = 12+col; t1 >= 4+col; t1 -= 4){//stop at second last row
                        for(int t2 = t1 - 4; t2 >= col; t2 -= 4){
                            if(board_cp[t2] != 0){
                                if(board_cp[t2] == board_cp[t1]){
                                    //tiles match, combine
                                    board_cp[t1]++;
                                    board_cp[t2] = 0;
                                    return 1;
                                }
                                else if(board_cp[t1] == 0){
                                    //starting tile is 0, move tile to blank space and look for future combinations
                                    board_cp[t1] = board_cp[t2];
                                    board_cp[t2] = 0;
                                    return 1;
                                }
                                else{
                                    //tiles do not match, do nothing
                                    break;
                                }
                            }
                        }
                    }
                }
            break;
        case LEFT:
            for(int row = 0; row <= 12; row += 4){
                    for(int t1 = row; t1 <= row + 2; t1++){//stop at second last col
                        for(int t2 = t1 + 1; t2 <= row + 3; t2++) {
                            if(board_cp[t2] != 0){
                                if(board_cp[t2] == board_cp[t1]){
                                    //tiles match, combine
                                    board_cp[t1]++;
                                    board_cp[t2] = 0;
                                    return 1;
                                }
                                else if(board_cp[t1] == 0){
                                    //starting tile is 0, move tile to blank space and look for future combinations
                                    board_cp[t1] = board_cp[t2];
                                    board_cp[t2] = 0;
                                    return 1;
                                }
                                else{
                                    //tiles do not match, do nothing
                                    break;
                                }
                            }
                        }
                    }
                }
            break;
        case RIGHT:
            for(int row = 3; row <= 15; row += 4){
                    for(int t1 = row; t1 >= row -2; t1--){//stop at second last col
                        for(int t2 = t1 - 1; t2 >= row - 3; t2--){
                            if(board_cp[t2] != 0){
                                if(board_cp[t2] == board_cp[t1]){
                                    //tiles match, combine
                                    board_cp[t1]++;
                                    board_cp[t2] = 0;
                                    return 1;
                                }
                                else if(board_cp[t1] == 0){
                                    //starting tile is 0, move tile to blank space and look for future combinations
                                    board_cp[t1] = board_cp[t2];
                                    board_cp[t2] = 0;
                                    return 1;
                                }
                                else{
                                    //tiles do not match, do nothing
                                    break;
                                }
                            }
                        }
                    }
                }
            break;

    }
    return 0;
}

int get_empty_tiles(Board* board, int* empty_tiles){
    //adds empty tile indicies to 0:length positions of the empty_tiles list
    // returns the length of the empty_tiles array
    int length = 0;
    for(int i = 0; i < 16; i++){
        if(board->tiles[i] == 0){
            empty_tiles[length] = i;
            length++;
        }
    }
    return length;
}

int get_valid_moves(Board* board, int* valid_moves){
    int length = 0;
    for(int i = 0; i <4; i ++){
        if (check_valid_move(board, moves[i])){
            valid_moves[length] = moves[i];
            length++;
        }
    }
    return length;
}

void set_tile(Board* board, int position, char value){
    //value should be in exp representation
    board->tiles[position] = value;
}

int get_score(Board* board){
    return board->score;
}

void copy_board_values(Board* b1, Board* b2){
    //copies values from b1 into b2
    b2->score = b1->score;
    for(int i = 0; i < 16; i++){
        b2->tiles[i] = b1->tiles[i];
    }
}

void powerep_to_intrep(char* powerrep, int* intrep){
    //converts from char based power rep to nice looking int rep
    for(int i = 0; i < 16; i++){
        intrep[i] = (2 << (powerrep[i]-1)) * (powerrep[i]!=0);
    }
}

void intrep_to_powerrep(char* powerrep, int* intrep){
    //converts from int rep to power rep
    for(int i = 0; i < 16; i++){
        if(intrep[i] == 0){
            powerrep[i] = 0;
        }else{
            powerrep[i] = sizeof(int) * 8 - __builtin_clz(intrep[i]) - 1;
        }
    }
}

static void print_board(Board* board){
    int tiles[16];
    powerep_to_intrep((board->tiles), tiles);

    for(int i = 0; i < 16; i++){
        printf("%d   ", tiles[i]);
        if(i%4==3){
            printf("\n");
        }
    }
    printf("\n");
}

double estimate_score(Board* board, double* params){
    // use heuristic to estimate score
    /*
    [0]: depth
    [1]: path_penalty
    [2]: loss_penalty
    [3]: score_factor
    */
   double score = (double)board->score;
   double penalty = 0;
   int tiles[16];
   powerep_to_intrep(board->tiles, tiles);

   //loss penalty
   int valid_moves[4];
    if(!get_valid_moves(board, valid_moves)){
        penalty += params[2];
    }

    //path penalty
    int path[16] = {3,2,1,0,4,5,6,7,11,10,9,8,12,13,14,15};
    double path_pen = 0;
    for(int i = 0; i<15; i++){
        if(tiles[path[i]] > tiles[path[i+1]]){
            path_pen += tiles[path[i]] - tiles[path[i+1]];
        }
    }
    penalty += params[1] * path_pen;

    return params[3] * score - penalty;

}

double expectiminmax(Board* board, double* params, bool choose_move, int depth){
    // use expectiminmax to evaluate states
    // Choose move == 1 indicates the current state is the users turn to choose the move
    // else, random state
    double result;
    int loss = 1;
    int valid_moves[4];
    int num_valid_moves = get_valid_moves(board, valid_moves);
    if(num_valid_moves){
        loss = 0;
    }

    if(depth == 0 || loss){
        return estimate_score(board, params);
    }

    if(choose_move){
        result = params[2];
        for(int i = 0; i < num_valid_moves; i ++){
            Board b1;
            copy_board_values(board, &b1);
            apply_move(&b1, valid_moves[i]);
            double emm_result = expectiminmax(&b1, params, false, depth-1);
            result = (result > emm_result) ? result : emm_result;
            
        }
    }else{
        result = 0;
        int empty_tiles[16];
        int empty_len = get_empty_tiles(board, empty_tiles);
        for(int i = 0; i < empty_len; i++){
            Board b1;
            Board b2;
            copy_board_values(board, &b1);
            copy_board_values(board, &b2);

            set_tile(&b1, empty_tiles[i], 1); //set with exp value
            set_tile(&b2, empty_tiles[i], 2);

            result += 0.9/empty_len * expectiminmax(&b1, params, true, depth-1);
            result += 0.1/empty_len * expectiminmax(&b2, params, true, depth-1);
        }

    }
    return result;
}





int get_next_move(int* tiles, int score, double* params){
    /*takes in the set of tiles (in int rep form), the current score, and a set of parameters
        [0]: depth
        [1]: path_penalty
        [2]: loss_penalty
        [3]: score_factor
     returns the best move from this state
    */
    int start_val = -1000000000;
    char powertiles[16];
    intrep_to_powerrep(powertiles, tiles);

    Board b; 
    for(int i =  0; i < 16; i ++){
        b.tiles[i] = powertiles[i];
    }
    b.score = score;

    //print_board(&b);
    int valid_moves[4];
    int num_valid_moves = get_valid_moves(&b, valid_moves);
    double scores[num_valid_moves];
    double max_score = start_val;
    Move max_move;
    if(num_valid_moves){
        max_move = valid_moves[0];
    }
    else{return moves[0];}
    

    for(int i=0; i<num_valid_moves; i++){
        //printf("is_valid: %d\n", check_valid_move(&b, moves[i]));

        Board b_cp;
        copy_board_values(&b, &b_cp);
        apply_move(&b_cp, valid_moves[i]);
        scores[i] = expectiminmax(&b_cp, params, false, params[0]-1);
        if (max_score < scores[i]){
            max_score = scores[i];
            max_move = valid_moves[i];
        }

        //printf("%d: %f\n, ", moves[i], scores[i]);
        

    }

    
    return max_move;


}
double KL_divergence(double p, double q){
    //Gets the kl divergence KL(p||q) for two bernoulli variables
    // p is the probability of dist 1 being 1
    // q is the probability of dist 2 being 1
    if(p == q){return 0;}
    else if(q == 0 || q == 1){return (p == 0) ? 0.0 : INFINITY;} //avoid log(0)
    else{
        return p * (log(p) - log(q)) + (1-p)*(log(1-p)-log(1-q));
    }
}

double compute_w_star(double* means, int best_arm_index, double tolerance, int max_iterations){
    //computes the minimum sample complexity to identify best arm with confidence level (1-delta) using bisection method

    double W_min = 0;
    double W_max = 1;
    double W_mid;
    double KL_d;
    double best_mean = means[best_arm_index];
    bool feasible;
    

    for(int i = 0; i < max_iterations; i ++){
        W_mid = (W_min + W_max)/2.0;
        feasible = true;
        for(int j = 0; j < 4; j++){
            if(j != best_arm_index){
                KL_d = KL_divergence(best_mean, means[j]);
                if(KL_d == 0 || W_mid * KL_d > 1){
                    feasible = false;
                    printf("%d\n", i);
                    break;
                }
            }
        }

        if(feasible){
            W_min = W_mid; // increase W_min to find max feasible
        }
        else{
            W_max = W_mid; // reduce to find max feasible
        }

        if (W_max - W_min < tolerance){
            printf("%d\n", i);
            break;
        }
    }
    return W_min;
}
void place_random_tile(Board* board){
    // place a tile in a randomly selected empty square
    
    int empty_tiles[15];
    int len_empty_tiles = get_empty_tiles(board, empty_tiles);
    int tile = empty_tiles[rand() % (len_empty_tiles)];
    int tile_value = ((double)rand()/(double)RAND_MAX > 0.1) ? 1 : 2;

    board->tiles[tile] = tile_value;
    }
    
  

bool run_trial_until_win(Board* board, int stop){
    // run a trial until either the game is won or lost and return the result
    // stop is an exp rep value which specifies the maximum tile required to consider the game as won

    int c = 0;
    Move next_move;

    while(true){
        int valid_moves[4];
        int num_valid_moves = get_valid_moves(board, valid_moves);
        
        if(!num_valid_moves){
            return 0;
        }
        int index = rand() % (num_valid_moves);
        next_move = valid_moves[index];      
        apply_move(board, next_move);
        
        for(int i = 0; i < 16; i++){
            if (board->tiles[i] >= stop){
                print_board(board);
                return 1;
            }
        }
        place_random_tile(board);
      
    }
}

int track_and_stop(Board* board, double* params){
    int n[4] = {0,0,0,0};
    double means[4] = {0,0,0,0};
    double confidence = params[0];
    int max_trials = params[1];
    double w_tolerance = params[2];
    int max_w_iterations = params[3];

    double exploration_threshold;
    Move min_underexplored_arm;
    Move next_arm;
    Move best_arm = RIGHT;
    double W_star;
    double best_arm_score;

    srand(time(NULL));

    //step 0: run first trial

    for(int t = 0; t < max_trials; t++){
        
        //step 1: check for underexplored arms, and find minimum
        min_underexplored_arm = NONE; //defined as -1 in enum
        exploration_threshold = sqrt(t) - 2;

        for(int i = 0; i < 4; i++){
            if(n[i] < exploration_threshold && (min_underexplored_arm == -1 || n[i] < n[min_underexplored_arm])){
                min_underexplored_arm == i;
            }
        }

        //step 2: select arm using D-tracking

        if (min_underexplored_arm != NONE){
            // forced exploration
            next_arm = min_underexplored_arm;
        }
        else{
            // direct tracking
            W_star = compute_w_star(means, best_arm, w_tolerance, max_w_iterations);
            best_arm_score = t * W_star - n[0];
            next_arm = 0;
            for(int j = 1; j < 4; j++){
                
            }
        }



    }
    

    
}

int get_MCTS_next_move(int* tiles, int score, double* params){
    /*takes in the set of tiles (in int rep form), the current score, and a set of parameters
        [0]: double: delta (confidence in best arm selection)
        [1]: int: max trials if confidence is not met
        [2]: double: tolerance for W*
        [3]: int: max iterations for W* if tolerance is not met
        [4]:
     returns the best move from this state
    */
}


int main(){
    double means[4] = {0.2,0.4,0.7,0.6};
    int best = 1;
    double tolerance = 1e-5;
    int max_iter = 10000;

    printf("%f\n", compute_w_star(means, 0, tolerance, max_iter));
    printf("%f\n", compute_w_star(means, 1, tolerance, max_iter));
    printf("%f\n", compute_w_star(means, 2, tolerance, max_iter));
    printf("%f\n", compute_w_star(means, 3, tolerance, max_iter));
    srand(time(NULL));

    Board b1 = {
        {0,0,0,1,
        0,0,0,1,
        0,6,0,0,
        0,0,6,0},
        0
    };
    srand(time(NULL));
    for(int i = 0; i < 1000; i++){
        Board b1 = {
        {0,0,0,1,
        0,0,0,1,
        0,6,0,0,
        0,0,6,0},
        0
    };
    printf("%d\n", run_trial_until_win(&b1, 8));
    }
    

    return 1;


}




