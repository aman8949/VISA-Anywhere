Lambda <- 100

> Mue <- 20
> Rho <- Lambda/Mue
> N <- 50

> matrix <- matrix(0,100,3)
> matrix[,1] <- 1:100
> calculatewq(6)

> calculatewq <- function(c){
 P0inv <- (Rho^c*(1-((Rho/c)^(N-c+1))))/(factorial(c)*(1-(Rho/c)))
 for (i in 1:c-1) {
 P0inv = P0inv + (Rho^i)/factorial(i)
 }
 P0 = 1/P0inv
 Lq = (Rho^(c+1))*(1-((Rho/c)^(N-c+1))-((N-c+1)*(1-(Rho/c))*((Rho/c)^(N-c))))*P0/(factorial(c-1)*(c-Rho)^2)
 Wq = 60*Lq/Lambda
 Ls <- Lq + Rho
 Ws <- 60*Ls/Lambda
 PN <- (Rho^N)*P0/(factorial(c)*c^(N-c))
 customer_serviced <- (1 - PN)*100
 #print(paste(Lq," is queue length and ",Wq," is the waiting time"))
 a <- cbind(Lq,Wq,Ls,Ws,customer_serviced)
 return(a)
 }

> for (i in 1:100){
 matrix[i,2] <- calculatewq(i)[2]
 matrix[i,3] <- calculatewq(i)[5]
 }