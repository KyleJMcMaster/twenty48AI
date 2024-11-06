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

void place_random_tile(Board* board){
    // place a tile in a randomly selected empty square
    
    int empty_tiles[15];
    int len_empty_tiles = get_empty_tiles(board, empty_tiles);
    int tile = empty_tiles[rand() % (len_empty_tiles)];
    int tile_value = ((double)rand()/(double)RAND_MAX > 0.1) ? 1 : 2;

    board->tiles[tile] = tile_value;
    }
    
  

bool run_trial_until_win(Board* board, Move move, int stop){
    // run a trial until either the game is won or lost and return the result
    // stop is an exp rep value which specifies the maximum tile required to consider the game as won

    Move next_move = move;
    Board b2;
    copy_board_values(board, &b2);
    apply_move(&b2, next_move);

    while(true){
        int valid_moves[4];
        int num_valid_moves = get_valid_moves(&b2, valid_moves);
        
        if(!num_valid_moves){
            return 0;
        }
        next_move = valid_moves[rand() % (num_valid_moves)];      
        apply_move(&b2, next_move);
        
        for(int i = 0; i < 16; i++){
            if (b2.tiles[i] >= stop){
                return 1;
            }
        }
        place_random_tile(&b2);
      
    }
}
double Ifonc(double alpha, double m1, double m2){
    if (alpha == 0 || alpha == 1){return 0;}

    double mid = alpha*m1 + (1-alpha)*m2;

    return alpha*KL_divergence(m1, mid)+(1-alpha)*KL_divergence(m2, mid);
}
double g(double x, int k, double* means){
    double cost = 0;
    double n1 = 1/(1+x);
    double n2 = x/(1+x);
    if( n1 == 0 && n2==0){cost = 0;}
    else{
        cost = (n1+n2)*Ifonc(n1/(n1+n2), means[0], means[k]);
    }
    return cost;
}
double dico_solve_g(double xmin, double xmax, double delta, double* means, int k){
    double min = xmin;
    double max = xmax;
    double mid;

    double res = g(min, k, means);
    while(max-min>delta){
        mid = (max+min)/2;
        if(g(mid, k, means)* res > 0){min = mid;}
        else{max=mid;}
    }
    return (max+min)/2;

}

double xk_of_y(double y, int k, double* means, double delta){
    double xMax = 1;
    while(g(xMax, k, means) < 0){
        xMax = 2*xMax;
    }
    return dico_solve_g(0, xMax, delta, means, k);
}


double aux(double y, double* means, double delta, int k){
    double x[k-1];
    double m[k-1];
    for(int i = 0; i < k-1; i++){
        x[i] = xk_of_y(y, i+1, means, delta);
    }
    for(int i = 0; i < k-1; i++){
        m[i] = (means[0] + x[i]*means[i+1])/x[i];
    }
    double sum = 0;
    for(int i = 0; i < k-1; i++){
        sum += KL_divergence(means[0], m[i])/KL_divergence(means[i+1], m[i]);
    }
    return sum - 1;
}

double dico_solve_aux(double ymin, double ymax, double delta, double* means, int k){
    double min = ymin;
    double max = ymax;
    double mid;

    double res = aux(min, means, delta, k);
    while(max-min>delta){
        mid = (max+min)/2;
        if(aux(mid, means, delta, k)* res > 0){min = mid;}
        else{max=mid;}
    }
    return (max+min)/2;
}


void one_step_opt(double* w, double* means, double delta, int k){
    double yMax=0.5;
    double y;
    double x[k];
    double sum = 1;

    x[0] = 1;
    if(isinf(KL_divergence(means[0], means[1]))){
        while(aux(yMax, means, delta,k) < 0){
            yMax = yMax*2;
        }
    }
    else{yMax = KL_divergence(means[0], means[1]);}

    y = dico_solve_aux(0, yMax, delta, means,k);
    
    for(int i = 1; i < k; i++){
        x[i] = xk_of_y(y, i, means, delta);
        sum += x[i];
    }
    for(int i = 0; i < k; i++){
        w[i] = x[i]/sum;
    }
    
}


int compare_function(const void *a,const void *b) {
    double *x = (double *) a;
    double *y = (double *) b;
    // return *x - *y; // this is WRONG...
    if (x[0] < y[0]) return -1;
    else if (x[0] > y[0]) return 1; return 0;
}

void optimal_weights(double *w, double *means, double delta, int k){
    // get the values for w*
    int num_max_arms;
    int max_arms[k]; // refers to moves [0...3]
    double max_arm_val;

    num_max_arms = 1;
    max_arm_val = means[0];
    max_arms[0] = 0;
    for(int i = 1; i < k; i++){
        if(means[i] > max_arm_val){
            num_max_arms = 1;
            max_arm_val = means[i];
            max_arms[0] = i;
        }
        else if(means[i] == max_arm_val){
            max_arms[num_max_arms] = i;
            num_max_arms++; 
        }
    }

    if(num_max_arms>1){
        //if multiple max arms, set max arms to uniform dist
        for(int i = 0; i < k; i ++){
            w[i] = 0;
        }
        for(int i = 0; i < num_max_arms; i ++){
            w[max_arms[i]] = 1.0/(double)num_max_arms;
        }
        return;
    }

    double sorted_means[4][2]; // stores mean and original index
    for(int i = 0; i < k; i ++){
        sorted_means[i][0] = means[i];
        sorted_means[i][1] = i;
    }

    qsort(sorted_means, k, sizeof(sorted_means[0]), compare_function);

    // sort mu
    for(int i = 0; i < k; i ++){
        means[i] = sorted_means[i][0];
    }

    one_step_opt(w, means, delta, k);

    // return to original order
    for(int i = 0; i < k; i ++){
        w[(int)sorted_means[i][1]] = w[i];
    }

}
int track_and_stop(Board* board, double* params){
    // track and stop algorithm described by Garivier and Kaufmann 2016
    int valid_moves[4];
    int k = get_valid_moves(board, valid_moves);
    int n[k];
    double means[k];
    int S[k];
    double confidence = params[0];
    int max_trials = (int) params[1];
    double w_tolerance = params[2];
    int max_w_iterations = (int) params[3];
    int win_threshold = (int) params[4];
    
    int num_max_arms;
    int max_arms[k]; // refers to moves [0...3]
    double max_arm_val;
    int best_index;
    //step1
    int n_best;
    int s_best;
    double mean_best;
    double avg_means[k];
    //step2
    double min_score;
    double score;
    //step3
    int min_n;
    int min_n_index;
    double exploration_threshold;
    double w[k];
    int max_score_index;
    int max_score;

    srand(time(NULL));
    if (k == 1){return valid_moves[0];}

    //step 0: run first trial
    for(int i = 0; i < k; i++){
        n[i] = 1;
        S[i] = run_trial_until_win(board, valid_moves[i], win_threshold);
        means[i] = S[i];
    }

    for(int t = k; t < max_trials; t++){
        // step 1: find empirical best arm(s)
        num_max_arms = 1;
        max_arm_val = means[0];
        max_arms[0] = 0;
        for(int i = 1; i < k; i++){
            if(means[i] > max_arm_val){
                num_max_arms = 1;
                max_arm_val = means[i];
                max_arms[0] = i;
            }
            else if(means[i] == max_arm_val){
                max_arms[num_max_arms] = i;
                num_max_arms++; 
            }
        }
        best_index = max_arms[0]; // index of best arm

        //if multiple best arms, draw one at random, no need to check stopping statistic
        if(num_max_arms>1){
            best_index = max_arms[rand() % (num_max_arms)];
            t+=1;
            S[best_index] += run_trial_until_win(board, valid_moves[best_index], win_threshold);
            n[best_index]++;
            means[best_index] = S[best_index]/n[best_index];
            continue;
        }
        //otherwise, check stopping statistic
        // step 2: calculate stopping statistic
        
        mean_best = means[best_index];
        n_best = n[best_index];

        for(int i = 0; i < k; i++){
            avg_means[i] = (means[i] + mean_best)/2;
        }

        min_score = INFINITY;
        for(int i = 0; i < k; i ++){
            if(i == best_index){continue;} // skip best
            score = n_best*KL_divergence(mean_best, avg_means[i]) + n[i]*KL_divergence(means[i], avg_means[i]);
            min_score = (score < min_score) ? score : min_score;
        }

        if(min_score > log(2*t*(k-1)/confidence)){ //log((log(t)+1)/delta) is alternative stopping point
            // stop
            printf("Min Score _thresh met: %f\n", min_score);
            for(int i = 0; i < k; i ++){
                printf("%f, ", means[i]);
            }
            printf("\n");
            return valid_moves[best_index];
        }

        // step 3: pick arm to sample
        min_n_index = 0;
        min_n = n[0];
        exploration_threshold = sqrt(t) - 2;
        for(int i = 1; i < 4; i ++){
            if(n[i] < min_n){
                min_n = n[i];
                min_n_index = i;
            }
        }
        if(min_n < exploration_threshold){
            // enter forced exploration
            best_index = min_n_index;
            t+=1;
            S[best_index] += run_trial_until_win(board, valid_moves[best_index], win_threshold);
            n[best_index]++;
            means[best_index] = S[best_index]/n[best_index];
            continue;
        }
        // optimal arm selection

        optimal_weights(w, means, w_tolerance, k);
        max_score_index = 0;
        max_score = w[0] - (double)n[0]/(double)t;
        for(int i = 1; i < 4; i++){
            score = w[i] - (double)n[i]/(double)t;
            if(max_score < score){
                max_score = score;
                max_score_index = i;
            }
        }
        best_index = max_score_index;
        t+=1;
        S[best_index] += run_trial_until_win(board, valid_moves[best_index], win_threshold);
        n[best_index]++;
        means[best_index] = S[best_index]/n[best_index];
        continue;
        
    }
    printf("Min Score: %f\n", min_score);
    for(int i = 0; i < k; i ++){
        printf("%f, ", means[i]);
    }
    printf("\n");
    return valid_moves[best_index];

    

    
}

int get_MCTS_next_move(int* tiles, int score, double* params){
    /*takes in the set of tiles (in int rep form), the current score, and a set of parameters
        [0]: double: delta (confidence in best arm selection)
        [1]: int: max trials if confidence is not met
        [2]: double: tolerance for W*
        [3]: int: max iterations for W* if tolerance is not met
        [4]: int: value for 'win' condition in exp value
     returns the best move from this state
    */


    char powertiles[16];
    intrep_to_powerrep(powertiles, tiles);

    Board b; 
    for(int i =  0; i < 16; i ++){
        b.tiles[i] = powertiles[i];
    }
    b.score = score;

    
    return track_and_stop(&b, params);
}


int main(){
    double means[4] = {0.2,0.4,0.7,0.6};
    int best = 1;
    double tolerance = 1e-5;
    int max_iter = 10000;
    double params[5] ={0.9999, 10000, 1e-11, 10000, 10};

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
    printf("%d\n", run_trial_until_win(&b1, 0, 8));
    }
    printf("best move: %d\n", get_MCTS_next_move((int * )b1.tiles, b1.score, params));


    return 1;


}




