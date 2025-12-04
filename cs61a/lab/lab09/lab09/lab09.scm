(define (over-or-under num1 num2) 
   (if(> num1 num2) 1 (if(< num1 num2) -1 0)))
  

(define (make-adder num) 
  (lambda (x) (+ x num))
)

(define (composed f g) 
  (lambda (x) (f (g x)))
  )

(define (repeat f n) 
  (define (repeat-helper current-fn k)
    (cond
      ((= k 1) current-fn)
      (else (repeat-helper (composed current-fn f) (- k 1)))

    )
  )
  (if(= n 1)
    f 
    (repeat-helper f n)
  )
  
)
(define (max a b)
  (if (> a b)
      a
      b))

(define (min a b)
  (if (> a b)
      b
      a))

(define (gcd a b) 
  (define (gcd_helper m n)
    (if (= n 0)
      m
      (gcd_helper n (remainder m n))
    )
  )
  (gcd_helper (max a b) (min a b))  
)
