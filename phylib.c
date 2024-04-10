#include "phylib.h"
//void printTable(phylib_table * table);
//part1
phylib_object *phylib_new_still_ball(unsigned char number,
phylib_coord *pos ){

    phylib_object *new_object = (phylib_object *)calloc(1,sizeof(phylib_object));

    //if alloc fails
    if(new_object==NULL){
        return NULL;
    }
    new_object->type = PHYLIB_STILL_BALL;
    new_object->obj.still_ball.number = number;
    new_object->obj.still_ball.pos = *pos;

    return new_object;
}

phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc ){

    phylib_object *new_object = (phylib_object *)calloc(1,sizeof(phylib_object));

    //if alloc fails
    if(new_object==NULL){
        return NULL;
    }

    new_object->type = PHYLIB_ROLLING_BALL;
    new_object->obj.rolling_ball.pos = *pos;
    new_object->obj.rolling_ball.vel = *vel;
    new_object->obj.rolling_ball.number = number;
    new_object->obj.rolling_ball.acc = *acc;

    return new_object;
}

phylib_object *phylib_new_hole( phylib_coord *pos){

    phylib_object *new_object = (phylib_object *)calloc(1,sizeof(phylib_object));

    //if malloc fails
    if(new_object==NULL){
        return NULL;
    }
    new_object->type = PHYLIB_HOLE;
    new_object->obj.hole.pos = *pos;

    return new_object;
}

phylib_object *phylib_new_hcushion(double y){

    phylib_object *new_object = (phylib_object *)malloc(sizeof(phylib_object));

    //if malloc fails
    if(new_object==NULL){
        return NULL;
    }

    new_object->type = PHYLIB_HCUSHION;
    new_object->obj.hcushion.y = y;

    return new_object;
}

phylib_object *phylib_new_vcushion( double x ){

    phylib_object *new_object = (phylib_object *)malloc(sizeof(phylib_object));

    //if malloc fails
    if(new_object==NULL){
        return NULL;
    }

    new_object->type = PHYLIB_VCUSHION;
    new_object->obj.vcushion.x = x;

    return new_object;
}

phylib_table *phylib_new_table(void){

    phylib_table *newTable =(phylib_table *)malloc(sizeof(phylib_table));

    //if malloc fails
    if(newTable==NULL){
        return NULL;
    }

    newTable->time=0.0;

    //set array
    newTable->object[0] = phylib_new_hcushion(0.0);
    newTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH); 
    newTable->object[2] = phylib_new_vcushion(0.0); 
    newTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH); 
    newTable->object[4] = phylib_new_hole(&(phylib_coord){0.0, 0.0}); 
    newTable->object[5] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH / 2.0}); 
    newTable->object[6] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH}); 
    newTable->object[7] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, 0.0});
    newTable->object[8] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH / 2.0});
    newTable->object[9] =phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH}); 
    for(int i=0;i<10;i++){
        if(newTable->object[i]==NULL){
            return NULL;
        }
    }
    for (int i = 10; i < PHYLIB_MAX_OBJECTS; ++i) {
        newTable->object[i] = NULL;
    }
    return newTable;
}
//part2

void phylib_copy_object(phylib_object **dest, phylib_object **src){

    if(*src==NULL){
        *dest=NULL;
        return;
    }
     *dest = (phylib_object *)malloc(sizeof(phylib_object));
    if(*dest==NULL){
        return;
    }
    memcpy(*dest, *src, sizeof(phylib_object));

 }

phylib_table *phylib_copy_table( phylib_table *table ){
    
    if(table==NULL){
        return NULL;
    }

    phylib_table *newTable =(phylib_table *)malloc(sizeof(phylib_table));
    if(newTable==NULL){
        return NULL;
    }
    newTable->time = table->time;
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] != NULL) {
            phylib_copy_object(&(newTable->object[i]),&(table->object[i]));
        }
        else{
            newTable->object[i] = NULL;
        }
    }
    return newTable;
}

void phylib_add_object( phylib_table *table, phylib_object *object ){

    for(int i=0;i<PHYLIB_MAX_OBJECTS;i++){
        if(table->object[i]==NULL){
            table->object[i]= object;
            return;
        }
    }
}

void phylib_free_table(phylib_table *table ){

    if(table==NULL){
        return;
    }

    for(int i=0;i<PHYLIB_MAX_OBJECTS;i++){
        if(table->object[i]!=NULL){
            free(table->object[i]);
            table->object[i]=NULL;
        }
    }
    free(table);
    table=NULL;
}

phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2){
    phylib_coord answer;
    answer.x=c1.x-c2.x;
    answer.y=c1.y-c2.y;
    return answer;
}

double phylib_length(phylib_coord c){
    double length =sqrt((c.x * c.x) + (c.y * c.y));
    return length;
}

double phylib_dot_product( phylib_coord a, phylib_coord b ){

    double dotProduct= (a.x*b.x)+(a.y*b.y);
    return dotProduct;
}

double phylib_distance( phylib_object *obj1, phylib_object *obj2 ){

    double distance=0.0;
    phylib_coord obj1Center;
    phylib_coord obj2Center;
    
    if(obj1==NULL){
        return -1.0;
    }
    if(obj2==NULL){
        return -1.0;
    }
    if(obj1->type!=PHYLIB_ROLLING_BALL){
        return -1.0;
    }

    obj1Center.x = obj1->obj.rolling_ball.pos.x;
    obj1Center.y = obj1->obj.rolling_ball.pos.y;
    obj2Center.x = 0.0;
    obj2Center.y = 0.0;

    if(obj2->type==PHYLIB_ROLLING_BALL || obj2->type==PHYLIB_STILL_BALL){
        if (obj2->type == PHYLIB_ROLLING_BALL) {
            obj2Center = obj2->obj.rolling_ball.pos;
        } else if (obj2->type == PHYLIB_STILL_BALL) {
            obj2Center= obj2->obj.still_ball.pos;
        }
        distance = phylib_length(phylib_sub(obj1Center, obj2Center)) - PHYLIB_BALL_DIAMETER;
    }else if(obj2->type==PHYLIB_HOLE){
        obj2Center = obj2->obj.hole.pos;
        distance = phylib_length(phylib_sub(obj1Center, obj2Center)) - PHYLIB_HOLE_RADIUS;

    }else if (obj2->type == PHYLIB_VCUSHION){
        distance = fabs(obj1Center.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
    }
    else if (obj2->type == PHYLIB_HCUSHION) {
            distance = fabs(obj1Center.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;
    }
    else{
        return -1.0;
    }

    return distance;
}

//part3

void phylib_roll(phylib_object *new, phylib_object *old, double time){
    
    if(new->type!=PHYLIB_ROLLING_BALL || old->type!=PHYLIB_ROLLING_BALL){
        return;
    }

    //calc new positions
    new->obj.rolling_ball.pos.x=old->obj.rolling_ball.pos.x + (old->obj.rolling_ball.vel.x * time) + (0.5 * old->obj.rolling_ball.acc.x * time * time);
    new->obj.rolling_ball.pos.y=old->obj.rolling_ball.pos.y + (old->obj.rolling_ball.vel.y * time)+ (0.5 * old->obj.rolling_ball.acc.y * time * time);

    //calc new vel
    new->obj.rolling_ball.vel.x= old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x * time;
    new->obj.rolling_ball.vel.y= old->obj.rolling_ball.vel.y + old->obj.rolling_ball.acc.y * time;

    if(new->obj.rolling_ball.vel.x * old->obj.rolling_ball.vel.x<0){
        new->obj.rolling_ball.vel.x=0;
        new->obj.rolling_ball.acc.x=0;
    }
    if(new->obj.rolling_ball.vel.y * old->obj.rolling_ball.vel.y<0){
        new->obj.rolling_ball.vel.y=0;
        new->obj.rolling_ball.acc.y=0;
    }
}

unsigned char phylib_stopped(phylib_object *object ){

    double speed=0.0;
    speed= phylib_length(object->obj.rolling_ball.vel);

    if(speed<PHYLIB_VEL_EPSILON){
        unsigned char ballNum=object->obj.rolling_ball.number;
        phylib_coord ballPos = object->obj.rolling_ball.pos;
        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.number=ballNum;
        object->obj.still_ball.pos=ballPos;
        return 1;
    }
    else{
        return 0;
    }
}

void phylib_bounce(phylib_object **a, phylib_object **b ){
    //declarations
    phylib_coord r_ab;
    phylib_coord v_rel;
    phylib_coord n;
    phylib_coord holderPos;
    double v_rel_n;
    unsigned char num=0;

    if ((*a) == NULL || (*b) == NULL) {
        // Invalid input, one or both objects are NULL
        return;
    }
    if((*a)->type!=PHYLIB_ROLLING_BALL){
        return;
    }

    switch ((*b)->type) {
        case PHYLIB_HCUSHION:
            (*a)->obj.rolling_ball.vel.y = -1 * (*a)->obj.rolling_ball.vel.y;
            (*a)->obj.rolling_ball.acc.y = -1 * (*a)->obj.rolling_ball.acc.y;
        break;

        case PHYLIB_VCUSHION:
            (*a)->obj.rolling_ball.vel.x = -1 *  (*a)->obj.rolling_ball.vel.x;
            (*a)->obj.rolling_ball.acc.x = -1 * (*a)->obj.rolling_ball.acc.x;
        break;

        case PHYLIB_HOLE:
            free(*a);
            (*a)=NULL;
        break;

        case PHYLIB_STILL_BALL:
            holderPos= (*b)->obj.still_ball.pos;
            num=(*b)->obj.still_ball.number;
            (*b)->type = PHYLIB_ROLLING_BALL;
            (*b)->obj.rolling_ball.pos=holderPos;
            (*b)->obj.rolling_ball.number=num;
            (*b)->obj.rolling_ball.acc.x=0.0;
            (*b)->obj.rolling_ball.acc.y=0.0;
            (*b)->obj.rolling_ball.vel.x=0.0;
            (*b)->obj.rolling_ball.vel.y=0.0;

        case PHYLIB_ROLLING_BALL:
            r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
            v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
            n.x = r_ab.x / phylib_length(r_ab);
            n.y = r_ab.y / phylib_length(r_ab);
            v_rel_n = phylib_dot_product(v_rel, n);
 
            //update ball a
            (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
            (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;

            //update ball b
            (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
            (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

            double aSpeed= phylib_length((*a)->obj.rolling_ball.vel);
            double bSpeed = phylib_length((*b)->obj.rolling_ball.vel);
            
            if(aSpeed>PHYLIB_VEL_EPSILON){
                (*a)->obj.rolling_ball.acc.x= -1*(*a)->obj.rolling_ball.vel.x /aSpeed*PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y= -1*(*a)->obj.rolling_ball.vel.y /aSpeed*PHYLIB_DRAG;
            }
            if(bSpeed>PHYLIB_VEL_EPSILON){
                (*b)->obj.rolling_ball.acc.x= -1*(*b)->obj.rolling_ball.vel.x / bSpeed*PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y= -1*(*b)->obj.rolling_ball.vel.y /bSpeed* PHYLIB_DRAG;
            }
        break;
    }
}

unsigned char phylib_rolling( phylib_table *t ){

    //indicate failure?
    if(t==NULL){
        return -1;
    }
    unsigned char counter=0;
    int i=0;
    while(i<PHYLIB_MAX_OBJECTS){
        if(t->object[i]!=NULL &&t->object[i]->type==PHYLIB_ROLLING_BALL){
            counter++;
        }
        i++;
    }
     return counter;

    }
phylib_table * phylib_segment(phylib_table *table){

    if(table==NULL){
        return NULL;
    }
    double distanceBetween=0.0;
    phylib_table *newTable = phylib_copy_table(table);

    if(newTable==NULL){
        return NULL;
    }

    unsigned char numRolling=phylib_rolling(newTable);
    if(numRolling<1){
        phylib_free_table(newTable);
        return NULL;
    }
    double thisTime=PHYLIB_SIM_RATE;

    while(thisTime<PHYLIB_MAX_TIME){
        for(int i=0;i<PHYLIB_MAX_OBJECTS;i++){
             if(newTable->object[i]!=NULL && newTable->object[i]->type==PHYLIB_ROLLING_BALL){
                phylib_roll(newTable->object[i],table->object[i], thisTime);
                //phylib_stopped(newTable->object[i]);
            }
        }
        for(int i=0;i<PHYLIB_MAX_OBJECTS;i++){
            if(newTable->object[i]!=NULL &&  newTable->object[i]->type==PHYLIB_ROLLING_BALL){
                for(int j=0;j<PHYLIB_MAX_OBJECTS;j++){
                    if(newTable->object[j]!=NULL && j!=i){
                        if(phylib_stopped(newTable->object[i])){
                            newTable->time+=(thisTime);
                            return newTable;
                        }
                        distanceBetween = phylib_distance(newTable->object[i],newTable->object[j]);
                        if(distanceBetween<0.0){
                            phylib_bounce(&(newTable->object[i]),&(newTable->object[j]));
                            newTable->time+=(thisTime);
                            return newTable;
                        }
                    }
                }
            }
        }
        thisTime+=PHYLIB_SIM_RATE;
    }
    newTable->time+=thisTime;
    return newTable;
}

//new one
char *phylib_object_string( phylib_object *object )
{
static char string[80];
if (object==NULL)
{
snprintf( string, 80, "NULL;" );
return string;
}
switch (object->type)
{
case PHYLIB_STILL_BALL:
snprintf( string, 80,
"STILL_BALL (%d,%6.1lf,%6.1lf)",
object->obj.still_ball.number,
object->obj.still_ball.pos.x,
object->obj.still_ball.pos.y );
break;
case PHYLIB_ROLLING_BALL:
snprintf( string, 80,
"ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
object->obj.rolling_ball.number,
object->obj.rolling_ball.pos.x,
object->obj.rolling_ball.pos.y,
object->obj.rolling_ball.vel.x,
object->obj.rolling_ball.vel.y,
object->obj.rolling_ball.acc.x,
object->obj.rolling_ball.acc.y );
break;
case PHYLIB_HOLE:
snprintf( string, 80,
"HOLE (%6.1lf,%6.1lf)",
object->obj.hole.pos.x,
object->obj.hole.pos.y );
break;
case PHYLIB_HCUSHION:
snprintf( string, 80,
"HCUSHION (%6.1lf)",
object->obj.hcushion.y );
break;
case PHYLIB_VCUSHION:
snprintf( string, 80,
"VCUSHION (%6.1lf)",
object->obj.vcushion.x );
break;
}
return string;
}
