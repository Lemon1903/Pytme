truth a = true;

plaza abyss message(){
    display("Hello World");
}

plaza abyss sum( point a , point b){
    display( a + b );
}

plaza point max( point x , point y){
    if ( x > y ) {
        dispatch x;
    } else {
        dispatch y;
    }
}

message();
sum( 1 , 3 );

max( 10 , 20 );
display( mx );