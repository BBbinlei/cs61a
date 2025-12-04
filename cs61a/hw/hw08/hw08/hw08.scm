(define (ascending? s) 
    (if (or (null? s) (null? (cdr s)))
        #t
        (and (<= (car s) (car (cdr s))) (ascending? (cdr s)))
    )
)

(define (my-filter pred s) 
    (if (null? s)
        s
        (if (pred (car s))
            (cons (car s) (my-filter pred (cdr s)))
            (my-filter pred (cdr s))
        )
    )
)

(define (interleave lst1 lst2) 
    (if (or (null? lst1) (null? lst2))
        (append lst1 lst2)
        (cons (car lst1) (cons (car lst2) (interleave (cdr lst1) (cdr lst2))))
    )
)

(define (no-repeats s) 
    (define (filter? a s)
        (cond
            ((null? s) #f)
            ((= a (car s)) #t)
            (else (filter? a (cdr s)))
        
        )
    )
    (define (main s)
        (cond 
            ((null? s) s)
            ((filter? (car s) (cdr s)) (main (cdr s)))
            (else (cons (car s) (main (cdr s))))        
        )
    
    )
    (main s)
)
